from playwright.sync_api import expect

from sample_automation.data.article_builder import (
    ArticleData,
    CreatedArticle,
)
from sample_automation.data.user_builder import UserData
from sample_automation.pages.article_page import ArticlePage
from sample_automation.pages.editor_page import EditorPage


def test_user_can_edit_article(
    api_authenticated_user: UserData,
    existing_article: CreatedArticle,
    article_update: ArticleData,
    article_page: ArticlePage,
    editor_page: EditorPage,
) -> None:
    article_page.open(existing_article.slug)

    # Verify that authenticated state survived navigation.
    expect(
        article_page.navigation.user_profile_link(
            api_authenticated_user.username
        )
    ).to_be_visible()

    # Verify the API-created prerequisite is visible through UI.
    expect(
        article_page.title(existing_article.title)
    ).to_be_visible()

    article_page.edit_article()

    # Verify edit mode loads the existing article.
    expect(
        editor_page.article_title_input()
    ).to_have_value(existing_article.title)

    expect(
        editor_page.article_description_input()
    ).to_have_value(existing_article.description)

    expect(
        editor_page.article_body_input()
    ).to_have_value(existing_article.body)

    # Exercise the behavior under test.
    editor_page.fill_article_form(
        article_update
    )

    editor_page.publish()

    # Verify persisted result.
    expect(
        article_page.title(article_update.title)
    ).to_be_visible()

    expect(
        article_page.body()
    ).to_contain_text(
        article_update.body
    )