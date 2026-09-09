from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class TestUser:
    username: str
    email: str
    password: str


def build_unique_user() -> TestUser:
    suffix = uuid4().hex[:10]

    return TestUser(
        username=f"agentic_qa_{suffix}",
        email=f"agentic_qa_{suffix}@example.com",
        password="QaPassword123!",
    )