from collections.abc import Iterator

import pytest
from playwright.sync_api import (
    APIRequestContext,
    Page,
    Playwright,
    expect,
)

from sample_automation.api.realworld_client import (
    RealWorldApiClient,
)
from sample_automation.data.article_builder import (
    CreatedArticle,
    ArticleData,
    build_article_update,
    build_unique_article,
)
from sample_automation.data.user_builder import (
    UserData,
)
from sample_automation.pages.article_page import ArticlePage
from sample_automation.pages.editor_page import EditorPage
from sample_automation.components.navigation import Navigation

@pytest.fixture
def realworld_api_context(
    playwright: Playwright,
    realworld_api_base_url: str,
) -> Iterator[APIRequestContext]:
    request = playwright.request.new_context(
        base_url=realworld_api_base_url,
    )

    yield request

    request.dispose()


@pytest.fixture
def realworld_api_client(
    realworld_api_context: APIRequestContext,
) -> RealWorldApiClient:
    return RealWorldApiClient(
        request=realworld_api_context,
    )


@pytest.fixture
def registered_user_token(
    realworld_api_client: RealWorldApiClient,
    registered_user: UserData,
) -> str:
    return realworld_api_client.login(
        email=registered_user.email,
        password=registered_user.password,
    )


@pytest.fixture
def new_article() -> ArticleData:
    return build_unique_article()


@pytest.fixture
def existing_article(
    realworld_api_client: RealWorldApiClient,
    registered_user_token: str,
) -> Iterator[CreatedArticle]:
    article_data = build_unique_article()

    article = realworld_api_client.create_article(
        token=registered_user_token,
        article=article_data,
    )

    yield article

    realworld_api_client.delete_article(
        token=registered_user_token,
        slug=article.slug,
        allow_missing=True,
    )


@pytest.fixture
def article_update(
    existing_article: CreatedArticle,
) -> ArticleData:
    return build_article_update(
        title=existing_article.title,
    )


@pytest.fixture
def editor_page(
    page: Page,
    realworld_base_url: str,
) -> EditorPage:
    return EditorPage(
        page=page,
        base_url=realworld_base_url,
    )


@pytest.fixture
def article_page(
    page: Page,
    realworld_base_url: str,
) -> ArticlePage:
    return ArticlePage(
        page=page,
        base_url=realworld_base_url,
    )

@pytest.fixture
def api_authenticated_user(
    page: Page,
    realworld_base_url: str,
    registered_user: UserData,
    registered_user_token: str,
) -> UserData:
    page.goto(realworld_base_url)

    page.evaluate(
        "(token) => localStorage.setItem('jwtToken', token)",
        registered_user_token,
    )

    page.reload()

    navigation = Navigation(page)

    expect(
        navigation.user_profile_link(
            registered_user.username
        )
    ).to_be_visible()

    return registered_user