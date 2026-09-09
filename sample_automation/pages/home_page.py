from playwright.sync_api import Page

from sample_automation.components.navigation import (
    Navigation,
)
from sample_automation.pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    def __init__(
        self,
        page: Page,
        base_url: str,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
        )

        self.navigation = Navigation(page=page)
