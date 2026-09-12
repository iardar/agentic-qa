from io import StringIO

import pytest

from agentic_qa.integrations.zephyr.csv_reader import (
    ZephyrCsvImportError,
    _read_zephyr_csv,
)

CSV_HEADER = (
    "Key,Name,Status,Precondition,Objective,Folder,Priority,"
    "Component,Labels,Owner,Estimated Time,Coverage (Issues),"
    "Coverage (Pages),Test Script (Step-by-Step) - Step,"
    "Test Script (Step-by-Step) - Test Data,"
    "Test Script (Step-by-Step) - Expected Result,"
    "Test Script (Plain Text),Test Script (BDD)\n"
)


def test_reader_groups_multiple_rows_into_one_test_case() -> None:
    csv_text = (
        CSV_HEADER
        + (
            "TEST-T1,Create task,Draft,User is logged in,"
            "Verify task creation,/Tasks,Normal,,E2E,owner1,,,,"
            "Open Tasks,N/A,Tasks page is opened,,\n"
        )
        + (
            ",,,,,,,,,,,,,"
            "Click Create,test data : Task,"
            "Create dialog is opened,,\n"
        )
    )

    test_cases = _read_zephyr_csv(StringIO(csv_text))

    assert len(test_cases) == 1

    test_case = test_cases[0]

    assert test_case.key == "TEST-T1"
    assert test_case.name == "Create task"
    assert test_case.labels == ["E2E"]

    assert len(test_case.steps) == 2

    assert test_case.steps[0].sequence == 1
    assert test_case.steps[0].action == "Open Tasks"
    assert test_case.steps[0].test_data == "N/A"

    assert test_case.steps[1].sequence == 2
    assert test_case.steps[1].action == "Click Create"
    assert test_case.steps[1].test_data == "test data : Task"


def test_reader_starts_new_test_case_when_key_is_present() -> None:
    csv_text = (
        CSV_HEADER
        + (
            "TEST-T1,Create task,Draft,,,/Tasks,Normal,,,,,,,"
            "Create task,N/A,Task is created,,\n"
        )
        + (
            "TEST-T2,Delete task,Draft,,,/Tasks,Normal,,,,,,,"
            "Delete task,N/A,Task is deleted,,\n"
        )
    )

    test_cases = _read_zephyr_csv(StringIO(csv_text))

    assert len(test_cases) == 2
    assert test_cases[0].key == "TEST-T1"
    assert test_cases[1].key == "TEST-T2"


def test_reader_converts_blank_optional_values_to_none() -> None:
    csv_text = (
        CSV_HEADER
        + (
            "TEST-T1,Create task,,,,,,,,,,,,"
            "Click Create,,, ,\n"
        )
    )

    test_cases = _read_zephyr_csv(StringIO(csv_text))

    test_case = test_cases[0]

    assert test_case.status is None
    assert test_case.objective is None
    assert test_case.steps[0].test_data is None
    assert test_case.steps[0].expected_result is None


def test_reader_rejects_continuation_row_without_parent_case() -> None:
    csv_text = (
        CSV_HEADER
        + (
            ",,,,,,,,,,,,,"
            "Click Create,N/A,Dialog opened,,\n"
        )
    )

    with pytest.raises(
        ZephyrCsvImportError,
        match="continuation row before a test case",
    ):
        _read_zephyr_csv(StringIO(csv_text))