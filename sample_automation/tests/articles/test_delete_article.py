from playwright.sync_api import expect

from sample_automation.api.realworld_client import (
    RealWorldApiClient,
)
from sample_automation.data.article_builder import (
    CreatedArticle,
)
from sample_automation.data.user_builder import UserData
from sample_automation.pages.article_page import ArticlePage


def test_user_can_delete_article(
    api_authenticated_user: UserData,
    existing_article: CreatedArticle,
    registered_user_token: str,
    realworld_api_client: RealWorldApiClient,
    article_page: ArticlePage,
) -> None:
    article_page.open(existing_article.slug)

    expect(
        article_page.navigation.user_profile_link(
            api_authenticated_user.username
        )
    ).to_be_visible()

    expect(
        article_page.title(
            existing_article.title
        )
    ).to_be_visible()

    assert realworld_api_client.article_exists(
        token=registered_user_token,
        slug=existing_article.slug,
    )

    article_page.delete_article()

    assert not realworld_api_client.article_exists(
        token=registered_user_token,
        slug=existing_article.slug,
    )