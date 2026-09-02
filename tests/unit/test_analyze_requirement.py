from agentic_qa.graph.nodes import create_analyze_requirement_node
from tests.unit.fakes import FakeRequirementAnalyzer


def test_analyze_requirement_adds_analysis_to_state() -> None:
    analyzer = FakeRequirementAnalyzer()

    node = create_analyze_requirement_node(analyzer)

    result = node({"requirement": ("User should be able to delete an existing component.")})

    analysis = result["requirement_analysis"]

    assert analysis.feature == "components"
    assert analysis.operation == "delete"
    assert analysis.needs_ui_exploration is True
