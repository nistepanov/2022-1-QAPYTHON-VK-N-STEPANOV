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

    def create_segment_button(self, flag):
        if flag == "segment exists":
            self.search_click(SegmentsPageLocators.QUERY_CREATE_SEGMENT_BUTTON, timeout=40)
        elif flag == "segment not exists":
            self.search_click(SegmentsPageLocators.QUERY_CREATE_SEGMENT_LINK, timeout=40)

    def select_active_segment(self):
        self.search_click(SegmentsPageLocators.QUERY_ACTIVE_SEGMENT)

    @allure.step("Нажимаем на галочку выбора сегмента")
    def insert_checkbox(self):
        self.search_click(SegmentsPageLocators.QUERY_CHECKBOX)

    @allure.step("Заполняем рандомным именем сегмент")
    def insert_segment_name(self, name):
        self.search_insert(SegmentsPageLocators.QUERY_ADD_NAME_SEGMENT, name, timeout=15)

    @allure.step("Добавляем сегмент")
    def add_segment(self):
        self.search_click(SegmentsPageLocators.QUERY_ADD_SEGMENT)

    def wait_for_table_segments(self):
        self.find(SegmentsPageLocators.QUERY_TABLE_SEGMENTS)

    @allure.step("Кликам на крестик для удаления")
    def click_on_cross(self):
        self.search_click(SegmentsPageLocators.QUERY_SEGMENT_CROSS, timeout=15)

    @allure.step("Выбираем сегмент для удаления")
    def click_on_checkbox(self):
        self.search_click(SegmentsPageLocators.QUERY_SEGMENTS_CHECKBOX)

    @allure.step("Подтверждаем удаление сегмента")
    def click_on_button_confirm_delete_segment(self):
        self.search_click(SegmentsPageLocators.QUERY_BUTTON_CONFIRM_DELETE_SEGMENT)

    @allure.step('Ищем в таблице сегментов ранее созданный сегмент')
    def search_name_of_previously_created_segment(self, segment_name):
        QUERY_PREVIOUSLY_CREATED_SEGMENT = (By.XPATH, f"//a[text()='{segment_name}']")
        return self.find(QUERY_PREVIOUSLY_CREATED_SEGMENT, timeout=20).text

    @allure.step('Создаем сегмент. Setup для тестов удаления сегмента')
    def create_segment_for_test(self):
        self.is_opened()
        count_segments_before_adding_segment = int(self.count_segments_at_cur_time())
        if count_segments_before_adding_segment > 0:
            self.create_segment_button("segment exists")
        elif count_segments_before_adding_segment == 0:
            self.create_segment_button("segment not exists")
        self.insert_checkbox()

        self.add_segment()

        segment_name = RandomGenerate.generate_random_name()

        self.insert_segment_name(name=segment_name)
        self.create_segment_button("segment exists")

    @allure.step("Удаляем ранее созданный сегмент. Подчищаем тестовый стенд")
    def delete_previously_created_segment(self):
        self.is_opened()
        self.click_on_cross()
        self.click_on_button_confirm_delete_segment()

    def wait_for_list_of_segments(self):
        self.find(SegmentsPageLocators.QUERY_LIST_SEGMENTS)

    def click_on_button_actions(self):
        self.search_click(SegmentsPageLocators.QUERY_BUTTON_ACTIONS)

    def remove_segment_by_actions(self):
        self.search_click(SegmentsPageLocators.QUERY_REMOVE_SEGMENT_BUTTON_ACTIONS)
