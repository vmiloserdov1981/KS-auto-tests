from core import BasePage
from selenium.webdriver.common.by import By
import time
from variables import PkmVars as Vars


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


