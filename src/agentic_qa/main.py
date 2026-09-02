import argparse
import json
from typing import Any

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from agentic_qa.config import settings
from agentic_qa.graph.workflow import build_workflow
from agentic_qa.requirements.llm_analyzer import LLMRequirementAnalyzer


def serialize(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")

    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def create_workflow():
    if settings.openai_api_key is None:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    if not settings.llm_model:
        raise RuntimeError("LLM_MODEL is not configured.")

    model = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key.get_secret_value(),
    )

    requirement_analyzer = LLMRequirementAnalyzer(model=model)

    return build_workflow(requirement_analyzer=requirement_analyzer)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agentic QA workflow",
    )

    parser.add_argument(
        "requirement",
        help="Test requirement to process",
    )

    args = parser.parse_args()

    workflow = create_workflow()

    result = workflow.invoke(
        {
            "requirement": args.requirement,
        }
    )

    print(
        json.dumps(
            result,
            indent=2,
            default=serialize,
        )
    )


if __name__ == "__main__":
    main()
