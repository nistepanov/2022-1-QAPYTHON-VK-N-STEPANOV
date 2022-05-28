from selenium.webdriver.common.by import By


class AuthPageLocators:
    QUERY_PLACEHOLDER_USER_NAME = (By.XPATH, '//input[contains(@placeholder, "Username")]')
    QUERY_PLACEHOLDER_PASSWORD = (By.XPATH, '//input[contains(@placeholder, "Password")]')
    QUERY_BUTTON_SUBMIT_AUTH = (By.XPATH, '//input[@type="submit"]')
    QUERY_LOGIN = (By.XPATH, "//a[starts-with(@href, '/reg')]")
    QUERY_INVALID_AUTH = (By.XPATH, "//div[contains(text(), 'Invalid username or password')]")


class RegistrationPageLocators:
    QUERY_PLACEHOLDER_NAME = (By.XPATH, '//input[contains(@placeholder, "Name")]')
    QUERY_PLACEHOLDER_SURNAME = (By.XPATH, '//input[contains(@placeholder, "Surname")]')
    QUERY_PLACEHOLDER_MIDDLE_NAME = (By.XPATH, '//input[contains(@placeholder, "Midddleename")]')
    QUERY_PLACEHOLDER_USER_NAME = (By.XPATH, '//input[contains(@placeholder, "Username")]')
    QUERY_PLACEHOLDER_EMAIL = (By.XPATH, '//input[contains(@placeholder, "Email")]')
    QUERY_PLACEHOLDER_PASSWORD = (By.XPATH, '//input[contains(@placeholder, "Password")]')
    QUERY_PLACEHOLDER_REPEAT_PASSWORD = (By.XPATH, '//input[contains(@placeholder, "Repeat password")]')
    QUERY_CHECK_BOX = (By.XPATH, '//input[@type="checkbox"]')
    QUERY_BUTTON_SUBMIT_REGISTER = (By.XPATH, '//input[@type="submit"]')
    QUERY_LOGIN = (By.XPATH, "//a[starts-with(@href, '/login')]")
    QUERY_INCORRECT_EMAIL_LENGTH = (By.XPATH, "//div[contains(text(), 'Incorrect email length')]")
    QUERY_PASSWORDS_MUST_MATCH = (By.XPATH, "//div[contains(text(), 'Passwords must match')]")
    QUERY_USER_ALREADY_EXISTS = (By.XPATH, "//div[contains(text(), 'User already exist')]")
    QUERY_EMAIL_ALREADY_EXISTS = (By.XPATH, "//div[contains(text(), 'Internal Server Error')]")
    QUERY_EMAIL_INVALID = (By.XPATH, "//div[contains(text(), 'Invalid email address')]")
    QUERY_PAGE_AVAILABLE_TO_AUTH_USER = (By.XPATH, "//div[contains(text(), 'This page is available')]")


class WelcomePageLocators:
    QUERY_NAV_BAR_BUG = (By.XPATH, ' //a[contains(@class, "uk-navbar-brand")]')
    QUERY_NAV_BAR_HOME = (By.XPATH, "//a[contains(text(), 'HOME')]")
    QUERY_NAV_BAR_PYTHON = (By.XPATH, "//a[starts-with(@href, 'https://www.python.org/')]")
    QUERY_NAV_BAR_PYTHON_HISTORY = (By.XPATH, "//a[contains(text(), 'Python history')]")
    QUERY_NAV_BAR_ABOUT_FLASK = (By.XPATH, "//a[contains(text(), 'About Flask')]")
    QUERY_NAV_BAR_LINUX = (By.XPATH, "//a[contains(text(), 'Linux')]")
    QUERY_NAV_BAR_CENTOS = (By.XPATH, "//a[contains(text(), 'Download Centos7')]")
    QUERY_NAV_BAR_NETWORK = (By.XPATH, "//a[contains(text(), 'Network')]")
    QUERY_NAV_BAR_NEWS = (By.XPATH, "//a[contains(text(), 'News')]")
    QUERY_NAV_BAR_WIRESHARK_DOWNLOAD = (By.XPATH, "//a[@href='https://www.wireshark.org/#download']")
    QUERY_NAV_BAR_EXAMPLES = (By.XPATH, "//a[contains(text(), 'Examples')]")
    QUERY_LOGGED_AS = (By.XPATH, "//li[contains(text(), 'Logged as')]")
    QUERY_USER = (By.XPATH, "//li[contains(text(), 'User')]")
    QUERY_VK_ID = (By.XPATH, "//li[contains(text(), 'VK')]")
    QUERY_BUTTON_LOGOUT = (By.XPATH, "//a[starts-with(@href, '/logout')]")
    QUERY_IMAGE_LAPTOP = (By.XPATH, '//img[@src="/static/images/laptop.png"]')
    QUERY_IMAGE_LOOP = (By.XPATH, '//img[@src="/static/images/loupe.png"]')
    QUERY_IMAGE_SMTP = (By.XPATH, '//img[@src="/static/images/analytics.png"]')
    QUERY_FACT = (By.XPATH, "//div[starts-with(@class, 'uk-text-center uk-text-large')]//child::p")
