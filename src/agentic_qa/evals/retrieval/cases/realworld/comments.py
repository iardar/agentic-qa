from agentic_qa.evals.retrieval.models import RetrievalEvaluationCase
from agentic_qa.models import InteractionSurface, RequirementAnalysis

COMMENT_CASES = [
    RetrievalEvaluationCase(
        name="realworld_create_comment",
        analysis=RequirementAnalysis(
            feature="Article comments",
            operation="Create comment",
            objective=(
                "Verify that an authenticated user can add a comment to an existing article."
            ),
            actors=["Authenticated user"],
            conditions=[
                "The user is authenticated.",
                "An existing article is available.",
                "The user has unique valid comment text.",
            ],
            expected_outcomes=[
                "The comment is submitted through the UI.",
                "The new comment body is visible.",
                "The correct comment author is visible.",
                "The comment is persisted in the backend.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/comments/test_create_comment.py",
            "pages/article_page.py",
            "components/comment.py",
            "fixtures/articles.py",
            "data/comment_builder.py",
            "api/realworld_client.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="realworld_read_comment",
        analysis=RequirementAnalysis(
            feature="Article comments",
            operation="View existing comment",
            objective=(
                "Verify that a previously created comment "
                "is displayed when a user opens its article."
            ),
            actors=["Authenticated user"],
            conditions=[
                "The user is authenticated.",
                "An existing article is available.",
                "An existing comment belongs to the article.",
            ],
            expected_outcomes=[
                "The existing comment is visible.",
                "The comment body is displayed correctly.",
                "The correct comment author is displayed.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/comments/test_read_comment.py",
            "pages/article_page.py",
            "components/comment.py",
            "fixtures/comments.py",
            "data/comment_builder.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="realworld_delete_comment",
        analysis=RequirementAnalysis(
            feature="Article comments",
            operation="Delete own comment",
            objective=(
                "Verify that an authenticated user can delete their own existing article comment."
            ),
            actors=[
                "Authenticated user",
                "Comment author",
            ],
            conditions=[
                "The user is authenticated.",
                "An existing article is available.",
                "An existing comment is owned by the user.",
            ],
            expected_outcomes=[
                "The user deletes the comment through the UI.",
                "The deleted comment disappears from the page.",
                "The deleted comment is absent from the backend.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/comments/test_delete_comment.py",
            "pages/article_page.py",
            "components/comment.py",
            "fixtures/comments.py",
            "api/realworld_client.py",
            "data/comment_builder.py",
        ],
    ),
]
