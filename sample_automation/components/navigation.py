from playwright.sync_api import Locator, Page


class Navigation:
    def __init__(
        self,
        page: Page,
    ) -> None:
        self.root = page.get_by_role("navigation")

        self.home_link = self.root.get_by_role(
            "link",
            name="Home",
            exact=True,
        )

    def user_profile_link(
        self,
        username: str,
    ) -> Locator:
        return self.root.get_by_role(
            "link",
            name=username,
            exact=True,
        )

    def open_home(self) -> None:
        self.home_link.click()
