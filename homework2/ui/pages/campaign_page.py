import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from homework2.ui.tools.random_generate import RandomGenerate
from .base_page import BasePage
from ..locators.my_target_locators.static_locators import CampaignPageLocators


class CampaignPage(BasePage):
    locators = CampaignPageLocators
    url = 'https://target.my.com/campaign/new'

    @allure.step('Скроллим до превью кампании')
    def move_to_image_preview_area(self):
        actions = ActionChains(self.driver)
        preview_area = self.find(CampaignPageLocators.QUERY_IMAGE_PREVIEW, timeout=30)
        actions.move_to_element(preview_area).perform()

    @allure.step('Грузим картинку')
    def upload_image(self, file_path):
        self.find_presence(CampaignPageLocators.QUERY_UPLOAD_IMAGE_BUTTON, timeout=30).send_keys(file_path)

    @allure.step('Ищем в таблице кампаний ранее созданную кампанию')
    def search_name_of_previously_created_campaign(self):
        QUERY_PREVIOUSLY_CREATED_CAMPAIGN = (By.XPATH, f"//a[text()='{self.campaign_name}']")
        return self.find(QUERY_PREVIOUSLY_CREATED_CAMPAIGN, timeout=20).text

    @allure.step('Заполняем всю необходимую информацию для типа кампании - Траффик')
    def fill_traffic_campaign_data(self, file_path):
        self.search_click(CampaignPageLocators.QUERY_TRAFFIC_BUTTON)
        self.search_insert(CampaignPageLocators.QUERY_PLACEHOLDER_LINK, 'https://target.my.com/')
        self.search_click(CampaignPageLocators.QUERY_BANNER_BUTTON)
        self.move_to_image_preview_area()
        self.upload_image(file_path)

        self.campaign_name = RandomGenerate.generate_random_name()

        self.search_insert(CampaignPageLocators.QUERY_INPUT_NAME_CAMPAIGN, self.campaign_name)
        self.search_click(CampaignPageLocators.QUERY_BUTTON_CREATE_CAMPAIGN)
        self.find(CampaignPageLocators.QUERY_WORK_AREA)
