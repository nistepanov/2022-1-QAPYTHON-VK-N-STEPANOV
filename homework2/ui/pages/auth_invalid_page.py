from homework2.ui.locators.my_target_locators.static_locators import InvalidAuthLocators
from .base_page import BasePage
from ..locators.my_target_locators.static_locators import LoginPageLocators


class AuthInvalidPage(BasePage):
    locators = LoginPageLocators
    url = "https://account.my.com/login/?error_code"

    def find_error_title(self):
        error_title_elem = self.find(InvalidAuthLocators.QUERY_ERROR_AUTH_TITLE, timeout=5)
        return error_title_elem.text

    def find_error_text(self):
        error_text_elem = self.find(InvalidAuthLocators.QUERY_ERROR_AUTH_TEXT, timeout=5)
        return error_text_elem.text
