import allure
from selenium.webdriver import ActionChains

from locators.static_locators import WelcomePageLocators
from pages.base_page import BasePage
from final_project.code.settings.config import APP_HOST, APP_PORT


class WelcomePage(BasePage):
    url = f'http://{APP_HOST}:{APP_PORT}/welcome/'

    @allure.step('Нажимаем на кнопку с жуком')
    def click_on_image_bug(self):
        fact_text = self.find(WelcomePageLocators.QUERY_FACT).text
        self.search_click(WelcomePageLocators.QUERY_NAV_BAR_BUG)

        return fact_text

    @allure.step('Нажимаем на кнопку HOME')
    def click_on_button_home(self):
        fact_text = self.find(WelcomePageLocators.QUERY_FACT).text
        self.search_click(WelcomePageLocators.QUERY_NAV_BAR_HOME)

        return fact_text

    def click_on_python_history_in_python_button_menu(self):
        actions = ActionChains(self.driver)
        python_button = self.find(WelcomePageLocators.QUERY_NAV_BAR_PYTHON)
        with allure.step('Наводимся на кнопку Python '):
            actions.move_to_element(python_button).perform()

        with allure.step('В выпадающем меню нажимаем на кнопку Python History'):
            self.search_click(WelcomePageLocators.QUERY_NAV_BAR_PYTHON_HISTORY)

    def click_on_about_flask_in_python_button_menu(self):
        actions = ActionChains(self.driver)
        python_button = self.find(WelcomePageLocators.QUERY_NAV_BAR_PYTHON)
        with allure.step('Наводимся на кнопку Python '):
            actions.move_to_element(python_button).perform()
        actions.move_to_element(python_button).perform()

        with allure.step('В выпадающем меню нажимаем на кнопку About Flask'):
            self.search_click(WelcomePageLocators.QUERY_NAV_BAR_ABOUT_FLASK)

    def click_on_download_centos_in_linux_button_menu(self):
        actions = ActionChains(self.driver)
        python_button = self.find(WelcomePageLocators.QUERY_NAV_BAR_LINUX)
        with allure.step('Наводимся на кнопку Linux '):
            actions.move_to_element(python_button).perform()
        actions.move_to_element(python_button).perform()

        with allure.step('В выпадающем меню нажимаем на кнопку Download Centos 7'):
            self.search_click(WelcomePageLocators.QUERY_NAV_BAR_CENTOS)

    def click_on_news_in_network_button_menu(self):
        actions = ActionChains(self.driver)
        python_button = self.find(WelcomePageLocators.QUERY_NAV_BAR_NETWORK)
        with allure.step('Наводимся на кнопку Network '):
            actions.move_to_element(python_button).perform()
        actions.move_to_element(python_button).perform()

        with allure.step('В выпадающем меню нажимаем на кнопку news'):
            self.search_click(WelcomePageLocators.QUERY_NAV_BAR_NEWS)

    def click_on_download_in_network_button_menu(self):
        actions = ActionChains(self.driver)
        python_button = self.find(WelcomePageLocators.QUERY_NAV_BAR_NETWORK)
        with allure.step('Наводимся на кнопку Network '):
            actions.move_to_element(python_button).perform()
        actions.move_to_element(python_button).perform()

        with allure.step('В выпадающем меню нажимаем на кнопку Download'):
            self.search_click(WelcomePageLocators.QUERY_NAV_BAR_WIRESHARK_DOWNLOAD)

    def click_on_examples_in_network_button_menu(self):
        actions = ActionChains(self.driver)
        python_button = self.find(WelcomePageLocators.QUERY_NAV_BAR_NETWORK)
        with allure.step('Наводимся на кнопку Network '):
            actions.move_to_element(python_button).perform()
        actions.move_to_element(python_button).perform()

        with allure.step('В выпадающем меню нажимаем на кнопку Examples'):
            self.search_click(WelcomePageLocators.QUERY_NAV_BAR_EXAMPLES)
