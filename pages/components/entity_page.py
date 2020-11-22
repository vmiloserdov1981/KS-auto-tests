from core import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{list_name}'] ]//div[contains(@class, 'list-item ') and .=' {element_name} ']")
        return locator

    @staticmethod
    def class_relation_link_locator_creator(relation_name):
        locator = (By.XPATH,
                   f"//div[@class='list' and .//div[@class='title' and .='Связи'] ]//div[contains(@class, 'list-item')]//relation-arrow[.=' {relation_name} ']")
        return locator

    @staticmethod
    def list_elements_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{list_name}'] ]//div[contains(@class, 'list-item ')]")
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

    @staticmethod
    def dropdown_locator_creator(form_control_name):
        locator = (By.XPATH, f"//pkm-dropdown[@formcontrolname='{form_control_name}']//div[contains(@class, 'dropdown')]")
        return locator

    @staticmethod
    def async_dropdown_locator_creator(form_control_name):
        locator = (By.XPATH, f"//async-dropdown-search[@formcontrolname='{form_control_name}']//div[contains(@class, 'dropdown')]//input")
        return locator

    @staticmethod
    def input_locator_creator(form_control_name):
        locator = (By.XPATH, f"//input[@formcontrolname='{form_control_name}']")
        return locator

    @staticmethod
    def add_entity_button_locator_creator(entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'list-header') and .='{entity_name}']//fa-icon[@icon='plus']")
        return locator

    @staticmethod
    def list_element_edit_button_locator_creator(list_name, element_name):
        element_xpath = EntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='pencil-alt']")
        return locator

    def get_entity_page_title(self, return_raw=False):
        if return_raw:
            title = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
        else:
            title = self.get_element_text(self.LOCATOR_ENTITY_PAGE_TITLE)
        return title

    def rename_title(self, title_name):
        self.find_and_click(self.LOCATOR_PAGE_TITLE_BLOCK)
        title_input = self.find_element(self.LOCATOR_TITLE_INPUT)
        title_input.send_keys(Keys.CONTROL + "a")
        title_input.send_keys(Keys.DELETE)
        title_input.send_keys(title_name)
        self.find_and_click(self.LOCATOR_TITLE_CHECK_ICON)
        actual_title_name = (self.get_element_text(self.LOCATOR_PAGE_TITLE_BLOCK))
        assert actual_title_name == title_name.upper()
        time.sleep(2)

    def get_list_elements_names(self, list_name):
        elements = [element.text for element in self.elements_generator(self.list_elements_creator(list_name), time=1)]
        return elements if elements != [] else None
