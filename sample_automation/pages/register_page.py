from playwright.sync_api import Locator, Page

from sample_automation.pages.base_page import BasePage


class RegisterPage(BasePage):
    PATH = "/register"

    def __init__(
        self,
        page: Page,
        base_url: str,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
        )

        self.username_input = page.get_by_placeholder("Username")
        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")

        self.sign_up_button = page.get_by_role(
            "button",
            name="Sign up",
        )

        self.error_messages = page.locator(".error-messages")

    def open(self) -> None:
        self.open_path(self.PATH)

    def fill_registration_form(
        self,
        username: str,
        email: str,
        password: str,
    ) -> None:
        self.username_input.fill(username)
        self.email_input.fill(email)
        self.password_input.fill(password)

    def register(
        self,
        username: str,
        email: str,
        password: str,
    ) -> None:
        self.fill_registration_form(
            username=username,
            email=email,
            password=password,
        )
        self.sign_up_button.click()

    def registration_errors(self) -> Locator:
        return self.error_messages
