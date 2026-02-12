import json
import pytest
import time
from spec.executor import execute_step, execute_assertion
from utilities.logging_utils import logger_utility
from utilities.scenario_context import ScenarioContext


# measure time of each test using this decorator
# In pytest, decorators are useful, but fixtures and hooks are often preferred for lifecycle concerns
# because decorators can hide behavior and make debugging harder.
def measure_time(func):
    def wrapper(page_instance, *args, **kwargs):
        start = time.time()
        result = func(page_instance, *args, **kwargs)
        logger_utility().info(f"{func.__name__} took {time.time() - start:.2f}s")
        return result

    return wrapper


@measure_time
def test_from_spec(page_instance):
    with open("features/generated/login.json") as f:
        spec = json.load(f)
        context = ScenarioContext()

        for block in spec["flow"]:

            if "steps" in block:
                for step in block["steps"]:
                    execute_step(page_instance, step, context)

            if "assertions" in block:
                for assertion in block["assertions"]:
                    execute_assertion(page_instance, assertion, context)

    with open("features/generated/view_product.json") as f:
        spec = json.load(f)
        context = ScenarioContext()

        for block in spec["flow"]:

            if "steps" in block:
                for step in block["steps"]:
                    execute_step(page_instance, step, context)

            if "assertions" in block:
                for assertion in block["assertions"]:
                    execute_assertion(page_instance, assertion, context)

    with open("features/generated/product_filters.json") as f:
        spec = json.load(f)
        context = ScenarioContext()

        for block in spec["flow"]:

            if "steps" in block:
                for step in block["steps"]:
                    execute_step(page_instance, step, context)

            if "assertions" in block:
                for assertion in block["assertions"]:
                    execute_assertion(page_instance, assertion, context)

