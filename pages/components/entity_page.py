from core import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import TimeoutException
from pages.components.modals import Modals
from api.api import ApiClasses
from api.api import ApiModels
from variables import PkmVars as Vars
import time


class EntityPage(BasePage):
    LOCATOR_ENTITY_PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'title-value')]")
    LOCATOR_PAGE_TITLE_BLOCK = (By.XPATH, "//div[@class='page-title-container']//div[@class='title-value']")
    LOCATOR_TITLE_INPUT = (By.XPATH, "(//div[@class='page-title-container']//input)[1]")
    LOCATOR_TITLE_CHECK_ICON = (By.XPATH, "//div[@class='page-title-container']//fa-icon[@icon='check']")

    @staticmethod
    def add_list_element_button_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and text()=' {list_name} '] ]//fa-icon[@icon='plus']")
        return locator

    @staticmethod
    def list_element_creator(list_name, element_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and text()=' {list_name} '] ]//div[contains(@class, 'list-item ') and .=' {element_name} ']")
        return locator

    @staticmethod
    def list_elements_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and text()=' {list_name} '] ]//div[contains(@class, 'list-item ')]")
        return locator

    @staticmethod
    def list_element_rename_button_creator(list_name, element_name):
        element_xpath = EntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='edit']")
        return locator

    @staticmethod
    def list_element_delete_button_creator(list_name, element_name):
        element_xpath = EntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='trash']")
        return locator

    def get_entity_page_title(self):
        title = self.get_element_text(self.LOCATOR_ENTITY_PAGE_TITLE)
        return title

    def rename_title(self, title_name):
        action = ActionChains(self.driver)
        self.find_and_click(self.LOCATOR_PAGE_TITLE_BLOCK)
        title_input = self.find_element(self.LOCATOR_TITLE_INPUT)
        action.double_click(title_input).perform()
        title_input.send_keys(Keys.DELETE)
        title_input.send_keys(title_name)
        self.find_and_click(self.LOCATOR_TITLE_CHECK_ICON)
        actual_title_name = (self.get_element_text(self.LOCATOR_PAGE_TITLE_BLOCK))
        assert actual_title_name == title_name.upper()
        time.sleep(2)
