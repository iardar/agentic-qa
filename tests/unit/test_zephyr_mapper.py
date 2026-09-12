from agentic_qa.integrations.zephyr.mapper import (
    map_zephyr_test_case,
    map_zephyr_test_cases,
)
from agentic_qa.integrations.zephyr.models import (
    ZephyrTestCase,
    ZephyrTestStep,
)
from agentic_qa.test_cases.models import TestCaseSource


def test_mapper_maps_zephyr_test_case_to_qa_test_case() -> None:
    zephyr_case = ZephyrTestCase(
        key="P10020416-T373",
        name="TP-TASK-001",
        status="Draft",
        precondition="User is on TP home page.",
        objective="Validate that the user can create a checklist",
        folder="/Training Portal/Plan",
        priority="Normal",
        labels=[
            "Checklist",
            "E2E",
            "TP",
            "Automation",
        ],
        owner="JIRAUSER94235",
        steps=[
            ZephyrTestStep(
                sequence=1,
                action="Open Training Plans",
                test_data="N/A",
                expected_result="Training Plans page is opened",
            ),
            ZephyrTestStep(
                sequence=2,
                action="Click Create New Plan",
                test_data="test data : Plan",
                expected_result="Create New Plan modal is opened",
            ),
        ],
    )

    qa_case = map_zephyr_test_case(zephyr_case)

    assert qa_case.id == "zephyr:P10020416-T373"

    assert qa_case.source.system == TestCaseSource.ZEPHYR
    assert qa_case.source.external_id == "P10020416-T373"

    assert qa_case.title == "TP-TASK-001"
    assert qa_case.status == "Draft"
    assert qa_case.priority == "Normal"

    assert qa_case.preconditions == [
        "User is on TP home page.",
    ]

    assert qa_case.labels == [
        "Checklist",
        "E2E",
        "TP",
        "Automation",
    ]

    assert len(qa_case.steps) == 2

    assert qa_case.steps[0].sequence == 1
    assert qa_case.steps[0].action == "Open Training Plans"
    assert qa_case.steps[0].test_data == "N/A"

    assert qa_case.steps[1].sequence == 2
    assert qa_case.steps[1].test_data == "test data : Plan"


def test_mapper_maps_missing_precondition_to_empty_list() -> None:
    zephyr_case = ZephyrTestCase(
        key="TEST-T1",
        name="Create task",
        precondition=None,
    )

    qa_case = map_zephyr_test_case(zephyr_case)

    assert qa_case.preconditions == []


def test_mapper_maps_multiple_test_cases() -> None:
    zephyr_cases = [
        ZephyrTestCase(
            key="TEST-T1",
            name="Create task",
        ),
        ZephyrTestCase(
            key="TEST-T2",
            name="Delete task",
        ),
    ]

    qa_cases = map_zephyr_test_cases(zephyr_cases)

    assert len(qa_cases) == 2

    assert qa_cases[0].id == "zephyr:TEST-T1"
    assert qa_cases[1].id == "zephyr:TEST-T2"


def test_mapper_preserves_test_data_placeholder() -> None:
    zephyr_case = ZephyrTestCase(
        key="TEST-T1",
        name="Create task",
        steps=[
            ZephyrTestStep(
                sequence=1,
                action="Fill Team",
                test_data="test data : Team",
            ),
        ],
    )

    qa_case = map_zephyr_test_case(zephyr_case)

    assert qa_case.steps[0].test_data == "test data : Team"
