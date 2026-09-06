import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from sample_automation.pages.home_page import (
    HomePage,
)
from sample_automation.pages.login_page import (
    LoginPage,
)

load_dotenv()


pytest_plugins = ("sample_automation.fixtures.users",)


@pytest.fixture
def realworld_base_url() -> str:
    return os.getenv(
        "REALWORLD_BASE_URL",
        "https://demo.realworld.show",
    )


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
def home_page(
    page: Page,
    realworld_base_url: str,
) -> HomePage:
    return HomePage(
        page=page,
        base_url=realworld_base_url,
    )
