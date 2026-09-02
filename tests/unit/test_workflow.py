from agentic_qa.graph.workflow import build_workflow
from agentic_qa.models import ExecutionStatus
from tests.unit.fakes import FakeRequirementAnalyzer


def test_workflow_processes_requirement() -> None:
    analyzer = FakeRequirementAnalyzer()

    workflow = build_workflow(requirement_analyzer=analyzer)

    result = workflow.invoke(
        {"requirement": ("User should be able to delete an existing component.")}
    )

    assert result["requirement_analysis"].feature == "components"

    assert result["requirement_analysis"].operation == "delete"

    assert "test_design" in result
    assert "generated_code" in result

    assert result["execution_result"].status == ExecutionStatus.NOT_RUN
