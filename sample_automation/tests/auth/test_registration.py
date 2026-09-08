from playwright.sync_api import expect

from sample_automation.data.user_builder import build_unique_user
from sample_automation.pages.home_page import HomePage
from sample_automation.pages.register_page import RegisterPage


def test_user_can_register(
    register_page: RegisterPage,
    home_page: HomePage,
) -> None:
    user = build_unique_user()

    register_page.open()

    register_page.register(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    expect(
        home_page.navigation.user_profile_link(
            user.username
        )
    ).to_be_visible()