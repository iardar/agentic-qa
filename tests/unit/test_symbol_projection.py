from agentic_qa.retrieval.models import RepositoryArtifactType
from agentic_qa.retrieval.symbols.models import (
    RepositorySymbol,
    RetrievedSymbol,
    SymbolRetrievalContext,
    SymbolType,
)
from agentic_qa.retrieval.symbols.projection import (
    project_symbols_to_repository_context,
)


def test_projection_collapses_duplicate_paths() -> None:
    edit_method = RepositorySymbol(
        name="edit_article",
        qualified_name="ArticlePage.edit_article",
        symbol_type=SymbolType.METHOD,
        path="pages/article_page.py",
        parent="ArticlePage",
        start_line=20,
        end_line=22,
        source=(
            "def edit_article(self):\n"
            "    self.edit_button.click()"
        ),
        parameters=["self"],
    )

    article_class = RepositorySymbol(
        name="ArticlePage",
        qualified_name="ArticlePage",
        symbol_type=SymbolType.CLASS,
        path="pages/article_page.py",
        start_line=1,
        end_line=40,
        source="class ArticlePage(BasePage): ...",
        bases=["BasePage"],
    )

    edit_test = RepositorySymbol(
        name="test_user_can_edit_article",
        qualified_name="test_user_can_edit_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_edit_article.py",
        start_line=1,
        end_line=10,
        source=(
            "def test_user_can_edit_article("
            "existing_article, article_page"
            "): pass"
        ),
        parameters=[
            "existing_article",
            "article_page",
        ],
    )

    existing_article_fixture = RepositorySymbol(
        name="existing_article",
        qualified_name="existing_article",
        symbol_type=SymbolType.FIXTURE,
        path="fixtures/articles.py",
        start_line=10,
        end_line=20,
        source="def existing_article(): ...",
        decorators=["pytest.fixture"],
    )

    symbol_context = SymbolRetrievalContext(
        query_terms=[
            "article",
            "edit",
            "existing",
        ],
        items=[
            RetrievedSymbol(
                symbol=edit_method,
                score=30.0,
                matched_terms=[
                    "article",
                    "edit",
                ],
            ),
            RetrievedSymbol(
                symbol=article_class,
                score=25.0,
                matched_terms=["article"],
            ),
            RetrievedSymbol(
                symbol=edit_test,
                score=24.0,
                matched_terms=[
                    "article",
                    "edit",
                    "existing",
                ],
            ),
            RetrievedSymbol(
                symbol=existing_article_fixture,
                score=20.0,
                matched_terms=[
                    "article",
                    "existing",
                ],
            ),
        ],
    )

    context = project_symbols_to_repository_context(
        symbol_context,
        top_k=8,
    )

    assert [item.path for item in context.items] == [
        "pages/article_page.py",
        "tests/articles/test_edit_article.py",
        "fixtures/articles.py",
    ]

    assert context.query_terms == [
        "article",
        "edit",
        "existing",
    ]

    assert context.items[0].score == 30.0

    assert (
        context.items[0].artifact_type
        == RepositoryArtifactType.PAGE_OBJECT
    )

    assert (
        context.items[1].artifact_type
        == RepositoryArtifactType.TEST
    )

    assert (
        context.items[2].artifact_type
        == RepositoryArtifactType.FIXTURE
    )