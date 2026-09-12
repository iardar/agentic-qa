import csv
from pathlib import Path
from typing import TextIO

from agentic_qa.integrations.zephyr.models import (
    ZephyrCsvRow,
    ZephyrTestCase,
    ZephyrTestStep,
)


class ZephyrCsvImportError(ValueError):
    """Raised when a Zephyr CSV export cannot be reconstructed safely."""


def read_zephyr_csv(path: Path) -> list[ZephyrTestCase]:
    """Read Zephyr Scale CSV export and reconstruct complete test cases."""

    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        return _read_zephyr_csv(csv_file)


def _read_zephyr_csv(csv_file: TextIO) -> list[ZephyrTestCase]:
    reader = csv.DictReader(csv_file)

    test_cases: list[ZephyrTestCase] = []
    current_rows: list[ZephyrCsvRow] = []

    for row_number, raw_row in enumerate(reader, start=2):
        row = ZephyrCsvRow.model_validate(raw_row)

        if row.key.strip():
            if current_rows:
                test_cases.append(_build_test_case(current_rows))

            current_rows = [row]
            continue

        if not current_rows:
            raise ZephyrCsvImportError(
                "Encountered a continuation row before a test case "
                f"at CSV row {row_number}."
            )

        current_rows.append(row)

    if current_rows:
        test_cases.append(_build_test_case(current_rows))

    return test_cases


def _build_test_case(rows: list[ZephyrCsvRow]) -> ZephyrTestCase:
    first_row = rows[0]

    steps: list[ZephyrTestStep] = []

    for row in rows:
        action = _optional_text(row.step)

        if action is None:
            continue

        steps.append(
            ZephyrTestStep(
                sequence=len(steps) + 1,
                action=action,
                test_data=_optional_text(row.test_data),
                expected_result=_optional_text(row.expected_result),
            )
        )

    return ZephyrTestCase(
        key=first_row.key.strip(),
        name=first_row.name.strip(),
        status=_optional_text(first_row.status),
        precondition=_optional_text(first_row.precondition),
        objective=_optional_text(first_row.objective),
        folder=_optional_text(first_row.folder),
        priority=_optional_text(first_row.priority),
        component=_optional_text(first_row.component),
        labels=_parse_labels(first_row.labels),
        owner=_optional_text(first_row.owner),
        estimated_time=_optional_text(first_row.estimated_time),
        coverage_issues=_optional_text(first_row.coverage_issues),
        coverage_pages=_optional_text(first_row.coverage_pages),
        steps=steps,
        plain_text_script=_optional_text(first_row.plain_text_script),
        bdd_script=_optional_text(first_row.bdd_script),
    )


def _optional_text(value: str) -> str | None:
    stripped = value.strip()
    return stripped or None


def _parse_labels(value: str) -> list[str]:
    return [
        label.strip()
        for label in value.split(",")
        if label.strip()
    ]