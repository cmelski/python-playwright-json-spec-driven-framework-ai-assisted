import os

DATA_MAP = {
    "VALID_USERNAME": os.getenv("VALID_USERNAME"),
    "VALID_PASSWORD": os.getenv("VALID_PASSWORD"),
    "INVALID_USERNAME": "bad_user@yahoo.com",
    "INVALID_PASSWORD": "bad_pass",
    "INVALID_LOGIN_ERROR_MESSAGE": "Incorrect email or password.",
    "EMAIL_PASSWORD_REQUIRED_ERROR_MESSAGE": "*Email is required. *Password is required.",
    "PRODUCT_TO_VIEW": "ADIDAS",
    "MIN_PRICE_FILTER": "10000",
    "MAX_PRICE_FILTER": "15000",
    "SEARCH_TEXT": "ADIDAS",
    "HOUSEHOLD_FILTER": "household",
    "CART_ITEMS": ("ZARA", "IPHONE"),
    "CART_ICON_TEXT": "Cart"
}
