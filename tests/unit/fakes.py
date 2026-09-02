from agentic_qa.models import RequirementAnalysis
from agentic_qa.retrieval.models import (
    RepositoryArtifactType,
    RepositoryContext,
    RetrievedContextItem,
)


from agentic_qa.models import (
    InteractionSurface,
    RequirementAnalysis,
)


class FakeRequirementAnalyzer:
    def analyze(
        self,
        requirement: str,
    ) -> RequirementAnalysis:
        return RequirementAnalysis(
            feature="Component management",
            operation="Delete an existing component",
            objective=(
                "Verify that an existing component can be deleted."
            ),
            actors=[
                "User",
            ],
            conditions=[
                "A component already exists.",
            ],
            expected_outcomes=[
                "The component can be deleted.",
            ],
            ambiguities=[
                "The interaction surface is not specified.",
            ],
            interaction_surface=(
                InteractionSurface.UNKNOWN
            ),
        )
    
class FakeRepositoryContextProvider:
    def retrieve(
        self,
        analysis: RequirementAnalysis,
    ) -> RepositoryContext:
        return RepositoryContext(
            query_terms=[
                "todo",
                "complete",
            ],
            items=[
                RetrievedContextItem(
                    path="pages/todo_page.py",
                    artifact_type=(RepositoryArtifactType.PAGE_OBJECT),
                    score=10.0,
                    matched_terms=[
                        "todo",
                        "complete",
                    ],
                    snippet=("def complete_todo(self, title: str) -> None:"),
                )
            ],
        )
