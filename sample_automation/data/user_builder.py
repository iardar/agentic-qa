from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class UserData:
    username: str
    email: str
    password: str


def build_unique_user() -> UserData:
    suffix = uuid4().hex[:10]

    return UserData(
        username=f"agentic_qa_{suffix}",
        email=f"agentic_qa_{suffix}@example.com",
        password="QaPassword123!",
    )
