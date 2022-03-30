import time

import allure
from selenium.common.exceptions import StaleElementReferenceException

from base import BaseCase, BaseCaseLogin
from homework2.ui.tools.random_generate import RandomGenerate
from homework2.ui.fixtures import *


class TestAuthInvalid(BaseCaseLogin):
    @pytest.mark.UI
    def test_invalid_email(self, setup):
        self.login_page.login(email=RandomGenerate.generate_random_email())

        self.auth_invalid_page.is_opened()

        assert "Error" == self.auth_invalid_page.find_error_title()
        assert "Invalid login or password" == self.auth_invalid_page.find_error_text()
        assert "Invalid login or password" in self.driver.page_source

    @pytest.mark.UI
    def test_invalid_password(self, setup):
        self.login_page.login(password=RandomGenerate.generate_random_password())

        self.auth_invalid_page.is_opened()

        assert "Error" == self.auth_invalid_page.find_error_title()
        assert "Invalid login or password" == self.auth_invalid_page.find_error_text()
        assert "Invalid login or password" in self.driver.page_source


class TestCampaign(BaseCase):

    @pytest.mark.UI
    def test_create_traffic_campaign(self, setup, file_path):
        self.main_page.is_opened()
        self.main_page.go_to_create_campaign()

        self.campaign_page.is_opened()
        self.campaign_page.select_traffic_campaign()

        started = time.time()
        while time.time() - started < 5:
            try:
                self.campaign_page.insert_link_in_template_campaign()
                self.campaign_page.select_banner_campaign()
            except:
                self.driver.refresh()
            else:
                break
        self.campaign_page.move_to_image_preview_area()
        self.campaign_page.upload_image(file_path)

        campaign_name = RandomGenerate.generate_random_name()

        self.campaign_page.insert_name_of_campaign(campaign_name)
        self.campaign_page.click_button_create_campaign()
        self.campaign_page.wait_for_visible_work_area()

        assert campaign_name == self.campaign_page.search_name_of_previously_created_campaign(campaign_name)
        assert "https://target.my.com/dashboard#" == self.driver.current_url


class TestSegments(BaseCase):

    @pytest.mark.UI
    def test_create_segment(self, setup):
        self.main_page.is_opened()
        try:
            self.main_page.go_to_segments()
        except StaleElementReferenceException:
            self.driver.refresh()
            self.main_page.go_to_segments()

        self.segments_page.is_opened()

        count_segments_before_adding_segment = int(self.segments_page.count_segments_at_cur_time())
        if count_segments_before_adding_segment > 0:
            self.segments_page.create_segment_button("segment exists")
        elif count_segments_before_adding_segment == 0:
            self.segments_page.create_segment_button("segment not exists")

        self.segments_page.insert_checkbox()

        self.segments_page.add_segment()

        segment_name = RandomGenerate.generate_random_name()

        self.segments_page.insert_segment_name(name=segment_name)
        self.segments_page.create_segment_button("segment exists")
        self.segments_page.wait_for_table_segments()

        assert segment_name == self.segments_page.search_name_of_previously_created_segment(segment_name)

        count_segments_after_adding_segment = int(self.segments_page.count_segments_at_cur_time())

        assert count_segments_after_adding_segment == count_segments_before_adding_segment + 1

        self.segments_page.delete_previously_created_segment()

    @pytest.mark.UI
    def test_delete_segment_by_click_on_cross(self, setup):
        self.main_page.is_opened()
        self.main_page.go_to_segments()

        self.segments_page.is_opened()

        self.segments_page.create_segment_for_test()
        count_segments_before_delete = int(self.segments_page.count_segments_at_cur_time())
        self.segments_page.click_on_cross()
        self.segments_page.click_on_button_confirm_delete_segment()

        self.segments_page.wait_for_table_segments()
        self.segments_page.wait_for_list_of_segments()

        started = time.time()
        with allure.step("Ждем прогрузки поля с кол-вом активных сегментов"):
            while time.time() - started < 15:
                try:
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

        self.segments_page.create_segment_for_test()
        count_segments_before_delete = int(self.segments_page.count_segments_at_cur_time())

        self.segments_page.click_on_checkbox()
        self.segments_page.click_on_button_actions()
        self.segments_page.remove_segment_by_actions()

        started = time.time()
        while time.time() - started < 5:
            try:
                count_segments_after_delete = int(self.segments_page.count_segments_at_cur_time())
                assert count_segments_before_delete - count_segments_after_delete == 1
            except AssertionError:
                pass
            else:
                break
        assert "https://target.my.com/segments/segments_list" == self.driver.current_url
