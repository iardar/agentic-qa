import pytest
from playwright.sync_api import Page

from sample_automation.pages.home_page import HomePage
from sample_automation.pages.login_page import LoginPage
from sample_automation.pages.register_page import RegisterPage


@pytest.fixture
def login_page(
    page: Page,
    realworld_base_url: str,
) -> LoginPage:
    return LoginPage(
        page=page,
        base_url=realworld_base_url,
    )


@pytest.fixture
def register_page(
    page: Page,
    realworld_base_url: str,
) -> RegisterPage:
    return RegisterPage(
        page=page,
        base_url=realworld_base_url,
    )


@pytest.fixture
def home_page(
    page: Page,
    realworld_base_url: str,
) -> HomePage:
    return HomePage(
        page=page,
        base_url=realworld_base_url,
    )