from pydantic import BaseModel, ConfigDict, Field


class ZephyrCsvRow(BaseModel):
    """One physical row from a Zephyr Scale CSV export."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )

    key: str = Field(alias="Key")
    name: str = Field(alias="Name")
    status: str = Field(alias="Status")
    precondition: str = Field(alias="Precondition")
    objective: str = Field(alias="Objective")
    folder: str = Field(alias="Folder")
    priority: str = Field(alias="Priority")
    component: str = Field(alias="Component")
    labels: str = Field(alias="Labels")
    owner: str = Field(alias="Owner")
    estimated_time: str = Field(alias="Estimated Time")

    coverage_issues: str = Field(alias="Coverage (Issues)")
    coverage_pages: str = Field(alias="Coverage (Pages)")

    step: str = Field(
        alias="Test Script (Step-by-Step) - Step",
    )
    test_data: str = Field(
        alias="Test Script (Step-by-Step) - Test Data",
    )
    expected_result: str = Field(
        alias="Test Script (Step-by-Step) - Expected Result",
    )

    plain_text_script: str = Field(
        alias="Test Script (Plain Text)",
    )
    bdd_script: str = Field(
        alias="Test Script (BDD)",
    )


class ZephyrTestStep(BaseModel):
    """One normalized step inside a Zephyr test case."""

    model_config = ConfigDict(extra="forbid")

    sequence: int = Field(ge=1)
    action: str = Field(min_length=1)

    test_data: str | None = None
    expected_result: str | None = None


class ZephyrTestCase(BaseModel):
    """A complete Zephyr test case reconstructed from CSV rows."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1)
    name: str = Field(min_length=1)

    status: str | None = None
    precondition: str | None = None
    objective: str | None = None

    folder: str | None = None
    priority: str | None = None
    component: str | None = None

    labels: list[str] = Field(default_factory=list)

    owner: str | None = None
    estimated_time: str | None = None

    coverage_issues: str | None = None
    coverage_pages: str | None = None

    steps: list[ZephyrTestStep] = Field(default_factory=list)

    plain_text_script: str | None = None
    bdd_script: str | None = None
