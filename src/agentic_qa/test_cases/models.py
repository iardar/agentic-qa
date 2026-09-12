from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TestCaseSource(StrEnum):
    ZEPHYR = "zephyr"


class SourceReference(BaseModel):
    """Reference back to the external system that owns the test case."""

    model_config = ConfigDict(extra="forbid")

    system: TestCaseSource
    external_id: str = Field(min_length=1)


class QATestStep(BaseModel):
    """Vendor-neutral representation of one test step."""

    model_config = ConfigDict(extra="forbid")

    sequence: int = Field(ge=1)
    action: str = Field(min_length=1)

    test_data: str | None = None
    expected_result: str | None = None


class QATestCase(BaseModel):
    """Vendor-neutral test case used inside Agentic QA."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    source: SourceReference

    title: str = Field(min_length=1)
    objective: str | None = None

    preconditions: list[str] = Field(default_factory=list)
    steps: list[QATestStep] = Field(default_factory=list)

    status: str | None = None
    priority: str | None = None

    labels: list[str] = Field(default_factory=list)
    component: str | None = None
    folder: str | None = None

    owner: str | None = None
    estimated_time: str | None = None

    requirement_refs: list[str] = Field(default_factory=list)
    documentation_refs: list[str] = Field(default_factory=list)

    plain_text_script: str | None = None
    bdd_script: str | None = None