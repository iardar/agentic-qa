from playwright.sync_api import Locator, Page


class Navigation:
    def __init__(
        self,
        page: Page,
    ) -> None:
        self.page = page

    def user_profile_link(
        self,
        username: str,
    ) -> Locator:
        return self.page.get_by_role(
            "link",
            name=username,
            exact=True,
        )
