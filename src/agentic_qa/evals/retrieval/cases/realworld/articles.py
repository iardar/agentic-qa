

from agentic_qa.evals.retrieval.models import RetrievalEvaluationCase
from agentic_qa.models import (
    InteractionSurface,
    RequirementAnalysis,
)

ARTICLE_CASES: list[RetrievalEvaluationCase] = []


ARTICLE_CASES = [
    RetrievalEvaluationCase(
        name="realworld_create_article",
        analysis=RequirementAnalysis(
            feature="Article management",
            operation="Create article",
            objective=(
                "Verify that an authenticated user can create "
                "and publish a new article."
            ),
            actors=[
                "Authenticated user",
            ],
            conditions=[
                "The user is authenticated.",
                "The user has valid article title, description, body, and tags.",
                "The user is on the new article editor.",
            ],
            expected_outcomes=[
                "The article is published successfully.",
                "The published article title is visible.",
                "The published article body is visible.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/articles/test_create_article.py",
            "pages/editor_page.py",
            "pages/article_page.py",
            "fixtures/articles.py",
            "data/article_builder.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="realworld_edit_article",
        analysis=RequirementAnalysis(
            feature="Article management",
            operation="Edit article",
            objective=(
                "Verify that an authenticated user can edit "
                "an existing article."
            ),
            actors=[
                "Authenticated user",
                "Article author",
            ],
            conditions=[
                "The user is authenticated.",
                "An existing article owned by the user is available.",
                "The user opens the existing article.",
            ],
            expected_outcomes=[
                "The editor loads the existing article values.",
                "The article can be updated successfully.",
                "The updated article body is visible after publishing.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/articles/test_edit_article.py",
            "pages/article_page.py",
            "pages/editor_page.py",
            "fixtures/articles.py",
            "data/article_builder.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="realworld_delete_article",
        analysis=RequirementAnalysis(
            feature="Article management",
            operation="Delete article",
            objective=(
                "Verify that an authenticated article author "
                "can delete an existing article."
            ),
            actors=[
                "Authenticated user",
                "Article author",
            ],
            conditions=[
                "The user is authenticated.",
                "An existing article owned by the user is available.",
                "The user opens the existing article.",
            ],
            expected_outcomes=[
                "The article is deleted through the user interface.",
                "The deleted article no longer exists.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/articles/test_delete_article.py",
            "pages/article_page.py",
            "fixtures/articles.py",
            "api/realworld_client.py",
            "data/article_builder.py",
        ],
    ),
]