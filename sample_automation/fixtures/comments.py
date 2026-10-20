from collections.abc import Iterator

import pytest

from sample_automation.api.realworld_client import RealWorldApiClient
from sample_automation.data.article_builder import CreatedArticle
from sample_automation.data.comment_builder import (
    CreatedComment,
    build_unique_comment,
)


@pytest.fixture
def existing_comment(
    realworld_api_client: RealWorldApiClient,
    registered_user_token: str,
    existing_article: CreatedArticle,
) -> Iterator[CreatedComment]:
    """Create an article comment and clean it up after the test."""

    comment_data = build_unique_comment()

    created_comment = realworld_api_client.create_comment(
        token=registered_user_token,
        slug=existing_article.slug,
        comment=comment_data,
    )

    yield created_comment

    realworld_api_client.delete_comment(
        token=registered_user_token,
        slug=existing_article.slug,
        comment_id=created_comment.id,
        allow_missing=True,
    )
