from playwright.sync_api import expect

from sample_automation.data.article_builder import CreatedArticle
from sample_automation.data.comment_builder import CreatedComment
from sample_automation.data.user_builder import UserData
from sample_automation.pages.article_page import ArticlePage


def test_user_can_view_existing_comment(
    api_authenticated_user: UserData,
    article_page: ArticlePage,
    existing_article: CreatedArticle,
    existing_comment: CreatedComment,
) -> None:
    # Arrange / Act
    article_page.open(existing_article.slug)

    comment = article_page.comment_by_text(existing_comment.body)

    # Assert
    expect(comment.root).to_have_count(1)

    expect(comment.body).to_have_text(existing_comment.body)

    expect(comment.author_link(existing_comment.author_username)).to_be_visible()
