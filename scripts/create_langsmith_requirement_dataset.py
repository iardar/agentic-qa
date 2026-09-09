from dotenv import load_dotenv
from langsmith import Client

from agentic_qa.evals.requirements.cases import CASES

load_dotenv()
DATASET_NAME = "requirement-analyzer-v1"


def main() -> None:
    client = Client()

    if client.has_dataset(dataset_name=DATASET_NAME):
        print(
            f"Dataset '{DATASET_NAME}' already exists. "
            "Skipping creation."
        )
        return

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "Regression dataset for the Agentic QA "
            "Requirement Analyzer."
        ),
        metadata={
            "component": "requirement_analyzer",
            "version": "v1",
        },
    )

    examples = []

    for case in CASES:
        examples.append(
            {
                "inputs": {
                    "requirement": case.requirement,
                },
                "outputs": {
                    "expected_surface": (
                        case.expected_surface.value
                    ),
                    "required_condition_terms": (
                        case.required_condition_terms
                    ),
                    "required_condition_alternatives": (
                        case.required_condition_alternatives
                    ),
                    "required_outcome_terms": (
                        case.required_outcome_terms
                    ),
                    "required_outcome_alternatives": (
                        case.required_outcome_alternatives
                    ),
                    "require_ambiguities": (
                        case.require_ambiguities
                    ),
                },
                "metadata": {
                    "case_name": case.name,
                },
            }
        )

    client.create_examples(
        dataset_id=dataset.id,
        examples=examples,
    )

    print(
        f"Created dataset '{DATASET_NAME}' "
        f"with {len(examples)} examples."
    )


if __name__ == "__main__":
    main()