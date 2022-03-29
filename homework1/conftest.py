import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from ui import static


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(static.URL)

    yield driver
    driver.quit()
