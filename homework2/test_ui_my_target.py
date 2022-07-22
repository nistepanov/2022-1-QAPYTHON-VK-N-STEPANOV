import allure

from base import BaseCase, BaseCaseLogin
from homework2.ui.fixtures import *
from homework2.ui.tools.random_generate import RandomGenerate

MAX_RETRY_COUNT = 3


class TestAuthInvalid(BaseCaseLogin):
    @pytest.mark.UI
    def test_invalid_email(self, setup):
        self.login_page.login(email=RandomGenerate.generate_random_email())

        self.auth_invalid_page.is_opened()

        assert "Error" == self.auth_invalid_page.find_error_title()
        assert "Invalid login or password" == self.auth_invalid_page.find_error_text()

    @pytest.mark.UI
    def test_invalid_password(self, setup):
        self.login_page.login(password=RandomGenerate.generate_random_password())

        self.auth_invalid_page.is_opened()

        assert "Error" == self.auth_invalid_page.find_error_title()
        assert "Invalid login or password" == self.auth_invalid_page.find_error_text()


class TestCampaign(BaseCase):

    @pytest.mark.UI
    def test_create_traffic_campaign(self, setup, file_path):
        self.main_page.is_opened()
        self.main_page.go_to_create_campaign()

        self.campaign_page.is_opened()

        self.campaign_page.fill_traffic_campaign_data(file_path)

        assert self.campaign_page.campaign_name == self.campaign_page.search_name_of_previously_created_campaign()
        assert "https://target.my.com/dashboard#" == self.driver.current_url


class TestSegments(BaseCase):

    @pytest.mark.UI
    def test_create_segment(self, setup):
        self.main_page.is_opened()
        self.main_page.go_to_segments()

        self.segments_page.is_opened()

        count_segments_before_adding_segment = int(self.segments_page.count_segments_at_cur_time())

        self.segments_page.create_segment(count_segments_before_adding_segment)

        count_segments_after_adding_segment = int(self.segments_page.count_segments_at_cur_time())

        assert self.segments_page.segment_name == self.segments_page.search_name_of_previously_created_segment(
            self.segments_page.segment_name)
        assert count_segments_after_adding_segment == count_segments_before_adding_segment + 1

        self.segments_page.delete_segment_by_click_on_cross()

    @pytest.mark.UI
    def test_delete_segment_by_click_on_cross(self, setup):
        self.main_page.is_opened()
        self.main_page.go_to_segments()

        self.segments_page.is_opened()

        count_segments_before_delete = int(self.segments_page.count_segments_at_cur_time())

        self.segments_page.create_segment(count_segments_before_delete)

        self.segments_page.delete_segment_by_click_on_cross()

        with allure.step("Ждем прогрузки поля с кол-вом активных сегментов"):
            count = 0
            while count < MAX_RETRY_COUNT:
                try:
                    count += 1
                    count_segments_after_delete = int(self.segments_page.count_segments_at_cur_time())

                    assert count_segments_before_delete - count_segments_after_delete == 1
                except AssertionError:
                    pass
                else:
                    break
        assert "https://target.my.com/segments/segments_list" == self.driver.current_url

    @pytest.mark.UI
    def test_delete_segment_by_click_on_checkbox(self, setup):
        self.main_page.is_opened()
        self.main_page.go_to_segments()

        self.segments_page.is_opened()

        count_segments_before_delete = int(self.segments_page.count_segments_at_cur_time())

        self.segments_page.create_segment(count_segments_before_delete)

        self.segments_page.delete_segment_by_click_on_checkbox()

        with allure.step("Ждем прогрузки поля с кол-вом активных сегментов"):
            count = 0
            while count < MAX_RETRY_COUNT:
                try:
                    count += 1
                    count_segments_after_delete = int(self.segments_page.count_segments_at_cur_time())

                    assert count_segments_before_delete - count_segments_after_delete == 1
                except AssertionError:
                    pass
                else:
                    break

        assert "https://target.my.com/segments/segments_list" == self.driver.current_url
