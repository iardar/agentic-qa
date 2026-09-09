from typing import Any
from dotenv import load_dotenv
from langsmith import Client

from agentic_qa.config import settings
from agentic_qa.evals.retrieval.evaluator import (
    calculate_retrieval_metrics,
)
from agentic_qa.models import (
    RequirementAnalysis,
)
from agentic_qa.retrieval.keyword_provider import (
    KeywordRepositoryContextProvider,
)
from agentic_qa.retrieval.models import (
    RepositoryContext,
)

load_dotenv()

DATASET_NAME = "repository-retrieval-realworld-v1"


provider = KeywordRepositoryContextProvider(
    repository_path=settings.target_repository,
    top_k=8,
)

def target(
    inputs: dict[str, Any],
) -> dict[str, Any]:
    analysis = RequirementAnalysis.model_validate(
        inputs["analysis"]
    )

    context = provider.retrieve(
        analysis
    )

    return {
        "repository_context": (
            context.model_dump(
                mode="json"
            )
        )
    }

def retrieval_evaluator(
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> list[dict[str, Any]]:
    context = RepositoryContext.model_validate(
        outputs["repository_context"]
    )

    required_paths = reference_outputs[
        "required_paths"
    ]

    metrics = calculate_retrieval_metrics(
        context=context,
        required_paths=required_paths,
    )

    return [
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

def main() -> None:
    client = Client()

    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            retrieval_evaluator,
        ],
        experiment_prefix=(
            "repository-retrieval-realworld-v1"            
        ),
        metadata={
            "retriever": "keyword",
            "retrieval_version": "v1.1",
            "corpus": "realworld",
        },
    )

    print(results)

if __name__ == "__main__":
    main()