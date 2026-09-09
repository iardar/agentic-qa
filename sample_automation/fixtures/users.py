import os

import pytest

from sample_automation.data.user_builder import (
    TestUser,
    build_unique_user,
)


@pytest.fixture
def registered_user() -> TestUser:
    username = os.getenv("REALWORLD_TEST_USERNAME")
    email = os.getenv("REALWORLD_TEST_EMAIL")
    password = os.getenv("REALWORLD_TEST_PASSWORD")

    if not username:
        raise RuntimeError("REALWORLD_TEST_USERNAME is not configured.")

    if not email:
        raise RuntimeError("REALWORLD_TEST_EMAIL is not configured.")

    if not password:
        raise RuntimeError("REALWORLD_TEST_PASSWORD is not configured.")

    return TestUser(
        username=username,
        email=email,
        password=password,
    )


@pytest.fixture
def new_user() -> TestUser:
    return build_unique_user()
