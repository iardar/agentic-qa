from agentic_qa.evals.retrieval.evaluator import (
    calculate_retrieval_metrics,
)
from agentic_qa.retrieval.models import (
    RepositoryArtifactType,
    RepositoryContext,
    RetrievedContextItem,
)


def make_item(
    path: str,
) -> RetrievedContextItem:
    return RetrievedContextItem(
        path=path,
        artifact_type=(
            RepositoryArtifactType.OTHER
        ),
        score=1.0,
        matched_terms=[],
        snippet="",
    )


def test_calculates_retrieval_metrics() -> None:
    context = RepositoryContext(
        query_terms=[],
        items=[
            make_item("a.py"),
            make_item("unrelated.py"),
            make_item("b.py"),
            make_item("c.py"),
        ],
    )

    metrics = calculate_retrieval_metrics(
        context=context,
        required_paths=[
            "a.py",
            "b.py",
            "c.py",
        ],
    )

    assert metrics.top1_relevant is True

    assert metrics.precision_at_3 == (
        2 / 3
    )

    assert metrics.recall_at_3 == (
        2 / 3
    )

    assert metrics.recall_at_5 == 1.0