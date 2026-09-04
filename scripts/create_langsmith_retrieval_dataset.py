from langsmith import Client

from agentic_qa.evals.retrieval.cases import (
    CASES,
)


DATASET_NAME = "repository-retrieval-v1"


def main() -> None:
    client = Client()

    if client.has_dataset(
        dataset_name=DATASET_NAME
    ):
        print(
            f"Dataset '{DATASET_NAME}' "
            "already exists."
        )
        return

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "Repository retrieval regression "
            "dataset for Agentic QA."
        ),
        metadata={
            "component": "repository_retrieval",
            "dataset_version": "v1",
        },
    )

    examples = [
        {
            "inputs": {
                "analysis": case.analysis.model_dump(
                    mode="json"
                ),
            },
            "outputs": {
                "required_paths": (
                    case.required_paths
                ),
            },
            "metadata": {
                "case_name": case.name,
            },
        }
        for case in CASES
    ]

    client.create_examples(
        dataset_id=dataset.id,
        examples=examples,
    )

    print(
        f"Created '{DATASET_NAME}' "
        f"with {len(examples)} examples."
    )


if __name__ == "__main__":
    main()