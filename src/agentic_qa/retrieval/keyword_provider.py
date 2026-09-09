import re
from collections.abc import Iterator
from pathlib import Path

from agentic_qa.models import RequirementAnalysis
from agentic_qa.retrieval.models import (
    RepositoryArtifactType,
    RepositoryContext,
    RetrievedContextItem,
)


class KeywordRepositoryContextProvider:
    SUPPORTED_SUFFIXES = {
        ".py",
        ".md",
    }

    STOP_WORDS = {
        "the",
        "and",
        "for",
        "with",
        "when",
        "that",
        "this",
        "should",
        "user",
        "users",
        "verify",
        "able",
        "from",
        "into",
        "after",
        "before",
        "then",
        "their",
        "they",
        "them",
        # Generic requirement language
        "can",
        "has",
        "using",
        "successfully",
        "application",
        "page",
        
    }

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    def __init__(
        self,
        repository_path: Path,
        top_k: int = 8,
    ) -> None:
        self._repository_path = repository_path
        self._top_k = top_k

    def retrieve(
        self,
        analysis: RequirementAnalysis,
    ) -> RepositoryContext:
        self._validate_repository()

        query_terms = self._build_query_terms(analysis)

        candidates: list[RetrievedContextItem] = []

        for path in self._iter_source_files():
            item = self._score_file(
                path=path,
                query_terms=query_terms,
            )

            if item is not None:
                candidates.append(item)

        candidates.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return RepositoryContext(
            query_terms=query_terms,
            items=candidates[: self._top_k],
        )

    def _validate_repository(self) -> None:
        if not self._repository_path.exists():
            raise FileNotFoundError(f"Repository does not exist: {self._repository_path}")

        if not self._repository_path.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {self._repository_path}")

    def _build_query_terms(
        self,
        analysis: RequirementAnalysis,
    ) -> list[str]:
        values = [
            analysis.feature,
            analysis.operation,
            *analysis.conditions,
            *analysis.expected_outcomes,
        ]

        text = " ".join(values)

        words = re.findall(
            r"[A-Za-z0-9_]+",
            text.lower(),
        )

        terms = {word for word in words if len(word) >= 3 and word not in self.STOP_WORDS}

        return sorted(terms)

    def _iter_source_files(
        self,
    ) -> Iterator[Path]:
        for path in self._repository_path.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix not in self.SUPPORTED_SUFFIXES:
                continue

            if self._should_ignore(path):
                continue

            yield path

    def _should_ignore(
        self,
        path: Path,
    ) -> bool:
        return any(part in self.IGNORED_DIRECTORIES for part in path.parts)

    def _score_file(
        self,
        path: Path,
        query_terms: list[str],
    ) -> RetrievedContextItem | None:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None

        relative_path = path.relative_to(self._repository_path)

        path_text = str(relative_path).lower()
        content_text = content.lower()

        score = 0.0
        matched_terms: list[str] = []

        for term in query_terms:
            term_score = 0.0

            if term in path_text:
                term_score += 5.0

            occurrences = content_text.count(term)

            if occurrences > 0:
                term_score += min(
                    float(occurrences),
                    3.0,
                )

            if term_score > 0:
                matched_terms.append(term)
                score += term_score

        if score == 0:
            return None

        return RetrievedContextItem(
            path=str(relative_path),
            artifact_type=self._classify_file(relative_path),
            score=score,
            matched_terms=matched_terms,
            snippet=self._extract_snippet(
                content=content,
                matched_terms=matched_terms,
            ),
        )

    def _classify_file(
        self,
        path: Path,
    ) -> RepositoryArtifactType:
        if (
            path.name == "conftest.py"
            or "fixtures" in path.parts
        ):
            return RepositoryArtifactType.FIXTURE

        if (
            "tests" in path.parts
            and path.name.startswith("test_")
        ):
            return RepositoryArtifactType.TEST

        if "pages" in path.parts:
            return RepositoryArtifactType.PAGE_OBJECT

        if "components" in path.parts:
            return RepositoryArtifactType.COMPONENT

        if "data" in path.parts:
            return RepositoryArtifactType.TEST_DATA

        if path.suffix == ".md":
            return RepositoryArtifactType.GUIDELINE

        return RepositoryArtifactType.OTHER
    def _extract_snippet(
        self,
        content: str,
        matched_terms: list[str],
        context_lines: int = 5,
    ) -> str:
        lines = content.splitlines()

        for index, line in enumerate(lines):
            line_lower = line.lower()

            if any(term in line_lower for term in matched_terms):
                start = max(
                    0,
                    index - context_lines,
                )

                end = min(
                    len(lines),
                    index + context_lines + 1,
                )

                return "\n".join(lines[start:end])

        return "\n".join(lines[: 2 * context_lines])
