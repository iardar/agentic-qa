from agentic_qa.models import (
    InteractionSurface,
    RequirementAnalysis,
)
from agentic_qa.retrieval.symbols.models import (
    RepositorySymbol,
    RepositorySymbolIndex,
    SymbolType,
)
from agentic_qa.retrieval.symbols.provider import (
    SymbolRepositoryContextProvider,
)


def create_edit_article_analysis(
) -> RequirementAnalysis:
    return RequirementAnalysis(
        feature="Article management",
        operation="Edit article",
        objective=(
            "Verify that an authenticated user "
            "can edit an existing article."
        ),
        actors=[
            "Authenticated user",
        ],
        conditions=[
            "An existing article is available.",
        ],
        expected_outcomes=[
            "The article is updated.",
        ],
        ambiguities=[],
        interaction_surface=InteractionSurface.UI,
    )


def create_invalid_login_analysis() -> RequirementAnalysis:
    return RequirementAnalysis(
        feature="Authentication",
        operation="Sign in with invalid password",
        objective=(
            "Verify that a registered user cannot sign in "
            "with an invalid password."
        ),
        actors=[
            "Registered user",
        ],
        conditions=[
            "A registered user exists.",
            "The user enters an invalid password.",
        ],
        expected_outcomes=[
            "Sign in is rejected.",
            "An authentication error is visible.",
        ],
        ambiguities=[],
        interaction_surface=InteractionSurface.UI,
    )

def create_sparse_delete_article_analysis(
) -> RequirementAnalysis:
    return RequirementAnalysis(
        feature="Article management",
        operation="Delete article",
        objective="Verify article deletion.",
        actors=[],
        conditions=[],
        expected_outcomes=[],
        ambiguities=[
            (
                "The requirement does not specify "
                "preconditions or expected results."
            ),
        ],
        interaction_surface=InteractionSurface.UNKNOWN,
    )

def test_diagnostic_symbol_scores_for_invalid_login() -> None:
    invalid_login_test = RepositorySymbol(
        name="test_valid_user_invalid_password",
        qualified_name="test_valid_user_invalid_password",
        symbol_type=SymbolType.TEST,
        path="tests/auth/test_invalid_login.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_valid_user_invalid_password("
            "registered_user, login_page, invalid_password"
            "): pass"
        ),
        parameters=[
            "registered_user",
            "login_page",
            "invalid_password",
        ],
    )

    valid_login_test = RepositorySymbol(
        name="test_registered_user_can_sign_in",
        qualified_name="test_registered_user_can_sign_in",
        symbol_type=SymbolType.TEST,
        path="tests/auth/test_login.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_registered_user_can_sign_in("
            "registered_user, login_page"
            "): pass"
        ),
        parameters=[
            "registered_user",
            "login_page",
        ],
    )

    invalid_registration_test = RepositorySymbol(
        name="test_user_cannot_register_without_username",
        qualified_name=(
            "test_user_cannot_register_without_username"
        ),
        symbol_type=SymbolType.TEST,
        path="tests/auth/test_invalid_registration.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_cannot_register_without_username("
            "register_page"
            "): pass"
        ),
        parameters=[
            "register_page",
        ],
    )

    provider = SymbolRepositoryContextProvider(
        symbol_index=RepositorySymbolIndex(
            symbols=[
                valid_login_test,
                invalid_registration_test,
                invalid_login_test,
            ]
        )
    )

    context = provider.retrieve(
        create_invalid_login_analysis()
    )

    print("\nQUERY TERMS:")
    print(context.query_terms)

    print("\nRANKED SYMBOLS:")

    for rank, item in enumerate(
        context.items,
        start=1,
    ):
        print(
            f"{rank}. "
            f"{item.symbol.qualified_name} "
            f"score={item.score} "
            f"matched={item.matched_terms}"
        )

    assert (
        context.items[0].symbol.qualified_name
        == "test_valid_user_invalid_password"
    )

def test_retriever_prefers_symbol_matching_operation(
) -> None:
    edit_test = RepositorySymbol(
        name="test_user_can_edit_article",
        qualified_name="test_user_can_edit_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_edit_article.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_can_edit_article"
            "(existing_article): pass"
        ),
        parameters=[
            "existing_article",
        ],
    )

    delete_test = RepositorySymbol(
        name="test_user_can_delete_article",
        qualified_name=(
            "test_user_can_delete_article"
        ),
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_delete_article.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_can_delete_article"
            "(existing_article): pass"
        ),
        parameters=[
            "existing_article",
        ],
    )

    provider = SymbolRepositoryContextProvider(
        symbol_index=RepositorySymbolIndex(
            symbols=[
                delete_test,
                edit_test,
            ]
        )
    )

    context = provider.retrieve(
        create_edit_article_analysis()
    )

    assert (
        context.items[0].symbol.qualified_name
        == "test_user_can_edit_article"
    )

    assert "edit" in context.items[0].matched_terms


def test_retriever_uses_parameters_as_structural_evidence(
) -> None:
    parameter_match = RepositorySymbol(
        name="prepare",
        qualified_name="prepare",
        symbol_type=SymbolType.FUNCTION,
        path="helpers/context.py",
        start_line=1,
        end_line=2,
        source=(
            "def prepare(existing_article):\n"
            "    return existing_article"
        ),
        parameters=[
            "existing_article",
        ],
    )

    source_only_match = RepositorySymbol(
        name="prepare_other",
        qualified_name="prepare_other",
        symbol_type=SymbolType.FUNCTION,
        path="helpers/context.py",
        start_line=1,
        end_line=3,
        source=(
            "def prepare_other():\n"
            "    existing_article = None\n"
            "    return existing_article"
        ),
        parameters=[],
    )

    provider = SymbolRepositoryContextProvider(
        symbol_index=RepositorySymbolIndex(
            symbols=[
                source_only_match,
                parameter_match,
            ]
        )
    )

    context = provider.retrieve(
        create_edit_article_analysis()
    )

    assert context.items[0].symbol.name == "prepare"

    assert (
        context.items[0].score
        > context.items[1].score
    )

def test_diagnostic_symbol_scores_for_edit_article() -> None:
    edit_test = RepositorySymbol(
        name="test_user_can_edit_article",
        qualified_name="test_user_can_edit_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_edit_article.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_can_edit_article("
            "existing_article, article_update, article_page"
            "): pass"
        ),
        parameters=[
            "existing_article",
            "article_update",
            "article_page",
        ],
    )

    edit_method = RepositorySymbol(
        name="edit_article",
        qualified_name="ArticlePage.edit_article",
        symbol_type=SymbolType.METHOD,
        path="pages/article_page.py",
        parent="ArticlePage",
        start_line=10,
        end_line=12,
        source=(
            "def edit_article(self):\n"
            "    self.edit_button.click()"
        ),
        parameters=[
            "self",
        ],
    )

    delete_test = RepositorySymbol(
        name="test_user_can_delete_article",
        qualified_name="test_user_can_delete_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_delete_article.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_can_delete_article("
            "existing_article, article_page"
            "): pass"
        ),
        parameters=[
            "existing_article",
            "article_page",
        ],
    )

    provider = SymbolRepositoryContextProvider(
        symbol_index=RepositorySymbolIndex(
            symbols=[
                delete_test,
                edit_method,
                edit_test,
            ]
        )
    )

    context = provider.retrieve(
        create_edit_article_analysis()
    )

    print("\nQUERY TERMS:")
    print(context.query_terms)

    print("\nRANKED SYMBOLS:")

    for rank, item in enumerate(
        context.items,
        start=1,
    ):
        print(
            f"{rank}. "
            f"{item.symbol.qualified_name} "
            f"score={item.score} "
            f"matched={item.matched_terms}"
        )

    assert context.items

def test_diagnostic_symbol_scores_for_sparse_delete_article(
) -> None:
    delete_test = RepositorySymbol(
        name="test_user_can_delete_article",
        qualified_name="test_user_can_delete_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_delete_article.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_can_delete_article("
            "existing_article, article_page"
            "): pass"
        ),
        parameters=[
            "existing_article",
            "article_page",
        ],
    )

    delete_method = RepositorySymbol(
        name="delete_article",
        qualified_name="ArticlePage.delete_article",
        symbol_type=SymbolType.METHOD,
        path="pages/article_page.py",
        parent="ArticlePage",
        start_line=10,
        end_line=12,
        source=(
            "def delete_article(self):\n"
            "    self.delete_button.click()"
        ),
        parameters=[
            "self",
        ],
    )

    edit_test = RepositorySymbol(
        name="test_user_can_edit_article",
        qualified_name="test_user_can_edit_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_edit_article.py",
        start_line=1,
        end_line=5,
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

    create_test = RepositorySymbol(
        name="test_user_can_create_article",
        qualified_name="test_user_can_create_article",
        symbol_type=SymbolType.TEST,
        path="tests/articles/test_create_article.py",
        start_line=1,
        end_line=5,
        source=(
            "def test_user_can_create_article("
            "new_article, article_page"
            "): pass"
        ),
        parameters=[
            "new_article",
            "article_page",
        ],
    )

    provider = SymbolRepositoryContextProvider(
        symbol_index=RepositorySymbolIndex(
            symbols=[
                edit_test,
                create_test,
                delete_method,
                delete_test,
            ]
        )
    )

    context = provider.retrieve(
        create_sparse_delete_article_analysis()
    )

    print("\nQUERY TERMS:")
    print(context.query_terms)

    print("\nRANKED SYMBOLS:")

    for rank, item in enumerate(
        context.items,
        start=1,
    ):
        print(
            f"{rank}. "
            f"{item.symbol.qualified_name} "
            f"score={item.score} "
            f"matched={item.matched_terms}"
        )

    top_two = {
        item.symbol.qualified_name
        for item in context.items[:2]
    }

    assert top_two == {
        "test_user_can_delete_article",
        "ArticlePage.delete_article",
    }    