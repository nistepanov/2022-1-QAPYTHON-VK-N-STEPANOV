from .base_page import BasePage
from ..locators.my_target_locators.static_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators
    url = 'https://target.my.com/dashboard'

    def go_to_create_campaign(self):
        self.search_click(MainPageLocators.QUERY_CAMPAIGN_BUTTON, timeout=15)

    def go_to_segments(self):
        self.search_click(MainPageLocators.QUERY_SEGMENTS_BUTTON, timeout=40)
