from typing import Protocol

from agentic_qa.models import RequirementAnalysis
from agentic_qa.retrieval.models import RepositoryContext


class RepositoryContextProvider(Protocol):
    def retrieve(
        self,
        analysis: RequirementAnalysis,
    ) -> RepositoryContext:
        """Retrieve repository context relevant to a requirement."""
        ...
