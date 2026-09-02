from agentic_qa.models import RequirementAnalysis


class FakeRequirementAnalyzer:
    def analyze(
        self,
        requirement: str,
    ) -> RequirementAnalysis:
        return RequirementAnalysis(
            feature="components",
            operation="delete",
            objective=("Verify that an existing component can be deleted."),
            needs_ui_exploration=True,
        )
