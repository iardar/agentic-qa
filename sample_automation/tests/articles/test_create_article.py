from playwright.sync_api import expect

from sample_automation.data.article_builder import (
    TestArticle,
)
from sample_automation.data.user_builder import (
    TestUser,
)
from sample_automation.pages.article_page import (
    ArticlePage,
)
from sample_automation.pages.editor_page import (
    EditorPage,
)


def test_user_can_create_article(
    authenticated_user: TestUser,
    editor_page: EditorPage,
    article_page: ArticlePage,
    new_article: TestArticle,
) -> None:
    editor_page.open_new()

    editor_page.create_article(
        new_article
    )

    expect(
        article_page.title(
            new_article.title
        )
    ).to_be_visible()

    expect(
        article_page.body()
    ).to_contain_text(
        new_article.body
    )