import allure

from locators.static_locators import RegistrationPageLocators
from pages.base_page import BasePage
from final_project.code.settings.config import APP_HOST, APP_PORT


class RegistrationPage(BasePage):
    url = f'http://{APP_HOST}:{APP_PORT}/reg'

    @allure.step("Попытка зарегистрироваться")
    def registration(self, data, middle_name_option=0, empty_rep_password_option=0, rep_password=0,
                     checkbox_option=1):
        self.get_drive()
        try:
            self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_USER_NAME, data["username"])
            self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_PASSWORD, data["password"])
            if not empty_rep_password_option:
                self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_REPEAT_PASSWORD, data["password"])
            else:
                self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_REPEAT_PASSWORD, rep_password)
            if middle_name_option:
                self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_MIDDLE_NAME, data["middle_name"])
            self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_NAME, data["name"])
            self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_SURNAME, data["surname"])
            self.search_insert(RegistrationPageLocators.QUERY_PLACEHOLDER_EMAIL, data["email"])
        except:
            pass
        if checkbox_option:
            self.search_click(RegistrationPageLocators.QUERY_CHECK_BOX)
        self.search_click(RegistrationPageLocators.QUERY_BUTTON_SUBMIT_REGISTER)

    @allure.step("Смотрим pop-up validationMessage при пустом поле")
    def find_pop_up_empty_req_field(self, locator):
        elem = self.find(locator)
        message = elem.get_attribute('validationMessage')

        return message

    @allure.step("Смотрим pop-up text при пустом поле ")
    def find_pop_up_text(self, locator):
        elem = self.find(locator)

        return elem.text


