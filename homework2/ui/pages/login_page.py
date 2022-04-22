import allure

from ..data.user_data.static import PASSWORD, EMAIL
from .base_page import BasePage
from ..locators.my_target_locators.static_locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators
    url = 'https://target.my.com/'

    @allure.step("Логинимся")
    def login(self, password=PASSWORD, email=EMAIL):
        self.get_drive()
        self.search_click(LoginPageLocators.QUERY_LOGIN_BUTTON_HEAD)
        self.search_insert(LoginPageLocators.QUERY_LOGIN, email, timeout=5)
        self.search_insert(LoginPageLocators.QUERY_PASSWORD, password, timeout=5)
        self.search_click(LoginPageLocators.QUERY_LOGIN_BUTTON, timeout=5)
