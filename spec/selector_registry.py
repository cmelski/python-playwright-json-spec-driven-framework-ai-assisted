import os

SELECTOR_MAP = {
    "LOGIN_PAGE": os.environ.get('BASE_URL'),
    "DASHBOARD_PAGE": "https://rahulshettyacademy.com/client/#/dashboard/dash",
    "USERNAME_INPUT": "#userEmail",
    "PASSWORD_INPUT": "#userPassword",
    "LOGIN_BUTTON": "input[value='Login']",
    "INVENTORY_CARDS": ".card",
    "PRODUCT_DETAILS": ".row",
    "PRODUCT_NAME": ".row h2",
    "FILTERS_FORM": "#sidebar form",
    "SEARCH_TEXT_FILTER": "#sidebar form input[name='search']",
    "MIN_PRICE_FILTER": "#sidebar form input[name='minPrice']",
    "MAX_PRICE_FILTER": "#sidebar form input[name='maxPrice']",
    "CONTINUE_SHOPPING_BUTTON": ".continue"

}
