from agentic_qa.integrations.zephyr.models import ZephyrTestCase
from agentic_qa.test_cases.models import (
    QATestCase,
    QATestStep,
    SourceReference,
    TestCaseSource,
)


def map_zephyr_test_case(test_case: ZephyrTestCase) -> QATestCase:
    """Map a Zephyr test case into the Agentic QA domain model."""

    return QATestCase(
        id=f"zephyr:{test_case.key}",
        source=SourceReference(
            system=TestCaseSource.ZEPHYR,
            external_id=test_case.key,
        ),
        title=test_case.name,
        objective=test_case.objective,
        preconditions=_map_preconditions(test_case.precondition),
        steps=[
            QATestStep(
                sequence=step.sequence,
                action=step.action,
                test_data=step.test_data,
                expected_result=step.expected_result,
            )
            for step in test_case.steps
        ],
        status=test_case.status,
        priority=test_case.priority,
        labels=list(test_case.labels),
        component=test_case.component,
        folder=test_case.folder,
        owner=test_case.owner,
        estimated_time=test_case.estimated_time,
        plain_text_script=test_case.plain_text_script,
        bdd_script=test_case.bdd_script,
    )


def map_zephyr_test_cases(
    test_cases: list[ZephyrTestCase],
) -> list[QATestCase]:
    """Map multiple Zephyr test cases into Agentic QA domain models."""

    return [map_zephyr_test_case(test_case) for test_case in test_cases]


def _map_preconditions(precondition: str | None) -> list[str]:
    if precondition is None:
        return []

    return [precondition]
