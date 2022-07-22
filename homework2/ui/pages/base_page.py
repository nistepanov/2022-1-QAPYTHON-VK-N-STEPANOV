import time

import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PageNotOpenedException(Exception):
    pass


class BasePage(object):
    locators = None
    driver = None
    url = None

    def __init__(self, driver):
        self.driver = driver

    def get_drive(self):
        self.driver.get(self.url)
        self.is_opened()

    @allure.step("Переходим на необходимую страницу")
    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if (self.driver.current_url == self.url) or (self.url in self.driver.current_url):
                return True
        raise PageNotOpenedException(f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 40
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step("Ждем существования и видимости элемента")
    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.visibility_of_element_located(
            locator))

    @allure.step("Ждем существования элемента")
    def find_presence(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(
            locator))

    @allure.step("Очищаем и заполняем поле")
    def search_insert(self, locator, query, timeout=None):
        self.find(locator).clear()
        elem = self.wait(timeout).until(EC.element_to_be_clickable(
            locator))
        started = time.time()
        while time.time() - started < 15:
            try:
                elem.send_keys(query)
            except:
                pass
            else:
                break

    @allure.step("Кликаем по полю")
    def search_click(self, locator, timeout=None) -> WebElement:
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(
            locator))
        started = time.time()
        while time.time() - started < 15:
            try:
                elem.click()
            except:
                pass
            else:
                break
