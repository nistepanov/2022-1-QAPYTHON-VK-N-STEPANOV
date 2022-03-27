import allure
from selenium.webdriver import ActionChains

from .base_page import BasePage
from ..locators.my_target_locators.static_locators import CampaignPageLocators


class CampaignPage(BasePage):
    locators = CampaignPageLocators
    url = 'https://target.my.com/campaign/new'

    @allure.step('Выбираем кампанию "Траффик"')
    def select_traffic_campaign(self):
        self.search_click(CampaignPageLocators.QUERY_TRAFFIC_BUTTON, timeout=30)

    @allure.step('Заполняем ссылку на кампанию')
    def insert_link_in_template_campaign(self):
        self.search_insert(CampaignPageLocators.QUERY_PLACEHOLDER_LINK, 'https://target.my.com/', timeout=10)

    @allure.step('Выбираем компанию баннер')
    def select_banner_campaign(self):
        self.search_click(CampaignPageLocators.QUERY_BANNER_BUTTON, timeout=40)

    @allure.step('Скроллим до превью')
    def move_to_image_preview_area(self):
        actions = ActionChains(self.driver)
        preview_area = self.find(CampaignPageLocators.QUERY_IMAGE_PREVIEW, timeout=30)
        actions.move_to_element(preview_area).perform()

    @allure.step('Грузим картинку')
    def upload_image(self, file_path):
        self.find_presence(CampaignPageLocators.QUERY_UPLOAD_IMAGE_BUTTON, timeout=30).send_keys(file_path)

    @allure.step('Генерим рандомное имя кампании')
    def insert_name_of_campaign(self, name):
        self.search_insert(CampaignPageLocators.QUERY_INPUT_NAME_CAMPAIGN, name)

    def click_button_create_campaign(self):
        self.search_click(CampaignPageLocators.QUERY_BUTTON_CREATE_CAMPAIGN)

    def wait_for_visible_work_area(self):
        self.find(CampaignPageLocators.QUERY_WORK_AREA, timeout=30)