from selenium.webdriver.common.by import By


class LoginPageLocators:
    QUERY_LOGIN_BUTTON_HEAD = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
    QUERY_LOGIN = (By.XPATH, '//input[contains(@class, "authForm-module-input")]')
    QUERY_PASSWORD = (By.XPATH, '//input[contains(@class, "authForm-module-inputPassword")]')
    QUERY_LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')


class InvalidAuthLocators:
    QUERY_ERROR_AUTH_TITLE = (By.XPATH, '//div[contains(@class, "formMsg_title")]')
    QUERY_ERROR_AUTH_TEXT = (By.XPATH, '//div[contains(@class, "formMsg_text")]')


class MainPageLocators:
    QUERY_RIGHT_BUTTON = (By.XPATH, '//div[contains(@class, "right-module-rightWrap")]')
    QUERY_LOGOUT_BUTTON = (By.XPATH, "//a[contains(@class, 'rightMenu-module') and @href='/logout']/parent::li")
    QUERY_PROFILE = (By.XPATH, '//a[starts-with(@href, "/profile")]')
    QUERY_FIO = (By.XPATH, '//div[contains(@data-name, "fio")]//child::input')
    QUERY_PHONE = (By.XPATH, '//div[contains(@data-name, "phone")]//child::input')
    QUERY_SUBMIT_BUTTON = (By.XPATH, '//button[contains(@class, "button_submit")]')
    QUERY_STATISTICS = (By.XPATH, '//a[starts-with(@href, "/statistics")]')
    QUERY_CENTER_WRAP = (By.XPATH, '//div[contains(@class, "page__layout_float")]')
    QUERY_CAMPAIGN_BUTTON = (By.XPATH, '//div[contains(@class, "button-module-textWrapper")]')
    QUERY_SEGMENTS_BUTTON = (By.XPATH, '//a[starts-with(@href, "/segments")]')


class CampaignPageLocators:
    QUERY_TRAFFIC_BUTTON = (By.XPATH, '//div[contains(@class, "_traffic")]')
    QUERY_PLACEHOLDER_LINK = (By.XPATH, '//input[contains(@placeholder, "Введите ссылку")]')
    QUERY_BANNER_BUTTON = (By.XPATH, '//span[contains(@class, "banner-format-item__title") '
                                     'and contains(text(), "Баннер")]')
    QUERY_IMAGE_PREVIEW = (By.XPATH, '//div[contains(@class, "imagePreview-module-dropArea")]')
    QUERY_UPLOAD_IMAGE_BUTTON = (By.XPATH, "//input[contains(@type, 'file') and contains(@data-test, 'image_240x400')]")
    QUERY_INPUT_NAME_CAMPAIGN = (By.XPATH, '//div[contains(@class, "input__wrap")]/input')
    QUERY_BUTTON_CREATE_CAMPAIGN = (By.XPATH, '//div[contains(text(), "Создать кампанию")]')
    QUERY_WORK_AREA = (By.XPATH, '//div[contains(@class, "layout-module-pageBody")]')


class SegmentsPageLocators:
    QUERY_COUNT_SEGMENTS = (By.XPATH, '//span[contains(@class, "js-nav-item-count")]')
    QUERY_CREATE_SEGMENT_BUTTON = (By.CSS_SELECTOR, 'div.button__text')
    QUERY_CREATE_SEGMENT_LINK = (By.XPATH, "//a[@href='/segments/segments_list/new/']")
    QUERY_ACTIVE_SEGMENT = (By.XPATH, '//div[contains(@class, "adding-segments-item_active")]')
    QUERY_CHECKBOX = (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox")]')
    QUERY_ADD_SEGMENT = (By.XPATH, '//div[contains(@class, "adding-segments-modal__btn-wrap")]')
    QUERY_ADD_NAME_SEGMENT = (By.XPATH, '//div[contains(@class, "input_create-segment-form")]//child::input')
    QUERY_TABLE_SEGMENTS = (By.XPATH, '//div[contains(@class, "header-module-noWrap")]')
    QUERY_SEGMENT_CROSS = (By.XPATH, '//span[contains(@class, "cells-module-removeCell")]')
    QUERY_BUTTON_CONFIRM_DELETE_SEGMENT = (By.XPATH, '//button[contains(@class, "button_confirm-remove")]')
    QUERY_LIST_SEGMENTS = (By.XPATH, "//a[@href='/segments/segments_list']")
    QUERY_SEGMENTS_CHECKBOX = (By.XPATH, '//input[@type="checkbox"]')
    QUERY_BUTTON_ACTIONS = (By.XPATH, "//div[contains(@class, 'select-module-selectWrap')]")
    QUERY_REMOVE_SEGMENT_BUTTON_ACTIONS = (By.XPATH, "//li[contains(@class, 'optionsList-module-option')]")
