from enum import StrEnum

from pydantic import BaseModel, Field


class SymbolType(StrEnum):
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    TEST = "test"
    FIXTURE = "fixture"


class RepositorySymbol(BaseModel):
    name: str
    qualified_name: str
    symbol_type: SymbolType

    path: str

    parent: str | None = None

    start_line: int
    end_line: int

    source: str

    parameters: list[str] = Field(default_factory=list)

    decorators: list[str] = Field(default_factory=list)

    bases: list[str] = Field(default_factory=list)


class RepositorySymbolIndex(BaseModel):
    symbols: list[RepositorySymbol] = Field(default_factory=list)


class RetrievedSymbol(BaseModel):
    symbol: RepositorySymbol
    score: float

    matched_terms: list[str] = Field(default_factory=list)


class SymbolRetrievalContext(BaseModel):
    query_terms: list[str] = Field(default_factory=list)

    items: list[RetrievedSymbol] = Field(default_factory=list)
