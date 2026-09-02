from enum import StrEnum

from pydantic import BaseModel, Field


class InteractionSurface(StrEnum):
    UI = "ui"
    API = "api"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class RequirementAnalysis(BaseModel):
    feature: str = Field(description="Business or application feature being tested.")

    operation: str = Field(description="Primary user or system operation being tested.")

    objective: str = Field(
        description="Concise testing objective preserving the requirement intent."
    )

    actors: list[str] = Field(
        default_factory=list,
        description=(
            "Distinct users, roles, external systems, or other entities "
            "that perform or participate in the behavior. "
            "Do not include quantities, concurrency levels, conditions, "
            "or actions in actor names."
        ),
    )
    conditions: list[str] = Field(
        default_factory=list,
        description=(
            "Conditions, triggers, preconditions, or constraints "
            "explicitly stated in the requirement."
        ),
    )

    expected_outcomes: list[str] = Field(
        default_factory=list,
        description=("Observable expected behaviors explicitly stated in the requirement."),
    )

    ambiguities: list[str] = Field(
        default_factory=list,
        description=(
            "Important information that is missing, unclear, or insufficiently specified."
        ),
    )

    interaction_surface: InteractionSurface = Field(
        description=(
            "The explicitly indicated interaction surface. "
            "Use 'unknown' when the requirement does not provide "
            "enough information to determine UI, API, or system."
        )
    )


class TestDesign(BaseModel):
    title: str
    objective: str
    preconditions: list[str] = Field(default_factory=list)
    test_data: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected_results: list[str] = Field(default_factory=list)


class ExecutionStatus(StrEnum):
    NOT_RUN = "not_run"
    PASSED = "passed"
    FAILED = "failed"


class TestExecutionResult(BaseModel):
    status: ExecutionStatus
    exit_code: int | None = None
    output: str = ""


class ResultAnalysis(BaseModel):
    summary: str
    classification: str
