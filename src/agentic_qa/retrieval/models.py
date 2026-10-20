from enum import StrEnum

from pydantic import BaseModel, Field


class RepositoryArtifactType(StrEnum):
    TEST = "test"
    PAGE_OBJECT = "page_object"
    COMPONENT = "component"
    FIXTURE = "fixture"
    TEST_DATA = "test_data"
    GUIDELINE = "guideline"
    OTHER = "other"


class RetrievedContextItem(BaseModel):
    path: str

    artifact_type: RepositoryArtifactType

    score: float

    matched_terms: list[str] = Field(default_factory=list)

    snippet: str


class RepositoryContext(BaseModel):
    query_terms: list[str] = Field(default_factory=list)

    items: list[RetrievedContextItem] = Field(default_factory=list)
