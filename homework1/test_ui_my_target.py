import pytest

from ui.locators import basic_locators
from ui import static
from UIElementSearch import UIElementSearchClass


class TestsUIMyTarget(UIElementSearchClass):
    @pytest.fixture()
    def login(self):
        self.search_click(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON_HEAD)
        self.search_insert(basic_locators.BasePageLocators.QUERY_LOGIN, static.EMAIL, timeout=5)
        self.search_insert(basic_locators.BasePageLocators.QUERY_PASSWORD, static.PASSWORD, timeout=5)
        self.search_click(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON, timeout=5)

    @pytest.mark.UI
    def test_login(self, login):

        assert f'data-ga-username="{static.EMAIL}"' in self.driver.page_source
        assert self.find(basic_locators.BasePageLocators.QUERY_RIGHT_BUTTON, timeout=5)

    @pytest.mark.UI
    def test_logout(self, login):
        while 1:
            try:
                self.search_click(basic_locators.BasePageLocators.QUERY_RIGHT_BUTTON)
                self.search_click(basic_locators.BasePageLocators.QUERY_LOGOUT_BUTTON)
            except:
                self.driver.refresh()
            else:
                break

        assert self.find(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON_HEAD, timeout=20)
        assert "Войти" in self.find(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON_HEAD, timeout=20).text

    @pytest.mark.UI
    def test_editing_profile_information(self, login):
        rand_name = TestsUIMyTarget.generate_random_name()
        rand_phone = TestsUIMyTarget.generate_random_phone()

        while 1:
            try:
                self.search_click(basic_locators.BasePageLocators.QUERY_PROFILE)
            except:
                self.driver.refresh()
            else:
                break

        self.find(basic_locators.BasePageLocators.QUERY_FIO).clear()
        self.search_insert(basic_locators.BasePageLocators.QUERY_FIO, rand_name, timeout=5)
        self.find(basic_locators.BasePageLocators.QUERY_PHONE).clear()
        self.search_insert(basic_locators.BasePageLocators.QUERY_PHONE, rand_phone, timeout=5)
        self.search_click(basic_locators.BasePageLocators.QUERY_SUBMIT_BUTTON)

        assert "Информация успешно сохранена" in self.driver.page_source

        self.driver.refresh()
        while 1:
            try:
                name_input = self.find(basic_locators.BasePageLocators.QUERY_FIO, timeout=5)
                phone_input = self.find(basic_locators.BasePageLocators.QUERY_PHONE, timeout=5)
            except:
                pass
            else:
                break

        assert rand_name == name_input.get_attribute("value")
        assert rand_phone == phone_input.get_attribute("value")

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "expected, input",
        [
            pytest.param(
                "Аудиторные сегменты", basic_locators.BasePageLocators.QUERY_SEGMENTS
            ),
            pytest.param(
                "У вас еще нет ни одной рекламной кампании.", basic_locators.BasePageLocators.QUERY_STATISTICS
            ),
        ]
    )
    def test_portal_pages(self, input, expected, login):
        self.search_click(input)
        self.find(basic_locators.BasePageLocators.QUERY_CENTER_WRAP)
        while 1:
            try:
                assert expected in self.driver.page_source
            except:
                pass
            else:
                break
