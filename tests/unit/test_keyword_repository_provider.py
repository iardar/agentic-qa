from pathlib import Path

import pytest

from agentic_qa.models import (
    InteractionSurface,
    RequirementAnalysis,
)
from agentic_qa.retrieval.keyword_provider import (
    KeywordRepositoryContextProvider,
)
from agentic_qa.retrieval.models import (
    RepositoryArtifactType,
)


def create_analysis() -> RequirementAnalysis:
    return RequirementAnalysis(
        feature="Todo management",
        operation="Complete an existing todo",
        objective=("Verify that an existing todo can be completed."),
        actors=[
            "User",
        ],
        conditions=[
            "A todo already exists.",
        ],
        expected_outcomes=[
            "The todo is completed.",
        ],
        ambiguities=[],
        interaction_surface=(InteractionSurface.UNKNOWN),
    )


def test_retrieves_relevant_repository_files(
    tmp_path: Path,
) -> None:
    pages_dir = tmp_path / "pages"
    tests_dir = tmp_path / "tests"

    pages_dir.mkdir()
    tests_dir.mkdir()

    (pages_dir / "todo_page.py").write_text(
        """
class TodoPage:
    def complete_todo(self, title: str) -> None:
        pass
""",
        encoding="utf-8",
    )

    (tests_dir / "test_todo_completion.py").write_text(
        """
def test_user_can_complete_todo():
    pass
""",
        encoding="utf-8",
    )

    (tests_dir / "test_login.py").write_text(
        """
def test_user_can_login():
    pass
""",
        encoding="utf-8",
    )

    provider = KeywordRepositoryContextProvider(
        repository_path=tmp_path,
    )

    context = provider.retrieve(create_analysis())

    paths = {item.path for item in context.items}

    assert "pages/todo_page.py" in paths
    assert "tests/test_todo_completion.py" in paths

    assert "tests/test_login.py" not in paths


def test_classifies_repository_artifacts(
    tmp_path: Path,
) -> None:
    pages_dir = tmp_path / "pages"
    tests_dir = tmp_path / "tests"

    pages_dir.mkdir()
    tests_dir.mkdir()

    (pages_dir / "todo_page.py").write_text(
        "class TodoPage: pass",
        encoding="utf-8",
    )

    (tests_dir / "test_todo_completion.py").write_text(
        """
def test_complete_todo():
    pass
""",
        encoding="utf-8",
    )

    (tests_dir / "conftest.py").write_text(
        """
import pytest


@pytest.fixture
def existing_todo():
    return "todo"
""",
        encoding="utf-8",
    )

    provider = KeywordRepositoryContextProvider(
        repository_path=tmp_path,
    )

    context = provider.retrieve(create_analysis())

    artifact_types = {item.path: item.artifact_type for item in context.items}

    assert artifact_types["pages/todo_page.py"] == RepositoryArtifactType.PAGE_OBJECT

    assert artifact_types["tests/test_todo_completion.py"] == RepositoryArtifactType.TEST

    assert artifact_types["tests/conftest.py"] == RepositoryArtifactType.FIXTURE


def test_raises_error_when_repository_does_not_exist(
    tmp_path: Path,
) -> None:
    missing_repository = tmp_path / "missing"

    provider = KeywordRepositoryContextProvider(
        repository_path=missing_repository,
    )

    with pytest.raises(FileNotFoundError):
        provider.retrieve(create_analysis())
