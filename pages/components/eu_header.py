from core import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import TimeoutException
from pages.components.modals import Modals
from api.api import ApiClasses
from api.api import ApiModels


class EuHeader(BasePage):
    LOCATOR_EU_PAGE_TITLE = (By.XPATH, "//div[@class='user-menu-page-title']")
    LOCATOR_EU_USER_MENU = (By.XPATH, "//div[contains(@class, 'user-menu ')]")
    LOCATOR_EU_MENU_BUTTON = (By.XPATH, "//fa-icon[contains(@class, 'menu-button')]")

    def get_title_text(self):
        text = self.get_element_text(self.LOCATOR_EU_PAGE_TITLE, time=15)
        return text

    def open_menu(self):
        self.find_and_click(self.LOCATOR_EU_MENU_BUTTON)
        assert self.find_element(self.LOCATOR_EU_USER_MENU, time=5), 'Невозможно открыть меню'

    def navigate_to_page(self, page_name):
        title = self.get_title_text()
        if title == page_name.upper():
            pass
        else:
            self.open_menu()
            button = (By.XPATH, f"//div[contains(@class, 'menu-item ') and text() = ' {page_name} ']")
            self.find_and_click(button)
            self.wait_until_text_in_element(self.LOCATOR_EU_PAGE_TITLE, page_name.upper())
