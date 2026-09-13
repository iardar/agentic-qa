from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class TestArticle:
    title: str
    description: str
    body: str
    tags: list[str]


@dataclass(frozen=True)
class CreatedArticle:
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]


def build_unique_article() -> TestArticle:
    suffix = uuid4().hex[:10]

    return TestArticle(
        title=f"Agentic QA Article {suffix}",
        description=(
            f"Article description {suffix}"
        ),
        body=(
            "Article body created by the "
            "Agentic QA automation framework."
        ),
        tags=[
            "agentic-qa",
            f"test-{suffix}",
        ],
    )


def build_article_update(
    title: str,
) -> TestArticle:
    suffix = uuid4().hex[:10]

    return TestArticle(
        title=title,
        description=(
            f"Updated article description {suffix}"
        ),
        body=(
            "Updated article body created by the "
            "Agentic QA automation framework."
        ),
        tags=[
            "agentic-qa",
            "updated",
        ],
    )