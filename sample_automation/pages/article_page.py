from playwright.sync_api import Locator, Page

from sample_automation.pages.base_page import BasePage


class ArticlePage(BasePage):
    def __init__(
        self,
        page: Page,
        base_url: str,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
        )

        self.article_body = page.locator(".article-content p")

        self.edit_button = page.get_by_role(
            "link",
            name="Edit Article",
        )

        self.delete_button = page.get_by_role(
            "button",
            name="Delete Article",
        )

    def open(
        self,
        slug: str,
    ) -> None:
        self.open_path(f"/article/{slug}")

    def title(
        self,
        title: str,
    ) -> Locator:
        return self.page.get_by_role(
            "heading",
            name=title,
            exact=True,
        )

    def body(self) -> Locator:
        return self.article_body

    def edit_article(self) -> None:
        self.edit_button.click()

    def delete_article(self) -> None:
        self.delete_button.click()
