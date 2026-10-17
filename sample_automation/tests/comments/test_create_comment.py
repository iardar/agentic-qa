from playwright.sync_api import Page, expect

from sample_automation.api.realworld_client import RealWorldApiClient
from sample_automation.data.article_builder import CreatedArticle
from sample_automation.data.comment_builder import build_unique_comment
from sample_automation.data.user_builder import UserData
from sample_automation.pages.article_page import ArticlePage


def test_user_can_create_comment(
    api_authenticated_user: UserData,
    page: Page,
    article_page: ArticlePage,
    existing_article: CreatedArticle,
    registered_user_token: str,
    realworld_api_client: RealWorldApiClient,
) -> None:
    comment_data = build_unique_comment()

    try:
        # Arrange
        article_page.open(existing_article.slug)

        # Act
        with page.expect_response(
            lambda response: (
                response.request.method == "POST"
                and response.url.split("?")[0].endswith(
                    f"/articles/{existing_article.slug}/comments"
                )
            )
        ) as response_info:
            article_page.add_comment(comment_data.body)

        response = response_info.value
        assert response.status == 201

        # Assert: UI
        comment = article_page.comment_by_text(comment_data.body)

        expect(comment.root).to_have_count(1)
        expect(comment.body).to_have_text(comment_data.body)

        # Assert: backend
        comments = realworld_api_client.get_comments(
            token=registered_user_token,
            slug=existing_article.slug,
        )

        created_comment = next(
            (item for item in comments if item.body == comment_data.body),
            None,
        )

        assert created_comment is not None
        assert created_comment.id > 0

        expect(comment.author_link(created_comment.author_username)).to_be_visible()

    finally:
        # Cleanup even if UI assertions fail.
        comments = realworld_api_client.get_comments(
            token=registered_user_token,
            slug=existing_article.slug,
        )

        for item in comments:
            if item.body == comment_data.body:
                realworld_api_client.delete_comment(
                    token=registered_user_token,
                    slug=existing_article.slug,
                    comment_id=item.id,
                    allow_missing=True,
                )
