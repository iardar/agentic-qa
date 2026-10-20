from playwright.sync_api import Locator, Page

from sample_automation.pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    def __init__(
        self,
        page: Page,
        base_url: str,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
        )

        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")
        self.sign_in_button = page.get_by_role(
            "button",
            name="Sign in",
        )
        self.error_messages = page.locator(".error-messages")

    def open(self) -> None:
        self.open_path(self.PATH)

    def sign_in(
        self,
        email: str,
        password: str,
    ) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()

    def authentication_error(self) -> Locator:
        return self.error_messages
