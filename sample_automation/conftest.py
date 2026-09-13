import os

import pytest
from dotenv import load_dotenv

load_dotenv()


pytest_plugins = (
    "sample_automation.fixtures.authentication",
    "sample_automation.fixtures.users",
    "sample_automation.fixtures.articles",
)


@pytest.fixture
def realworld_base_url() -> str:
    return os.getenv(
        "REALWORLD_BASE_URL",
        "https://demo.realworld.show",
    )


@pytest.fixture
def realworld_api_base_url() -> str:
    return os.getenv(
        "REALWORLD_API_BASE_URL",
        "https://api.realworld.show",
    )
