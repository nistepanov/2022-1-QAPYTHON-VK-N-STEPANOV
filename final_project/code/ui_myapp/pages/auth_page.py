import allure

from locators.static_locators import AuthPageLocators
from pages.base_page import BasePage

from final_project.code.credentials.static import USERNAME, PASSWORD
from final_project.code.settings.config import APP_HOST, APP_PORT


class AuthPage(BasePage):
    url = f'http://{APP_HOST}:{APP_PORT}/login'

    @allure.step("Логинимся")
    def login(self, username=USERNAME, password=PASSWORD):
        self.get_drive()
        self.search_insert(AuthPageLocators.QUERY_PLACEHOLDER_USER_NAME, username)
        self.search_insert(AuthPageLocators.QUERY_PLACEHOLDER_PASSWORD, password)
        self.search_click(AuthPageLocators.QUERY_BUTTON_SUBMIT_AUTH)

    @allure.step("Ищем и проверяем pop-up, уведомляющий о неуспешной авторизации")
    def find_pop_up_invalid_auth_message(self):
        elem = self.find(AuthPageLocators.QUERY_INVALID_AUTH)

        assert elem
        assert elem.text == 'Invalid username or password'

    @allure.step("Ищем и проверяем pop-up, уведомляющий о невалидном поле логина")
    def find_pop_up_invalid_login_message(self):
        elem = self.find(AuthPageLocators.QUERY_PLACEHOLDER_USER_NAME)
        message = elem.get_attribute('validationMessage')

        return message
