from typing import Required, TypedDict

from agentic_qa.models import (
    RequirementAnalysis,
    ResultAnalysis,
    TestDesign,
    TestExecutionResult,
)
from agentic_qa.retrieval.models import RepositoryContext


class QAState(TypedDict, total=False):
    requirement: Required[str]

    requirement_analysis: RequirementAnalysis

    repository_context: RepositoryContext

    exploration_findings: list[str]

    test_design: TestDesign

    generated_code: str

    execution_result: TestExecutionResult

    result_analysis: ResultAnalysis
