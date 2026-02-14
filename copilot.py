import pytest

def test_login(page):
    # playwright test that logs in with standard_user and password_secret
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")

