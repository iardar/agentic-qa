from typing import Any, cast

from playwright.sync_api import (
    APIRequestContext,
    APIResponse,
)

from sample_automation.data.article_builder import (
    ArticleData,
    CreatedArticle,
)


class RealWorldApiClient:
    def __init__(
        self,
        request: APIRequestContext,
    ) -> None:
        self._request = request

    def login(
        self,
        email: str,
        password: str,
    ) -> str:
        response = self._request.post(
            "/api/users/login",
            data={
                "user": {
                    "email": email,
                    "password": password,
                }
            },
        )

        self._require_status(
            response=response,
            expected={200},
            operation="login",
        )

        payload = cast(
            dict[str, Any],
            response.json(),
        )

        user = payload.get("user")

        if not isinstance(user, dict):
            raise RuntimeError("Login response does not contain a user object.")

        token = user.get("token")

        if not isinstance(token, str):
            raise RuntimeError("Login response does not contain a valid token.")

        return token

    def create_article(
        self,
        token: str,
        article: ArticleData,
    ) -> CreatedArticle:
        response = self._request.post(
            "/api/articles",
            headers=self._auth_headers(token),
            data={
                "article": {
                    "title": article.title,
                    "description": article.description,
                    "body": article.body,
                    "tagList": article.tags,
                }
            },
        )

        self._require_status(
            response=response,
            expected={200, 201},
            operation="create article",
        )

        return self._article_from_response(response)

    def update_article(
        self,
        token: str,
        slug: str,
        article: ArticleData,
    ) -> CreatedArticle:
        response = self._request.put(
            f"/api/articles/{slug}",
            headers=self._auth_headers(token),
            data={
                "article": {
                    "title": article.title,
                    "description": article.description,
                    "body": article.body,
                }
            },
        )

        self._require_status(
            response=response,
            expected={200},
            operation="update article",
        )

        return self._article_from_response(response)

    def delete_article(
        self,
        token: str,
        slug: str,
        *,
        allow_missing: bool = False,
    ) -> None:
        response = self._request.delete(
            f"/api/articles/{slug}",
            headers=self._auth_headers(token),
        )

        expected = {
            200,
            204,
        }

        if allow_missing:
            expected.add(404)

        self._require_status(
            response=response,
            expected=expected,
            operation="delete article",
        )

    def article_exists(
        self,
        token: str,
        slug: str,
    ) -> bool:
        response = self._request.get(
            f"/api/articles/{slug}",
            headers=self._auth_headers(token),
        )

        if response.status == 200:
            return True

        if response.status == 404:
            return False

        raise RuntimeError(
            "RealWorld API get article failed: "
            f"status={response.status}, "
            f"body={response.text()}"
        )

    def _auth_headers(
        self,
        token: str,
    ) -> dict[str, str]:
        return {
            "Authorization": f"Token {token}",
        }

    def _article_from_response(
        self,
        response: APIResponse,
    ) -> CreatedArticle:
        payload = cast(
            dict[str, Any],
            response.json(),
        )

        article = payload.get("article")

        if not isinstance(article, dict):
            raise RuntimeError("API response does not contain an article object.")

        slug = article.get("slug")
        title = article.get("title")
        description = article.get("description")
        body = article.get("body")
        tags = article.get("tagList")

        if not isinstance(slug, str):
            raise RuntimeError("Article response has invalid slug.")

        if not isinstance(title, str):
            raise RuntimeError("Article response has invalid title.")

        if not isinstance(description, str):
            raise RuntimeError("Article response has invalid description.")

        if not isinstance(body, str):
            raise RuntimeError("Article response has invalid body.")

        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise RuntimeError("Article response has invalid tagList.")

        return CreatedArticle(
            slug=slug,
            title=title,
            description=description,
            body=body,
            tags=tags,
        )

    def _require_status(
        self,
        response: APIResponse,
        expected: set[int],
        operation: str,
    ) -> None:
        if response.status in expected:
            return

        raise RuntimeError(
            f"RealWorld API {operation} failed: status={response.status}, body={response.text()}"
        )
