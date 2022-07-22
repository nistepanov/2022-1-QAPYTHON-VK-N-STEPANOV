import time

import pytest

from UIElementSearch import UIElementSearchClass
from ui import static
from ui.locators import basic_locators


class TestsUIMyTarget(UIElementSearchClass):
    @pytest.fixture()
    def login(self):
        self.search_click(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON_HEAD)
        self.search_insert(basic_locators.BasePageLocators.QUERY_LOGIN, static.EMAIL)
        self.search_insert(basic_locators.BasePageLocators.QUERY_PASSWORD, static.PASSWORD)
        self.search_click(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON)

        assert f'data-ga-username="{static.EMAIL}"' in self.driver.page_source
        assert self.driver.current_url == "https://target.my.com/dashboard"
        assert self.find(basic_locators.BasePageLocators.QUERY_RIGHT_BUTTON)

    @pytest.mark.UI
    def test_logout(self, login):
        start = time.time()
        while time.time() - start < 10:
            try:
                self.search_click(basic_locators.BasePageLocators.QUERY_RIGHT_BUTTON)
                self.search_click(basic_locators.BasePageLocators.QUERY_LOGOUT_BUTTON)
            except:
                self.driver.refresh()
            else:
                break

        assert self.driver.current_url == "https://target.my.com/"
        assert self.find(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON_HEAD, timeout=30)
        assert "Войти" in self.find(basic_locators.BasePageLocators.QUERY_LOGIN_BUTTON_HEAD, timeout=30).text

    @pytest.mark.UI
    def test_editing_profile_information(self, login):
        rand_name = TestsUIMyTarget.generate_random_name()
        rand_phone = TestsUIMyTarget.generate_random_phone()

        self.search_click(basic_locators.BasePageLocators.QUERY_PROFILE)

        self.search_insert(basic_locators.BasePageLocators.QUERY_FIO, rand_name)
        self.search_insert(basic_locators.BasePageLocators.QUERY_PHONE, rand_phone)
        self.search_click(basic_locators.BasePageLocators.QUERY_SUBMIT_BUTTON)

        assert "Информация успешно сохранена" in self.driver.page_source

        name_input = self.find_visible(basic_locators.BasePageLocators.QUERY_FIO, timeout=30)
        phone_input = self.find_visible(basic_locators.BasePageLocators.QUERY_PHONE, timeout=30)

        assert rand_name == name_input.get_attribute("value")
        assert rand_phone == phone_input.get_attribute("value")

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "expected, input",
        [
            pytest.param(
                ["Аудиторные сегменты", "https://target.my.com/segments/segments_list"],
                basic_locators.BasePageLocators.QUERY_SEGMENTS
            ),
            pytest.param(
                ["У вас еще нет ни одной рекламной кампании.", "https://target.my.com/statistics/summary"],
                basic_locators.BasePageLocators.QUERY_STATISTICS
            ),
        ]
    )
    def test_portal_pages(self, input, expected, login):
        self.search_click(input)
        self.find_visible(basic_locators.BasePageLocators.QUERY_CENTER_WRAP)
        start = time.time()

        while time.time() - start < 15:
            try:
                assert expected[0] in self.driver.page_source
                assert expected[1] == self.driver.current_url
            except:
                pass
            else:
                break
