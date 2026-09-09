from playwright.sync_api import expect

from sample_automation.data.user_builder import TestUser
from sample_automation.pages.register_page import RegisterPage


def test_user_cannot_register_without_username(
    register_page: RegisterPage,
    new_user: TestUser,
) -> None:
    register_page.open()

    register_page.fill_registration_form(
        username="",
        email=new_user.email,
        password=new_user.password,
    )

    expect(
        register_page.sign_up_button
    ).to_be_disabled()

    expect(register_page.page).to_have_url(
        f"{register_page.base_url}/register"
    )