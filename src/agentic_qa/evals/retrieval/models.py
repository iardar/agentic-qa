from pydantic import BaseModel, Field

from agentic_qa.models import RequirementAnalysis


class RetrievalEvaluationCase(BaseModel):
    name: str
    analysis: RequirementAnalysis
    required_paths: list[str] = Field(default_factory=list)
