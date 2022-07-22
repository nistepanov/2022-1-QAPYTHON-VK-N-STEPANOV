import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from homework2.ui.pages import LoginPage, AuthInvalidPage, MainPage, CampaignPage, SegmentsPage


class BaseCase:
    driver = None

    @pytest.fixture(scope='function')
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.auth_invalid_page: AuthInvalidPage = (request.getfixturevalue('auth_invalid_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))
        self.campaign_page: CampaignPage = (request.getfixturevalue('campaign_page'))
        self.segments_page: SegmentsPage = (request.getfixturevalue('segments_page'))

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            screenshot = driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)


class BaseCaseLogin(BaseCase):
    @pytest.fixture(scope='function')
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.auth_invalid_page: AuthInvalidPage = (request.getfixturevalue('auth_invalid_page'))
