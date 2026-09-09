import argparse
import json
from typing import Any

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from agentic_qa.config import settings
from agentic_qa.graph.state import QAState
from agentic_qa.graph.workflow import build_workflow
from agentic_qa.requirements.llm_analyzer import LLMRequirementAnalyzer
from agentic_qa.retrieval.keyword_provider import KeywordRepositoryContextProvider

load_dotenv()

def serialize(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")

    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def create_workflow() -> CompiledStateGraph[
    QAState,
    None,
    QAState,
    QAState,
]:
    if settings.openai_api_key is None:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    if not settings.llm_model:
        raise RuntimeError("LLM_MODEL is not configured.")

    model = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
    )

    requirement_analyzer = LLMRequirementAnalyzer(model=model)
    repository_context_provider = KeywordRepositoryContextProvider(
        repository_path=settings.target_repository, top_k=8
    )

    return build_workflow(
        requirement_analyzer=requirement_analyzer,
        repository_context_provider=(repository_context_provider),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agentic QA workflow",
    )

    parser.add_argument(
        "requirement",
        help="Test requirement to process",
    )

    args = parser.parse_args()

    config: RunnableConfig = {
        "run_name": "agentic_qa_workflow",
        "tags": [
            "dev",
            "retrieval-v1",
        ],
        "metadata": {
            "model": settings.llm_model,
            "retireval_version": "v1-keyword",
            "application": "agentic-qa",
        },
    }

    workflow = create_workflow()

    result = workflow.invoke(
        {
            "requirement": args.requirement,
        },
        confgi=config,
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
