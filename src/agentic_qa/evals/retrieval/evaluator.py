from dataclasses import dataclass

from agentic_qa.retrieval.models import (
    RepositoryContext,
)


@dataclass
class RetrievalMetrics:
    top1_relevant: bool

    precision_at_3: float
    recall_at_3: float
    recall_at_5: float


def calculate_retrieval_metrics(
    context: RepositoryContext,
    required_paths: list[str],
) -> RetrievalMetrics:
    retrieved_paths = [item.path for item in context.items]

    required = set(required_paths)

    return RetrievalMetrics(
        top1_relevant=bool(retrieved_paths and retrieved_paths[0] in required),
        precision_at_3=_precision_at_k(
            retrieved_paths,
            required,
            3,
        ),
        recall_at_3=_recall_at_k(
            retrieved_paths,
            required,
            3,
        ),
        recall_at_5=_recall_at_k(
            retrieved_paths,
            required,
            5,
        ),
    )


def _precision_at_k(
    retrieved_paths: list[str],
    relevant_paths: set[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    top_k = retrieved_paths[:k]

    hits = sum(path in relevant_paths for path in top_k)

    return hits / k


def _recall_at_k(
    retrieved_paths: list[str],
    relevant_paths: set[str],
    k: int,
) -> float:
    if not relevant_paths:
        return 1.0

    top_k = retrieved_paths[:k]

    hits = sum(path in relevant_paths for path in top_k)

    return hits / len(relevant_paths)
