import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from final_project.code.settings.config import APP_PORT, APP_HOST
from ..pages import RegistrationPage, AuthPage, WelcomePage


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
            f'http://selenoid_hub:4444/wd/hub',
            desired_capabilities=capabilities
        )
    else:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture()
def auth_page(driver):
    return AuthPage(driver=driver)


@pytest.fixture()
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture()
def welcome_page(driver, auth_page):
    auth_page.login()
    return WelcomePage(driver=driver)
