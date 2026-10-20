from agentic_qa.retrieval.symbols import (
    RepositorySymbol,
    RepositorySymbolIndex,
    RetrievedSymbol,
    SymbolRetrievalContext,
    SymbolType,
)


def test_repository_symbol_represents_method() -> None:
    symbol = RepositorySymbol(
        name="sign_in",
        qualified_name="LoginPage.sign_in",
        symbol_type=SymbolType.METHOD,
        path="pages/login_page.py",
        parent="LoginPage",
        start_line=30,
        end_line=38,
        source=("def sign_in(self, email: str, password: str) -> None: ..."),
        parameters=[
            "self",
            "email",
            "password",
        ],
    )

    assert symbol.name == "sign_in"
    assert symbol.qualified_name == "LoginPage.sign_in"
    assert symbol.symbol_type == SymbolType.METHOD
    assert symbol.parent == "LoginPage"
    assert symbol.parameters == [
        "self",
        "email",
        "password",
    ]


def test_repository_symbol_uses_empty_metadata_by_default() -> None:
    symbol = RepositorySymbol(
        name="LoginPage",
        qualified_name="LoginPage",
        symbol_type=SymbolType.CLASS,
        path="pages/login_page.py",
        start_line=1,
        end_line=20,
        source="class LoginPage: ...",
    )

    assert symbol.parent is None
    assert symbol.parameters == []
    assert symbol.decorators == []
    assert symbol.bases == []


def test_repository_symbol_index_contains_symbols() -> None:
    symbol = RepositorySymbol(
        name="registered_user",
        qualified_name="registered_user",
        symbol_type=SymbolType.FIXTURE,
        path="fixtures/users.py",
        start_line=10,
        end_line=20,
        source="def registered_user(): ...",
        decorators=[
            "pytest.fixture",
        ],
    )

    index = RepositorySymbolIndex(symbols=[symbol])

    assert len(index.symbols) == 1
    assert index.symbols[0].name == "registered_user"
    assert index.symbols[0].symbol_type == SymbolType.FIXTURE


def test_symbol_retrieval_context_contains_ranked_symbol() -> None:
    symbol = RepositorySymbol(
        name="test_registered_user_can_sign_in",
        qualified_name="test_registered_user_can_sign_in",
        symbol_type=SymbolType.TEST,
        path="tests/auth/test_login.py",
        start_line=10,
        end_line=25,
        source=("def test_registered_user_can_sign_in(): ..."),
    )

    retrieved = RetrievedSymbol(
        symbol=symbol,
        score=12.0,
        matched_terms=[
            "registered",
            "sign",
        ],
    )

    context = SymbolRetrievalContext(
        query_terms=[
            "registered",
            "sign",
        ],
        items=[
            retrieved,
        ],
    )

    assert context.items[0].symbol.path == ("tests/auth/test_login.py")
    assert context.items[0].score == 12.0
    assert context.items[0].matched_terms == [
        "registered",
        "sign",
    ]


def test_symbol_retrieval_context_serializes_to_json() -> None:
    symbol = RepositorySymbol(
        name="sign_in",
        qualified_name="LoginPage.sign_in",
        symbol_type=SymbolType.METHOD,
        path="pages/login_page.py",
        parent="LoginPage",
        start_line=30,
        end_line=38,
        source="def sign_in(...): ...",
    )

    context = SymbolRetrievalContext(
        query_terms=["sign"],
        items=[
            RetrievedSymbol(
                symbol=symbol,
                score=10.0,
                matched_terms=["sign"],
            )
        ],
    )

    data = context.model_dump(mode="json")

    assert data["query_terms"] == ["sign"]
    assert data["items"][0]["score"] == 10.0
    assert data["items"][0]["symbol"]["symbol_type"] == "method"
