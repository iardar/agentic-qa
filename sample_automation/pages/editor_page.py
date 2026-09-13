from playwright.sync_api import Locator, Page

from sample_automation.data.article_builder import TestArticle
from sample_automation.pages.base_page import BasePage


class EditorPage(BasePage):
    PATH = "/editor"

    def __init__(
        self,
        page: Page,
        base_url: str,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
        )

        self.title_input = page.get_by_placeholder("Article Title")

        self.description_input = page.get_by_placeholder("What's this article about?")

        self.body_input = page.get_by_placeholder("Write your article (in markdown)")

        self.tag_input = page.get_by_placeholder("Enter tags")

        self.publish_button = page.get_by_role(
            "button",
            name="Publish Article",
        )

    def open_new(self) -> None:
        self.open_path(self.PATH)

    def open_for_edit(
        self,
        slug: str,
    ) -> None:
        self.open_path(f"/editor/{slug}")

    def fill_article_form(
        self,
        article: TestArticle,
    ) -> None:
        self.title_input.fill(article.title)

        self.description_input.fill(article.description)

        self.body_input.fill(article.body)

        self._fill_tags(article.tags)

    def publish(self) -> None:
        self.publish_button.click()

    def create_article(
        self,
        article: TestArticle,
    ) -> None:
        self.fill_article_form(article)
        self.publish()

    def article_title_input(self) -> Locator:
        return self.title_input

    def article_description_input(
        self,
    ) -> Locator:
        return self.description_input

    def article_body_input(self) -> Locator:
        return self.body_input

    def _fill_tags(
        self,
        tags: list[str],
    ) -> None:
        for tag in tags:
            self.tag_input.fill(tag)
            self.tag_input.press("Enter")
