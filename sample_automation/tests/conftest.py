import os

import pytest
from playwright.sync_api import Page

from sample_automation.pages.todo_page import TodoPage


@pytest.fixture
def todo_app_url() -> str:
    return os.getenv(
        "TODO_APP_URL",
        "https://demo.playwright.dev/todomvc/",
    )


@pytest.fixture
def todo_page(
    page: Page,
    todo_app_url: str,
) -> TodoPage:
    todo_page = TodoPage(
        page=page,
        base_url=todo_app_url,
    )

    todo_page.open()

    return todo_page


@pytest.fixture
def existing_todo(
    todo_page: TodoPage,
) -> str:
    title = "Buy groceries"

    todo_page.add_todo(title)

    return title
