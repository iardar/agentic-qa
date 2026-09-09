from playwright.sync_api import expect

from sample_automation.data.user_builder import (
    TestUser,
)
from sample_automation.pages.home_page import (
    HomePage,
)
from sample_automation.pages.login_page import (
    LoginPage,
)


def test_registered_user_can_sign_in(
    login_page: LoginPage,
    home_page: HomePage,
    registered_user: TestUser,
) -> None:
    login_page.open()

    login_page.sign_in(
        email=registered_user.email,
        password=registered_user.password,
    )

    expect(home_page.navigation.user_profile_link(registered_user.username)).to_be_visible()
