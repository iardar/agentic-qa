from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class CommentData:
    body: str


@dataclass(frozen=True)
class CreatedComment:
    id: int
    body: str
    author_username: str


def build_unique_comment() -> CommentData:
    return CommentData(body=f"QA automated comment {uuid4().hex}")
