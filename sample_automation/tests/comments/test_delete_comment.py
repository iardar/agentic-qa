
from playwright.sync_api import Page, expect

from sample_automation.api.realworld_client import RealWorldApiClient
from sample_automation.data.article_builder import CreatedArticle
from sample_automation.data.comment_builder import CreatedComment
from sample_automation.data.user_builder import UserData
from sample_automation.pages.article_page import ArticlePage


def test_user_can_delete_own_comment(
    api_authenticated_user: UserData,
    page: Page,
    article_page: ArticlePage,
    realworld_api_client: RealWorldApiClient,
    registered_user_token: str,
    existing_article: CreatedArticle,
    existing_comment: CreatedComment,
) -> None:
    # Arrange
    article_page.open(existing_article.slug)

    comment = article_page.comment_by_text(
        existing_comment.body
    )

    expect(comment.root).to_have_count(1)
    expect(comment.delete_button).to_be_visible()

    # Act
    with page.expect_response(
        lambda response: (
            response.request.method == "DELETE"
            and response.url.split("?")[0].endswith(
                f"/articles/{existing_article.slug}"
                f"/comments/{existing_comment.id}"
            )
        )
    ) as response_info:
        comment.delete()

    response = response_info.value
    assert response.status == 204

    # Assert: UI
    expect(comment.root).to_have_count(0)

    # Assert: backend
    remaining_comments = realworld_api_client.get_comments(
        token=registered_user_token,
        slug=existing_article.slug,
    )

    assert all(
        item.id != existing_comment.id
        for item in remaining_comments
    )
