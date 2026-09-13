from pathlib import Path

from agentic_qa.retrieval.symbols.indexer import (
    PythonAstSymbolIndexer,
)
from agentic_qa.retrieval.symbols.models import (
    SymbolType,
)


def test_indexer_extracts_class_and_method(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "login_page.py"

    source_file.write_text(
        """
class LoginPage(BasePage):
    def sign_in(
        self,
        email: str,
        password: str,
    ) -> None:
        pass
""".strip(),
        encoding="utf-8",
    )

    indexer = PythonAstSymbolIndexer(repository_path=tmp_path)

    index = indexer.build_index()

    assert len(index.symbols) == 2

    page_class = index.symbols[0]

    assert page_class.name == "LoginPage"
    assert page_class.symbol_type == SymbolType.CLASS
    assert page_class.bases == ["BasePage"]

    sign_in = index.symbols[1]

    assert sign_in.name == "sign_in"
    assert sign_in.qualified_name == "LoginPage.sign_in"
    assert sign_in.symbol_type == SymbolType.METHOD
    assert sign_in.parent == "LoginPage"
    assert sign_in.parameters == [
        "self",
        "email",
        "password",
    ]


def test_indexer_recognizes_pytest_fixture(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "users.py"

    source_file.write_text(
        """
import pytest


@pytest.fixture
def registered_user() -> TestUser:
    return TestUser()
""".strip(),
        encoding="utf-8",
    )

    index = PythonAstSymbolIndexer(repository_path=tmp_path).build_index()

    symbol = index.symbols[0]

    assert symbol.name == "registered_user"
    assert symbol.symbol_type == SymbolType.FIXTURE
    assert symbol.decorators == ["pytest.fixture"]


def test_indexer_recognizes_test_and_parameters(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "test_login.py"

    source_file.write_text(
        """
def test_registered_user_can_sign_in(
    login_page,
    home_page,
    registered_user,
) -> None:
    pass
""".strip(),
        encoding="utf-8",
    )

    index = PythonAstSymbolIndexer(repository_path=tmp_path).build_index()

    symbol = index.symbols[0]

    assert symbol.name == "test_registered_user_can_sign_in"
    assert symbol.symbol_type == SymbolType.TEST

    assert symbol.parameters == [
        "login_page",
        "home_page",
        "registered_user",
    ]


def test_indexer_recognizes_regular_function(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "user_builder.py"

    source_file.write_text(
        """
def build_unique_user() -> TestUser:
    return TestUser()
""".strip(),
        encoding="utf-8",
    )

    index = PythonAstSymbolIndexer(repository_path=tmp_path).build_index()

    symbol = index.symbols[0]

    assert symbol.name == "build_unique_user"
    assert symbol.symbol_type == SymbolType.FUNCTION


def test_indexer_extracts_fixture_parameters(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "authentication.py"

    source_file.write_text(
        """
import pytest


@pytest.fixture
def login_page(
    page: Page,
    base_url: str,
) -> LoginPage:
    return LoginPage(
        page=page,
        base_url=base_url,
    )
""".strip(),
        encoding="utf-8",
    )

    index = PythonAstSymbolIndexer(repository_path=tmp_path).build_index()

    symbol = index.symbols[0]

    assert symbol.symbol_type == SymbolType.FIXTURE

    assert symbol.parameters == [
        "page",
        "base_url",
    ]
