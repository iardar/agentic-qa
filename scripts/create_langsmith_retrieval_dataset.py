from dotenv import load_dotenv
from langsmith import Client

from agentic_qa.evals.retrieval.cases import REAL_WORLD_CASES

load_dotenv()
DATASET_NAME = "repository-retrieval-realworld-v2"
EXPECTED_CASE_COUNT = 10


def main() -> None:
    if len(REAL_WORLD_CASES) != EXPECTED_CASE_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_CASE_COUNT} retrieval cases, found {len(REAL_WORLD_CASES)}."
        )

    client = Client()

    if client.has_dataset(dataset_name=DATASET_NAME):
        dataset = client.read_dataset(dataset_name=DATASET_NAME)

        print(f"Dataset '{DATASET_NAME}' already exists.")
    else:
        dataset = client.create_dataset(
            dataset_name=DATASET_NAME,
            description=(
                "RealWorld repository retrieval benchmark v2:"
                "authentication, articles, and comments."
            ),
            metadata={
                "component": "repository_retrieval",
                "dataset_version": "v2",
                "case_count": EXPECTED_CASE_COUNT,
            },
        )

        print(f"Created dataset '{DATASET_NAME}'.")

    existing_examples = client.list_examples(dataset_id=dataset.id)

    existing_case_names = {
        example.metadata.get("case_name") for example in existing_examples if example.metadata
    }

    new_examples = []

    for case in REAL_WORLD_CASES:
        if case.name in existing_case_names:
            continue

        new_examples.append(
            {
                "inputs": {
                    "analysis": (case.analysis.model_dump(mode="json")),
                },
                "outputs": {
                    "required_paths": (case.required_paths),
                },
                "metadata": {
                    "case_name": case.name,
                },
            }
        )

    if not new_examples:
        print("Dataset is already synchronized.")
        return

    client.create_examples(
        dataset_id=dataset.id,
        examples=new_examples,
    )

    print(f"Added {len(new_examples)} new example(s) to '{DATASET_NAME}'.")


if __name__ == "__main__":
    main()
