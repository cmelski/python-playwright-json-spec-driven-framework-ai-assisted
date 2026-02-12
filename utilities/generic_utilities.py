
def reset_form(page, form_selector):
    form = page.locator(form_selector)

    # Clear text fields
    text_inputs = form.locator(
        "input:not([type=checkbox]):not([type=radio]):not([type=submit]), textarea"
    )

    for el in text_inputs.all():
        el.fill("")

    # Uncheck checkboxes
    checkboxes = form.locator("input[type=checkbox]")
    for cb in checkboxes.all():
        if cb.is_checked():
            cb.uncheck()
