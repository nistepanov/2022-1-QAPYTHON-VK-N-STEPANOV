import random
import string

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UIElementSearchClass:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        self.wait(timeout).until(EC.presence_of_element_located(
            locator))
        return self.wait(timeout).until(EC.visibility_of_element_located(
            locator))

    def search_insert(self, locator, query, timeout=None):
        self.find(locator).clear()
        elem = self.wait(timeout).until(EC.element_to_be_clickable(
            locator))
        elem.send_keys(query)

    def search_click(self, locator, timeout=None):
        self.find(locator)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(
            locator))
        elem.click()

    @staticmethod
    def generate_random_name(length=random.randint(5, 10)):
        letters = string.ascii_lowercase
        rand_name = ''.join(random.sample(letters, length))
        return rand_name

    @staticmethod
    def generate_random_phone():
        letters = string.digits
        rand_phone = ''.join(random.sample(letters, 10))
        return '+7' + rand_phone
