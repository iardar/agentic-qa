from playwright.sync_api import expect

from sample_automation.data.user_builder import TestUser
from sample_automation.pages.home_page import HomePage
from sample_automation.pages.register_page import RegisterPage


def test_user_can_register(
    register_page: RegisterPage,
    home_page: HomePage,
    new_user: TestUser,
) -> None:
    register_page.open()

    register_page.register(
        username=new_user.username,
        email=new_user.email,
        password=new_user.password,
    )

    expect(home_page.navigation.user_profile_link(new_user.username)).to_be_visible()
