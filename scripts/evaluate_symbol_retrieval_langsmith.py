from typing import Any

from dotenv import load_dotenv
from langsmith import Client

from agentic_qa.config import settings
from agentic_qa.evals.retrieval.evaluator import (
    calculate_retrieval_metrics,
)
from agentic_qa.models import RequirementAnalysis
from agentic_qa.retrieval.models import RepositoryContext
from agentic_qa.retrieval.symbols.indexer import (
    PythonAstSymbolIndexer,
)
from agentic_qa.retrieval.symbols.projection import (
    project_symbols_to_repository_context,
)
from agentic_qa.retrieval.symbols.provider import (
    SymbolRepositoryContextProvider,
)

load_dotenv()

DATASET_NAME = "repository-retrieval-realworld-v1"

TOP_K_SYMBOLS = 50
TOP_K_FILES = 8


symbol_index = PythonAstSymbolIndexer(
    repository_path=settings.target_repository,
).build_index()

provider = SymbolRepositoryContextProvider(
    symbol_index=symbol_index,
    top_k_symbols=TOP_K_SYMBOLS,
)


def target(
    inputs: dict[str, Any],
) -> dict[str, Any]:
    analysis = RequirementAnalysis.model_validate(
        inputs["analysis"]
    )

    symbol_context = provider.retrieve(analysis)

    context = project_symbols_to_repository_context(
        symbol_context,
        top_k=TOP_K_FILES,
    )

    return {
        "repository_context": context.model_dump(
            mode="json"
        )
    }


def retrieval_evaluator(
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> dict[str, Any]:
    context = RepositoryContext.model_validate(
        outputs["repository_context"]
    )

    metrics = calculate_retrieval_metrics(
        context=context,
        required_paths=reference_outputs[
            "required_paths"
        ],
    )

    return {
        "results": [
            {
                "key": "top1_relevant",
                "score": metrics.top1_relevant,
            },
            {
                "key": "precision_at_3",
                "score": metrics.precision_at_3,
            },
            {
                "key": "recall_at_3",
                "score": metrics.recall_at_3,
            },
            {
                "key": "recall_at_5",
                "score": metrics.recall_at_5,
            },
        ]
    }


def main() -> None:
    client = Client()

    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            retrieval_evaluator,
        ],
        experiment_prefix=(
            "realworld-retrieval-v2.0-symbol-token-aware"
        ),
        metadata={
            "retriever": "symbol",
            "retrieval_version": "v2.0",
            "retrieval_unit": "symbol",
            "projection": "unique_paths",
            "top_k_symbols": TOP_K_SYMBOLS,
            "top_k_files": TOP_K_FILES,
            "corpus": "realworld",
        },
    )

    print(results)


if __name__ == "__main__":
    main()