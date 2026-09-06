from dataclasses import dataclass


@dataclass(frozen=True)
class TestUser:
    username: str
    email: str
    password: str
