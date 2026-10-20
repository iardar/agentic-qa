from playwright.sync_api import Locator


class Comment:
    """Represents a single comment displayed on an article page."""

    def __init__(self, root: Locator) -> None:
        self.root = root

        self.body = root.locator(".card-text")

        self.delete_button = root.locator(".mod-options .ion-trash-a")

    def author_link(self, username: str) -> Locator:
        return self.root.get_by_role(
            "link",
            name=username,
            exact=True,
        )

    def delete(self) -> None:
        self.delete_button.click()
