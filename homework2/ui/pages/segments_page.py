import allure
from selenium.webdriver.common.by import By

from .base_page import BasePage
from ..locators.my_target_locators.static_locators import SegmentsPageLocators
from ..tools.random_generate import RandomGenerate


class SegmentsPage(BasePage):
    locators = SegmentsPageLocators
    url = 'https://target.my.com/segments/segments_list'

    @allure.step("Фиксируем сколько активных сегментов на данный момент")
    def count_segments_at_cur_time(self):
        count_segments_elem = self.find(SegmentsPageLocators.QUERY_COUNT_SEGMENTS)
        return count_segments_elem.text

    def create_segment_button(self):
        if self.flag == "segment exists":
            self.search_click(SegmentsPageLocators.QUERY_CREATE_SEGMENT_BUTTON)
        elif self.flag == "segment not exists":
            self.search_click(SegmentsPageLocators.QUERY_CREATE_SEGMENT_LINK)

    @allure.step('Ищем в таблице сегментов ранее созданный сегмент')
    def search_name_of_previously_created_segment(self, segment_name):
        QUERY_PREVIOUSLY_CREATED_SEGMENT = (By.XPATH, f"//a[text()='{segment_name}']")
        return self.find(QUERY_PREVIOUSLY_CREATED_SEGMENT, timeout=20).text

    @allure.step("Удаляем ранее созданный сегмент с помощью нажатия на 'крестик'. Подчищаем тестовый стенд")
    def delete_segment_by_click_on_cross(self):
        self.is_opened()
        self.search_click(SegmentsPageLocators.QUERY_SEGMENT_CROSS, timeout=15)
        self.search_click(SegmentsPageLocators.QUERY_BUTTON_CONFIRM_DELETE_SEGMENT)
        self.find(SegmentsPageLocators.QUERY_TABLE_SEGMENTS)
        self.find(SegmentsPageLocators.QUERY_LIST_SEGMENTS)

    @allure.step("Удаляем ранее созданный сегмент с помощью заполнения чекбокса (галочка). Подчищаем тестовый стенд")
    def delete_segment_by_click_on_checkbox(self):
        self.is_opened()
        self.search_click(SegmentsPageLocators.QUERY_SEGMENTS_CHECKBOX)
        self.search_click(SegmentsPageLocators.QUERY_BUTTON_ACTIONS)
        self.search_click(SegmentsPageLocators.QUERY_REMOVE_SEGMENT_BUTTON_ACTIONS)
        self.find(SegmentsPageLocators.QUERY_TABLE_SEGMENTS)
        self.find(SegmentsPageLocators.QUERY_LIST_SEGMENTS)

    @allure.step("Создаем сегмент")
    def create_segment(self, count_segments):
        if count_segments > 0:
            self.flag = "segment exists"
            self.create_segment_button()
        elif count_segments == 0:
            self.flag = "segment not exists"
            self.create_segment_button()

        self.search_click(SegmentsPageLocators.QUERY_CHECKBOX)
        self.search_click(SegmentsPageLocators.QUERY_ADD_SEGMENT)

        self.segment_name = RandomGenerate.generate_random_name()
        self.search_insert(SegmentsPageLocators.QUERY_ADD_NAME_SEGMENT, self.segment_name)
        print(self.flag)
        self.create_segment_button()
        self.find(SegmentsPageLocators.QUERY_TABLE_SEGMENTS)
