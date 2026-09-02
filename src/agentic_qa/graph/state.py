from typing import Required, TypedDict

from agentic_qa.models import (
    RequirementAnalysis,
    ResultAnalysis,
    TestDesign,
    TestExecutionResult,
)


class QAState(TypedDict, total=False):
    requirement: Required[str]

    requirement_analysis: RequirementAnalysis

    repository_context: list[str]

    exploration_findings: list[str]

    test_design: TestDesign

    generated_code: str

    execution_result: TestExecutionResult

    result_analysis: ResultAnalysis
