from agentic_qa.graph.workflow import build_workflow
from agentic_qa.models import ExecutionStatus
from agentic_qa.retrieval.models import RepositoryArtifactType
from tests.unit.fakes import FakeRepositoryContextProvider, FakeRequirementAnalyzer


def test_workflow_processes_requirement() -> None:
    analyzer = FakeRequirementAnalyzer()

    workflow = build_workflow(
        requirement_analyzer=analyzer,
        repository_context_provider=FakeRepositoryContextProvider(),
    )

    result = workflow.invoke(
        {"requirement": ("User should be able to delete an existing component.")}
    )

    repository_context = result["repository_context"]

    assert repository_context.items

    assert repository_context.items[0].artifact_type == RepositoryArtifactType.PAGE_OBJECT


    assert result["requirement_analysis"].feature == "Component management"

    assert result["requirement_analysis"].operation == "Delete an existing component"

    assert "test_design" in result
    assert "generated_code" in result

    assert result["execution_result"].status == ExecutionStatus.NOT_RUN
