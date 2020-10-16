from core import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import TimeoutException
from pages.components.modals import Modals
from api.api import ApiEu
from api.api import ApiModels
from pages.login_po import LoginPage


class EuHeader(BasePage):
    LOCATOR_EU_PAGE_TITLE = (By.XPATH, "//div[@class='user-menu-page-title']")
    LOCATOR_EU_USER_MENU = (By.XPATH, "//div[contains(@class, 'user-menu ')]")
    LOCATOR_EU_MENU_BUTTON = (By.XPATH, "//fa-icon[contains(@class, 'menu-button')]")
    LOCATOR_EU_SELECTED_PLAN_TEXT = (By.XPATH, "//pkm-dropdown[contains(@class, 'plans-dropdown')]//div[contains(@class, 'dropdown')]")
    LOCATOR_EU_PLAN_DROPDOWN = (By.XPATH, "//pkm-dropdown[contains(@class, 'plans-dropdown')]//div[contains(@class, 'dropdown')]")
    LOCATOR_EU_PLAN_DROPDOWN_VALUES = (By.XPATH, "//div[contains(@class, 'dropdown-list')]//pkm-dropdown-item")
    LOCATOR_EU_LOGOUT_BUTTON = (By.XPATH, "//div[contains(@class, 'menu-item') and text()=' Выход ']")

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.login_page = LoginPage(driver)

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

    def logout(self):
        self.open_menu()
        self.find_and_click(self.LOCATOR_EU_LOGOUT_BUTTON)
        self.login_page.find_element(self.login_page.LOCATOR_PKM_LOGIN_TITLE)

    def get_plan_dropdown_placeholder(self):
        value = self.find_element(self.LOCATOR_EU_SELECTED_PLAN_TEXT)
        return value.text

    def expand_plan_dropdown(self):
        dropdown = self.find_element(self.LOCATOR_EU_PLAN_DROPDOWN)
        if 'focused' not in dropdown.get_attribute('class'):
            self.find_and_click(self.LOCATOR_EU_PLAN_DROPDOWN)

    def hide_plan_dropdown(self):
        dropdown = self.find_element(self.LOCATOR_EU_PLAN_DROPDOWN)
        if 'focused' in dropdown.get_attribute('class'):
            self.find_and_click(self.LOCATOR_EU_PLAN_DROPDOWN)

    def get_plan_dropdown_values(self):
        values = []
        self.expand_plan_dropdown()
        dropdown_values = self.driver.find_elements(*self.LOCATOR_EU_PLAN_DROPDOWN_VALUES)
        for value in dropdown_values:
            self.driver.execute_script("arguments[0].scrollIntoView();", value)
            values.append(value.text)
        self.hide_plan_dropdown()
        return values

    def check_plan_dropdown_values(self):
        dropdown_values = self.get_plan_dropdown_values()
        api = self.api_creator.get_api_eu()
        plan_names = api.api_get_plans(names_only=True)
        assert self.compare_lists(dropdown_values, plan_names), 'В дропдауне версий отображаются не все планы'

    def select_plan(self, plan_uuid=None, plan_name=None):
        self.expand_plan_dropdown()
        if plan_uuid:
            value_locator = (By.XPATH, f"(//div[contains(@class, 'dropdown-list')]//pkm-dropdown-item)[@test-plan-uuid='{plan_uuid}']")
            value = self.find_element(value_locator)
            if plan_name:
                assert value.text == plan_name
            value.click()
        else:
            value_locator = (By.XPATH, f"//div[@class='content' and contains(text(),' {plan_name} ')]/../..")
            value = self.find_element(value_locator)
            if plan_uuid:
                assert value.get_attribute('test-plan-uuid') == plan_uuid
            value.click()
        if plan_name:
            assert self.get_plan_dropdown_placeholder() == plan_name








