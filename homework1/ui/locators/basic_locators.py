from selenium.webdriver.common.by import By


class BasePageLocators:
    QUERY_LOGIN_BUTTON_HEAD = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
    QUERY_LOGIN = (By.XPATH, '//input[contains(@class, "authForm-module-input")]')
    QUERY_PASSWORD = (By.XPATH, '//input[contains(@class, "authForm-module-inputPassword")]')
    QUERY_LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
    QUERY_RIGHT_BUTTON = (By.XPATH, '//div[contains(@class, "right-module-rightWrap")]')
    QUERY_LOGOUT_BUTTON = (By.XPATH, "//a[contains(@class, 'rightMenu-module') and @href='/logout']/parent::li")
    QUERY_PROFILE = (By.XPATH, '//a[starts-with(@href, "/profile")]')
    QUERY_FIO = (By.XPATH, '//div[contains(@data-name, "fio")]//child::input')
    QUERY_PHONE = (By.XPATH, '//div[contains(@data-name, "phone")]//child::input')
    QUERY_SUBMIT_BUTTON = (By.XPATH, '//button[contains(@class, "button button_submit")]')
    QUERY_SEGMENTS = (By.XPATH, '//a[starts-with(@href, "/segments")]')
    QUERY_STATISTICS = (By.XPATH, '//a[starts-with(@href, "/statistics")]')
    QUERY_CENTER_WRAP = (By.XPATH, '//div[contains(@class, "page__layout page__layout_float")]')
