from pathlib import Path

from agentic_qa.retrieval.models import (
    RepositoryArtifactType,
    RepositoryContext,
    RetrievedContextItem,
)
from agentic_qa.retrieval.symbols.models import SymbolRetrievalContext


def project_symbols_to_repository_context(
    context: SymbolRetrievalContext,
    top_k: int = 8,
) -> RepositoryContext:
    """Project ranked symbol results to unique ranked repository paths."""

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    seen_paths: set[str] = set()
    items: list[RetrievedContextItem] = []

    for retrieved_symbol in context.items:
        symbol = retrieved_symbol.symbol

        if symbol.path in seen_paths:
            continue

        seen_paths.add(symbol.path)

        items.append(
            RetrievedContextItem(
                path=symbol.path,
                artifact_type=_classify_path(Path(symbol.path)),
                score=retrieved_symbol.score,
                matched_terms=retrieved_symbol.matched_terms,
                snippet=symbol.source,
            )
        )

        if len(items) == top_k:
            break

    return RepositoryContext(
        query_terms=context.query_terms,
        items=items,
    )


def _classify_path(
    path: Path,
) -> RepositoryArtifactType:
    """Classify projected paths using the same conventions as V1.2."""

    if path.name == "conftest.py" or "fixtures" in path.parts:
        return RepositoryArtifactType.FIXTURE

    if "tests" in path.parts and path.name.startswith("test_"):
        return RepositoryArtifactType.TEST

    if "pages" in path.parts:
        return RepositoryArtifactType.PAGE_OBJECT

    if "components" in path.parts:
        return RepositoryArtifactType.COMPONENT

    if "data" in path.parts:
        return RepositoryArtifactType.TEST_DATA

    return RepositoryArtifactType.OTHER