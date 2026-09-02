from typing import Protocol

from agentic_qa.models import RequirementAnalysis


class RequirementAnalyzer(Protocol):
    def analyze(
        self,
        requirement: str,
    ) -> RequirementAnalysis:
        """Analyze an unstructured QA requirement."""
        ...
