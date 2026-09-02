from playwright.sync_api import Locator, Page

from sample_automation.pages.base_page import BasePage


class TodoPage(BasePage):
    def __init__(
        self,
        page: Page,
        base_url: str,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
        )

        self.new_todo_input = page.get_by_role(
            "textbox",
            name="What needs to be done?",
        )

        self.todo_items = page.get_by_role(
            "listitem",
        )

        self.completed_filter = page.get_by_role(
            "link",
            name="Completed",
        )

        self.active_filter = page.get_by_role(
            "link",
            name="Active",
        )

        self.all_filter = page.get_by_role(
            "link",
            name="All",
        )

    def add_todo(
        self,
        title: str,
    ) -> None:
        self.new_todo_input.fill(title)
        self.new_todo_input.press("Enter")

    def todo_item(
        self,
        title: str,
    ) -> Locator:
        return self.todo_items.filter(
            has_text=title,
        )

    def todo_checkbox(
        self,
        title: str,
    ) -> Locator:
        return self.todo_item(title).get_by_role(
            "checkbox",
            name="Toggle Todo",
        )

    def complete_todo(
        self,
        title: str,
    ) -> None:
        self.todo_checkbox(title).check()

    def show_completed(self) -> None:
        self.completed_filter.click()

    def show_active(self) -> None:
        self.active_filter.click()

    def show_all(self) -> None:
        self.all_filter.click()
