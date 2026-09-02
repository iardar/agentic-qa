from playwright.sync_api import expect

from sample_automation.pages.todo_page import TodoPage


def test_user_can_create_todo(
    todo_page: TodoPage,
) -> None:
    title = "Buy groceries"

    todo_page.add_todo(title)

    expect(todo_page.todo_item(title)).to_be_visible()


def test_created_todo_is_visible(
    todo_page: TodoPage,
    existing_todo: str,
) -> None:
    expect(todo_page.todo_item(existing_todo)).to_be_visible()
