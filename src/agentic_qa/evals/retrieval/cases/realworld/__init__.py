from agentic_qa.evals.retrieval.cases.realworld.articles import (
    ARTICLE_CASES,
)
from agentic_qa.evals.retrieval.cases.realworld.auth import (
    AUTH_CASES,
)
from agentic_qa.evals.retrieval.cases.realworld.comments import (
    COMMENT_CASES,
)
from agentic_qa.evals.retrieval.cases.realworld.feeds import (
    FEED_CASES,
)

REAL_WORLD_CASES = [
    *AUTH_CASES,
    *ARTICLE_CASES,
    *COMMENT_CASES,
    *FEED_CASES,
]

__all__ = [
    "ARTICLE_CASES",
    "AUTH_CASES",
    "COMMENT_CASES",
    "FEED_CASES",
    "REAL_WORLD_CASES",
]
