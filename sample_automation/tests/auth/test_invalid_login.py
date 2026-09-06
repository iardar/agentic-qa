from playwright.sync_api import expect

from sample_automation.data.user_builder import TestUser
from sample_automation.pages.login_page import LoginPage


def test_valid_user_invalid_password(
    login_page: LoginPage,
    registered_user: TestUser,
) -> None:
    login_page.open()

    login_page.sign_in(
        email=registered_user.email,
        password="invalid-password",
    )

    expect(
        login_page.authentication_error()
    ).to_contain_text("credentials invalid")

    expect(login_page.page).to_have_url(
        f"{login_page.base_url}/login"
    )