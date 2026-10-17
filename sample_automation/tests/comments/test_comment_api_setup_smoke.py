from sample_automation.api.realworld_client import RealWorldApiClient
from sample_automation.data.article_builder import CreatedArticle
from sample_automation.data.comment_builder import build_unique_comment


def test_comment_api_lifecycle(
    realworld_api_client: RealWorldApiClient,
    registered_user_token: str,
    existing_article: CreatedArticle,
) -> None:
    """Verify that API comment setup and cleanup work correctly."""

    comment_data = build_unique_comment()
    created_comment = None

    try:
        # CREATE
        created_comment = realworld_api_client.create_comment(
            token=registered_user_token,
            slug=existing_article.slug,
            comment=comment_data,
        )

        assert created_comment.id > 0
        assert created_comment.body == comment_data.body

        # READ
        comments = realworld_api_client.get_comments(
            token=registered_user_token,
            slug=existing_article.slug,
        )

        assert any(
            comment.id == created_comment.id
            and comment.body == comment_data.body
            for comment in comments
        )

        # DELETE
        realworld_api_client.delete_comment(
            token=registered_user_token,
            slug=existing_article.slug,
            comment_id=created_comment.id,
        )

        # VERIFY DELETION
        remaining_comments = realworld_api_client.get_comments(
            token=registered_user_token,
            slug=existing_article.slug,
        )

        assert all(
            comment.id != created_comment.id
            for comment in remaining_comments
        )

    finally:
        # Cleanup even when an assertion fails after creation.
        if created_comment is not None:
            realworld_api_client.delete_comment(
                token=registered_user_token,
                slug=existing_article.slug,
                comment_id=created_comment.id,
                allow_missing=True,
            )