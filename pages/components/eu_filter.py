from core import BasePage
from selenium.webdriver.common.by import By
import time
from variables import PkmVars as Vars
from selenium.common.exceptions import TimeoutException


class EuFilter(BasePage):
    LOCATOR_SHOW_EMPTY_EVENTS_TOGGLE = (By.XPATH, "//div[@class='slide-content' and text()=' Отображать незаполненные мероприятия ']//preceding-sibling::div[contains(@class, 'slide')]")
    LOCATOR_SHOW_EMPTY_EVENTS_ONLY_TOGGLE = (By.XPATH, "//div[@class='slide-content' and text()=' Только незаполненные мероприятия ']//preceding-sibling::div[contains(@class, 'slide')]")

    def is_show_empty_events(self):
        toggle = self.find_element(self.LOCATOR_SHOW_EMPTY_EVENTS_TOGGLE)
        if 'slide-selected' in toggle.get_attribute('class'):
            return True
        else:
            return False

    def is_show_empty_events_only(self):
        toggle = self.find_element(self.LOCATOR_SHOW_EMPTY_EVENTS_ONLY_TOGGLE)
        if 'slide-selected' in toggle.get_attribute('class'):
            return True
        else:
            return False

    def switch_on_empty_events(self):
        if self.is_show_empty_events():
            pass
        else:
            self.find_and_click(self.LOCATOR_SHOW_EMPTY_EVENTS_TOGGLE)
            time.sleep(Vars.PKM_USER_WAIT_TIME)

    def switch_off_empty_events(self):
        if self.is_show_empty_events():
            self.find_and_click(self.LOCATOR_SHOW_EMPTY_EVENTS_TOGGLE)
            time.sleep(Vars.PKM_USER_WAIT_TIME)
        else:
            pass

    def switch_on_empty_only_events(self):
        if self.is_show_empty_events_only():
            pass
        else:
            self.find_and_click(self.LOCATOR_SHOW_EMPTY_EVENTS_ONLY_TOGGLE)
            # time.sleep(Vars.PKM_USER_WAIT_TIME)

    def switch_off_empty_only_events(self):
        if self.is_show_empty_events_only():
            self.find_and_click(self.LOCATOR_SHOW_EMPTY_EVENTS_ONLY_TOGGLE)
            # time.sleep(Vars.PKM_USER_WAIT_TIME)
        else:
            pass

    def scroll_to_filter(self, filter_name):
        filter_locator = (By.XPATH, f"//div[text()='{filter_name}']/..")
        filter_block = self.find_element(filter_locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", filter_block)

    def get_filter_values(self, filter_name):
        values = []
        values_locator = (By.XPATH, f"//div[text()='{filter_name}']/..//div[contains(@class, 'multiple-dropdown-value-title')]")
        self.scroll_to_filter(filter_name)
        values_elements = self.driver.find_elements(*values_locator)
        for value in values_elements:
            self.driver.execute_script("arguments[0].scrollIntoView();", value)
            values.append(value.text)
        return values

    def clear_filter_values(self, filter_name):
        self.scroll_to_filter(filter_name)
        close_icons_locator = (By.XPATH, f"//div[text()='{filter_name}']/..//div[contains(@class, 'multiple-dropdown-value ')]//fa-icon[contains(@class, 'multiple-dropdown-value-close')]")
        try:
            self.find_element(close_icons_locator, time=1)
        except TimeoutException:
            return None
        while True:
            try:
                self.find_and_click(close_icons_locator, time=1)
            except TimeoutException:
                return True

    def click_filter_dropdown(self, filter_name):
        self.scroll_to_filter(filter_name)
        dropdown_locator = (By.XPATH, f"//div[text()='{filter_name}']/..//div[contains(@class, 'multiple-dropdown ')]")
        self.find_and_click(dropdown_locator)

    def set_filter(self, filter_name, values):
        self.click_filter_dropdown(filter_name)
        for value in values:
            self.check_value(value)
        self.click_filter_dropdown(filter_name)

    def is_filter_value_checked(self, value_name):
        dropdown_item_locator = (By.XPATH, f"//div[@class='content' and text()=' {value_name} ']//..")
        item = self.find_element(dropdown_item_locator)
        if 'selected' in item.get_attribute('class'):
            return True
        else:
            return False

    def check_value(self, value_name):
        dropdown_item_locator = (By.XPATH, f"//div[@class='content' and text()=' {value_name} ']//..")
        if not self.is_filter_value_checked(value_name):
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(dropdown_item_locator))
            self.find_and_click(dropdown_item_locator)
        else:
            pass

    def uncheck_value(self, value_name):
        dropdown_item_locator = (By.XPATH, f"//div[@class='content' and text()=' {value_name} ']//..")
        if self.is_filter_value_checked(value_name):
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(dropdown_item_locator))
            self.find_and_click(dropdown_item_locator)
        else:
            pass






