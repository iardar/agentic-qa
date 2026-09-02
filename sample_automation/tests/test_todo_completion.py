from playwright.sync_api import expect

from sample_automation.pages.todo_page import TodoPage


def test_user_can_complete_todo(
    todo_page: TodoPage,
    existing_todo: str,
) -> None:
    todo_page.complete_todo(existing_todo)

    expect(todo_page.todo_checkbox(existing_todo)).to_be_checked()


def test_completed_todo_appears_in_completed_filter(
    todo_page: TodoPage,
    existing_todo: str,
) -> None:
    todo_page.complete_todo(existing_todo)

    todo_page.show_completed()

    expect(todo_page.todo_item(existing_todo)).to_be_visible()


def test_completed_todo_is_hidden_from_active_filter(
    todo_page: TodoPage,
    existing_todo: str,
) -> None:
    todo_page.complete_todo(existing_todo)

    todo_page.show_active()

    expect(todo_page.todo_item(existing_todo)).to_be_hidden()
