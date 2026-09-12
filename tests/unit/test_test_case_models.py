import pytest
from pydantic import ValidationError

from agentic_qa.test_cases.models import (
    QATestCase,
    QATestStep,
    SourceReference,
    TestCaseSource,
)


def test_qa_test_case_preserves_source_reference() -> None:
    test_case = QATestCase(
        id="zephyr:P10020416-T373",
        source=SourceReference(
            system=TestCaseSource.ZEPHYR,
            external_id="P10020416-T373",
        ),
        title="TP-TASK-001",
    )

    assert test_case.id == "zephyr:P10020416-T373"
    assert test_case.source.system == TestCaseSource.ZEPHYR
    assert test_case.source.external_id == "P10020416-T373"


def test_qa_test_step_requires_positive_sequence() -> None:
    with pytest.raises(ValidationError):
        QATestStep(
            sequence=0,
            action="Click Save",
        )