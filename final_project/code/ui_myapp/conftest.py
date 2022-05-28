import os

import allure
import pytest

from final_project.code.tools.create_user_info import UserInfo
from final_project.code.ui_myapp.tools.fixtures import *


@allure.title("Создание пользовательских данных (без middle-name)")
@pytest.fixture(scope='function')
def create_user_data_without_middle_name(self):
    user_info = UserInfo()
    user_data = user_info.create_user_data()
    human_data = user_info.create_human_data()
    complex_data = {**user_data, **human_data}
    return complex_data


@allure.title("Создание пользовательских данных (c middle-name)")
@pytest.fixture(scope='function')
def create_user_data_with_middle_name():
    user_info = UserInfo()
    user_data = user_info.create_user_data()
    human_data = user_info.create_human_data(option_middle_name=1)
    complex_data = {**user_data, **human_data}
    return complex_data


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, temp_dir):
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
