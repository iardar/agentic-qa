from typing import Any, cast

from playwright.sync_api import (
    APIRequestContext,
    APIResponse,
)

from sample_automation.data.article_builder import (
    ArticleData,
    CreatedArticle,
)
from sample_automation.data.comment_builder import (
    CommentData,
    CreatedComment,
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
            f"RealWorld API get article failed: status={response.status}, body={response.text()}"
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
    
    def create_comment(
        self,
        token: str,
        slug: str,
        comment: CommentData,
    ) -> CreatedComment:
        response = self._request.post(
            f"/api/articles/{slug}/comments",
            headers=self._auth_headers(token),
            data={
                "comment": {
                    "body": comment.body,
                }
            },
        )

        self._require_status(
            response=response,
            expected={200, 201},
            operation="create comment",
        )

        return self._comment_from_response(response)

    def get_comments(
        self,
        token: str,
        slug: str,
    ) -> list[CreatedComment]:
        response = self._request.get(
            f"/api/articles/{slug}/comments",
            headers=self._auth_headers(token),
        )

        self._require_status(
            response=response,
            expected={200},
            operation="get comments",
        )

        payload = cast(
            dict[str, Any],
            response.json(),
        )

        comments = payload.get("comments")

        if not isinstance(comments, list):
            raise RuntimeError(
                "Get comments response has invalid comments list."
            )

        return [
            self._parse_comment(item)
            for item in comments
        ]    

    def delete_comment(
        self,
        token: str,
        slug: str,
        comment_id: int,
        *,
        allow_missing: bool = False,
    ) -> None:
        response = self._request.delete(
            f"/api/articles/{slug}/comments/{comment_id}",
            headers=self._auth_headers(token),
        )

        expected = {200, 204}

        if allow_missing:
            expected.add(404)

        self._require_status(
            response=response,
            expected=expected,
            operation="delete comment",
        )


    def _comment_from_response(
        self,
        response: APIResponse,
    ) -> CreatedComment:
        payload = cast(
            dict[str, Any],
            response.json(),
        )

        return self._parse_comment(
            payload.get("comment")
        )


    def _parse_comment(
        self,
        comment: Any,
    ) -> CreatedComment:
        if not isinstance(comment, dict):
            raise RuntimeError(
                "API response does not contain a comment object."
            )

        comment_id = comment.get("id")
        body = comment.get("body")
        author = comment.get("author")

        if (
            not isinstance(comment_id, int)
            or isinstance(comment_id, bool)
        ):
            raise RuntimeError(
                "Comment response has invalid id."
            )

        if not isinstance(body, str):
            raise RuntimeError(
                "Comment response has invalid body."
            )

        if not isinstance(author, dict):
            raise RuntimeError(
                "Comment response has invalid author."
            )

        username = author.get("username")

        if not isinstance(username, str):
            raise RuntimeError(
                "Comment response has invalid author username."
            )

        return CreatedComment(
            id=comment_id,
            body=body,
            author_username=username,
        )