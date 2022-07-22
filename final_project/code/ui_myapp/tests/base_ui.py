import allure
import pytest
from _pytest.fixtures import FixtureRequest

from pages import AuthPage, RegistrationPage, WelcomePage


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, mysql_client_fixture, request: FixtureRequest):
        with allure.step("Выполняем коннект к БД и возвращаем объект соединения"):
            self.mysql = mysql_client_fixture
        self.driver = driver
        self.config = config
        self.logger = logger
        self.auth_page: AuthPage = (request.getfixturevalue('auth_page'))
        self.registration_page: RegistrationPage = (request.getfixturevalue('registration_page'))


class BaseCaseLogin:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, mysql_client_fixture, request: FixtureRequest):
        with allure.step("Выполняем коннект к БД и возвращаем объект соединения"):
            self.mysql = mysql_client_fixture
        self.driver = driver
        self.config = config
        self.logger = logger
        self.auth_page: AuthPage = (request.getfixturevalue('auth_page'))
        self.registration_page: RegistrationPage = (request.getfixturevalue('registration_page'))
        self.welcome_page: WelcomePage = (request.getfixturevalue('welcome_page'))
