import os

from playwright.sync_api import expect

from spec.data_registry import DATA_MAP
from spec.selector_registry import SELECTOR_MAP
from spec.url_registry import URL_MAP
from utilities import generic_utilities
from utilities.logging_utils import logger_utility
from utilities.scenario_context import ScenarioContext


def run_spec(page, spec):
    context = ScenarioContext()

    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                execute_step(page, step, context)

        if "assertions" in block:
            for assertion in block["assertions"]:
                execute_assertion(page, assertion, context)


def execute_step(page, step: dict, context):
    # use .get because:
    # avoids KeyErrors
    # supports literals
    # supports mapped data
    # keeps execution layer clean
    action = step.get("action")
    target = step.get("target")
    raw_value = step.get("value")
    save_as = step.get("save_as")
    value = DATA_MAP.get(raw_value, raw_value)
    submit = step.get("submit")

    if action == "navigate":
        if target not in URL_MAP:
            raise ValueError(f"Unknown URL target: {target}")

        url = os.environ.get('BASE_URL') + URL_MAP[target]
        logger_utility().info(f"[STEP] Navigate → {url}")
        page.goto(url)

    elif action == "click":
        if target not in SELECTOR_MAP:
            raise ValueError(f"Unknown selector target: {target}")

        selector = SELECTOR_MAP[target]
        if raw_value:
            logger_utility().info(f"[STEP] Find → {value} in {target} and click")
            product = page.locator(selector).filter(has_text=value)
            product.get_by_text('View').click()
        else:
            logger_utility().info(f"[STEP] Click → {target}")
            page.click(selector)

    elif action == "add":
        if target not in SELECTOR_MAP:
            raise ValueError(f"Unknown selector target: {target}")

        selector = SELECTOR_MAP[target]
        if raw_value:
            logger_utility().info(f"[STEP] Find → {value} in {target} and click")
            if len(value) > 1:
                for item in value:
                    product = page.locator(selector).filter(has_text=item)
                    product.get_by_text('Add To Cart').click()
                    page.wait_for_timeout(2000)

            else:
                product = page.locator(selector).filter(has_text=value)
                product.get_by_text('Add To Cart').click()

        else:
            raise ValueError(f"Value not set")

    elif action == "fill":
        selector = SELECTOR_MAP.get(target)
        if not selector:
            raise ValueError(f"Unknown fill target: {target}")

        logger_utility().info(f"[STEP] Fill → {target} = {value}")
        page.fill(selector, value)
        if submit:
            page.locator(selector).press("Enter")

    elif action == "checkbox":
        selector = SELECTOR_MAP.get(target)
        if not selector:
            raise ValueError(f"Unknown fill target: {target}")

        logger_utility().info(f"[STEP] Check → {selector} → value = {value}")

        checkbox_filters = page.locator(selector)

        checkbox_filters_count = checkbox_filters.count()
        logger_utility().info(f'Checkbox filters count: {checkbox_filters_count}')

        for i in range(checkbox_filters_count):
            checkbox = checkbox_filters.nth(i)

            # go to parent container and get label text
            label = checkbox.locator("xpath=ancestor::div[contains(@class,'form-group')]//label").inner_text().strip()

            if label.lower() == value.lower():
                logger_utility().info(f'{value} checkbox found')
                checkbox.check()
                break

    elif action == "clear_form_filters":
        selector = SELECTOR_MAP.get(target)
        if not selector:
            raise ValueError(f"Unknown fill target: {target}")

        logger_utility().info(f"[STEP] Clear → {target}")
        generic_utilities.reset_form(page, selector)

    elif action == "wait":
        ms = step.get("value", 2000)
        logger_utility().info(f"[STEP] Wait → {ms}ms")
        page.wait_for_timeout(ms)

    elif action == "select":
        if target not in SELECTOR_MAP:
            raise ValueError(f"Unknown selector target: {target}")

        selector = SELECTOR_MAP[target]
        logger_utility().info(f"[STEP] Select → {target}")
        page.locator(selector).select_option(value=raw_value)

    elif action == "capture_product_details":
        if target not in SELECTOR_MAP:
            raise ValueError(f"Unknown selector target: {target}")

        selector = SELECTOR_MAP[target]
        logger_utility().info(f"[STEP] Capture → {save_as}")
        if raw_value:
            logger_utility().info(f"[STEP] Find → {value} in {target} and click")
            product = page.locator(selector).filter(has_text=value)
            product_name = product.locator('h5').inner_text().strip()
            product_price = product.locator('.text-muted').inner_text().strip()
            product_details = product_name, product_price
            logger_utility().info(f'Product details saved: {product_details}')
            # save new account to the scenario context
            context.set(save_as, product_details)
        else:
            raise ValueError(f"Raw value unknown: {raw_value}")

    elif action == "save_products_unfiltered":

        if target not in SELECTOR_MAP:
            raise ValueError(f"Unknown selector target: {target}")

        selector = SELECTOR_MAP[target]
        logger_utility().info(f"[STEP] Save → {save_as}")
        unfiltered_product_dict = {"products": []
                                   }
        products = page.locator(selector)
        product_count = products.count()
        for i in range(product_count):
            product_name = products.nth(i).locator('h5').inner_text().strip()
            product_price = products.nth(i).locator('.text-muted').inner_text().strip()
            product_to_add = {
                "product_name": product_name,
                "product_price": product_price,
            }
            unfiltered_product_dict['products'].append(product_to_add)

        logger_utility().info(f'Unfiltered product dictionary: {unfiltered_product_dict}')
        # save new account to the scenario context
        context.set(save_as, unfiltered_product_dict)


    else:
        raise ValueError(f"Unsupported step action: {action}")


def execute_assertion(page, assertion: dict, context):
    action = assertion.get("action")
    target = assertion.get("target")
    state = assertion.get("state")
    text = assertion.get("text")
    raw_value = assertion.get("value")
    value = DATA_MAP.get(raw_value, raw_value)
    contain_text_raw_value = assertion.get("toContainText")
    contain_text = DATA_MAP.get(contain_text_raw_value, contain_text_raw_value)
    condition = assertion.get("condition")
    rule = assertion.get("rule")
    filter_type = assertion.get("filter_type")
    context_key = assertion.get("context_key")

    if action != "expect":
        raise ValueError(f"Unsupported assertion action: {action}")

    if target not in SELECTOR_MAP:
        raise ValueError(f"Unknown assertion target: {target}")

    selector = SELECTOR_MAP[target]
    locator = page.locator(selector)


    logger_utility().info(f"[ASSERT] {target}")

    if state == "visible":
        expect(locator).to_be_visible()
        logger_utility().info(f'{selector} is {state}')

    elif state == "hidden":
        expect(locator).to_be_hidden()
        logger_utility().info(f'{selector} is {state}')

    elif state == "enabled":
        expect(locator).to_be_enabled()
        logger_utility().info(f'{selector} is {state}')

    elif state == "disabled":
        expect(locator).to_be_disabled()
        logger_utility().info(f'{selector} is {state}')

    elif state == "toHaveURL":
        expect(page).to_have_url(selector)
        logger_utility().info(f'page url matches {selector}')

    elif state == "toHaveCount":
        expect(locator.first).to_be_visible()
        products = locator
        product_count = products.count()
        logger_utility().info(f'Product count: {product_count}')
        # for i in range(product_count):
        #     logger_utility().info(f'Product visibility: {products.nth(i).is_visible()}')
        assert f'{product_count} {rule}', f"Expected at least 1 row but found {product_count}"
        logger_utility().info(f'{selector} has product_count {rule}')

    elif state == "cart_count":
        expect(locator.first).to_be_visible()
        cart_icon = locator.filter(has_text=value)
        label_count = cart_icon.locator('label').inner_text().strip()

        assert int(label_count) == rule, f'{int(label_count)}, {rule}'
        logger_utility().info(f'{value} icon has product_count: {rule}')

    if text == "not.empty":
        expect(locator).not_to_be_empty()
        logger_utility().info(f'{selector} is {text}')

    elif isinstance(text, str):
        expect(locator).to_contain_text(text)
        logger_utility().info(f'{selector} contains text: {text}')

    if value == "not.empty":
        expect(locator).not_to_be_empty()
        logger_utility().info(f'{selector} is {value}')

    if isinstance(contain_text, str):
        expect(locator).to_contain_text(contain_text)
        logger_utility().info(f'{selector} contains text: {contain_text}')

    if condition == "product_details_match":
        expected_product_details = context.get(context_key)
        product_name = page.locator(selector + ' h2').inner_text().strip()
        product_price = page.locator(selector + ' h3').inner_text().strip()
        product_details_page = product_name, product_price

        assert expected_product_details == product_details_page, (
            f'Product details do not match. Expected: {expected_product_details} '
            f'Actual: {product_details_page}')
        logger_utility().info(f'Product details match. Expected: {expected_product_details} '
                              f'Actual: {product_details_page}')

    if condition == "products_reflect_filter":

        unfiltered_product_dict = context.get(context_key)
        filtered_product_dict = {"products": []
                                 }
        products = locator
        product_count = products.count()
        for i in range(product_count):
            product_name = products.nth(i).locator('h5').inner_text().strip()
            product_price = products.nth(i).locator('.text-muted').inner_text().strip()
            product_to_add = {
                "product_name": product_name,
                "product_price": product_price,
            }
            filtered_product_dict["products"].append(product_to_add)

        logger_utility().info(f'Filtered product dictionary: {filtered_product_dict}')

        if filter_type == 'min_max':
            page.wait_for_timeout(2000)
            min_price = int(DATA_MAP.get('MIN_PRICE_FILTER'))
            max_price = int(DATA_MAP.get('MAX_PRICE_FILTER'))
            p_name = ''
            for item in filtered_product_dict['products']:
                for k, v in item.items():
                    if k == 'product_name':
                        p_name = v
                    if k == 'product_price':
                        price = int(v.split(' ')[1])
                        logger_utility().info(f'Formatted price: {price}')
                        assert min_price <= price <= max_price
                        logger_utility().info(f'{p_name} price: {v} is correctly between min '
                                              f'and max {min_price}-{max_price}')

        if filter_type == 'search_text':
            page.wait_for_timeout(2000)
            search_text = DATA_MAP.get('SEARCH_TEXT')
            for item in filtered_product_dict['products']:
                for k, v in item.items():
                    if k == 'product_name':
                        assert search_text in v
                        logger_utility().info(f'{v} contains search text: {search_text}')

        if filter_type == 'checkbox':
            page.wait_for_timeout(2000)
            assert product_count == rule
            logger_utility().info(f'Checkbox filter correctly shows {rule} products.')
