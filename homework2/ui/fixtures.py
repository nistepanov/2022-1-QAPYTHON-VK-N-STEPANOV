import os
import sys
import shutil

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from homework2.ui.pages import LoginPage, AuthInvalidPage, MainPage, CampaignPage, SegmentsPage
from homework2.ui.data.user_data.static import URL
from homework2.conftest import config, temp_dir


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def file_path(repo_root):
    return os.path.join(repo_root, 'data', 'scrudge.png')


@pytest.fixture()
def url():
    return URL


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '98.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            desired_capabilities=capabilities
        )
    else:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture()
def auth_invalid_page(driver):
    return AuthInvalidPage(driver=driver)


@pytest.fixture()
def main_page(login_page, driver):
    login_page.login()
    return MainPage(driver=driver)


@pytest.fixture()
def campaign_page(driver):
    return CampaignPage(driver=driver)


@pytest.fixture()
def segments_page(driver):
    return SegmentsPage(driver=driver)
