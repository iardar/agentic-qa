from playwright.sync_api import APIRequestContext

from sample_automation.data.article_builder import CreatedArticle


def test_existing_article_fixture_creates_article(
    existing_article: CreatedArticle,
    realworld_api_context: APIRequestContext,
    registered_user_token: str,
) -> None:
    response = realworld_api_context.get(
        f"/api/articles/{existing_article.slug}",
        headers={"Authorization": (f"Token {registered_user_token}")},
    )

    assert response.status == 200

    payload = response.json()
    article = payload["article"]

    assert article["slug"] == existing_article.slug
    assert article["title"] == existing_article.title
    assert article["description"] == (existing_article.description)
    assert article["body"] == existing_article.body
