from typing import Any, Protocol

import langsmith as ls

from agentic_qa.graph.state import QAState
from agentic_qa.models import (
    ExecutionStatus,
    InteractionSurface,
    RequirementAnalysis,
    ResultAnalysis,
    TestDesign,
    TestExecutionResult,
)
from agentic_qa.requirements.analyzer import RequirementAnalyzer
from agentic_qa.retrieval.models import RepositoryContext
from agentic_qa.retrieval.provider import RepositoryContextProvider


class QANode(Protocol):
    def __call__(
        self,
        state: QAState,
    ) -> Any: ...


def create_analyze_requirement_node(
    analyzer: RequirementAnalyzer,
) -> QANode:
    def analyze_requirement(
        state: QAState,
    ) -> dict[str, RequirementAnalysis]:
        analysis = analyzer.analyze(state["requirement"])

        return {
            "requirement_analysis": analysis,
        }

    return analyze_requirement


def create_retrieve_context_node(
    provider: RepositoryContextProvider,
) -> QANode:
    def retrieve_context(
        state: QAState,
    ) -> dict[str, RepositoryContext]:
        analysis = state["requirement_analysis"]

        with ls.trace(
            "keyword_repository_retrieval",
            "chain",
            inputs={
                "requirement_analysis": (analysis.model_dump(mode="json")),
            },
        ) as run:
            context = provider.retrieve(analysis)

            run.end(
                outputs={
                    "query_terms": context.query_terms,
                    "items": [item.model_dump(mode="json") for item in context.items],
                }
            )

        return {
            "repository_context": context,
        }

    return retrieve_context


def explore_ui(
    state: QAState,
) -> dict[str, list[str]]:
    analysis = state["requirement_analysis"]

    if analysis.interaction_surface != InteractionSurface.UI:
        return {
            "exploration_findings": [],
        }

    return {
        "exploration_findings": [
            "UI exploration is not connected yet.",
        ],
    }


def design_test(
    state: QAState,
) -> dict[str, TestDesign]:
    analysis = state["requirement_analysis"]

    design = TestDesign(
        title=analysis.objective,
        objective=analysis.objective,
        preconditions=[],
        test_data=[],
        steps=[
            "Prepare required test state.",
            "Perform the user action.",
            "Verify the expected behavior.",
        ],
        expected_results=[
            "The requirement is satisfied.",
        ],
    )

    return {
        "test_design": design,
    }


def generate_test(
    state: QAState,
) -> dict[str, str]:
    design = state["test_design"]

    generated_code = f'''\
def test_generated_scenario():
    """
    {design.title}
    """

    # Test generation is not connected yet.
    raise NotImplementedError
'''

    return {
        "generated_code": generated_code,
    }


def run_test(
    state: QAState,
) -> dict[str, TestExecutionResult]:
    _ = state["generated_code"]

    result = TestExecutionResult(
        status=ExecutionStatus.NOT_RUN,
        output="pytest runner is not connected yet.",
    )

    return {
        "execution_result": result,
    }


def analyze_result(
    state: QAState,
) -> dict[str, ResultAnalysis]:
    execution = state["execution_result"]

    analysis = ResultAnalysis(
        summary=f"Execution status: {execution.status}",
        classification="not_executed",
    )

    return {
        "result_analysis": analysis,
    }
