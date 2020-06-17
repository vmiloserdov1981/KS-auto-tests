from core import BasePage
from selenium.webdriver.common.by import By
import time
from variables import PkmVars as Vars
from selenium.common.exceptions import TimeoutException


class EuFilter(BasePage):
    LOCATOR_SHOW_EMPTY_EVENTS_TOGGLE = (By.XPATH, "//div[@class='slide-content' and text()=' Отображать незаполненные мероприятия ']//preceding-sibling::div[contains(@class, 'slide')]")
    LOCATOR_SHOW_EMPTY_EVENTS_ONLY_TOGGLE = (By.XPATH, "//div[@class='slide-content' and text()=' Только незаполненные мероприятия ']//preceding-sibling::div[contains(@class, 'slide')]")
    LOCATOR_HIDE_EVENTS_TOGGLE = (By.XPATH, "//div[@class='slide-content' and text()=' Скрывать мероприятия при фильтрации ']//preceding-sibling::div[contains(@class, 'slide')]")
    LOCATOR_CANCEL_BUTTON = (By.XPATH, "//div[@class='gantt-filter-cancel-btn']")
    LOCATOR_FILTERS_VALUE = (By.XPATH, "//div[@class='gantt-filters-block']//div[contains(@class, 'multiple-dropdown-value')]")

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

    def is_hide_events(self):
        toggle = self.find_element(self.LOCATOR_HIDE_EVENTS_TOGGLE)
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

    def switch_on_events_hiding(self):
        if self.is_hide_events():
            pass
        else:
            self.find_and_click(self.LOCATOR_HIDE_EVENTS_TOGGLE)
            # time.sleep(Vars.PKM_USER_WAIT_TIME)

    def switch_off_events_hiding(self):
        if self.is_hide_events():
            self.find_and_click(self.LOCATOR_HIDE_EVENTS_TOGGLE)
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
        try:
            self.find_element(values_locator, time=0.5)
        except TimeoutException:
            return values
        values_elements = self.driver.find_elements(*values_locator)
        for value in values_elements:
            self.driver.execute_script("arguments[0].scrollIntoView();", value)
            values.append(value.text)
        return values

    def clear_filter_values(self, filter_name, filter_set=None):
        if filter_set:
            to_delete = []
            if filter_set.get('custom_fields_filter'):
                for custom_field in filter_set.get('custom_fields_filter'):
                    if filter_set.get('custom_fields_filter').get(custom_field) != []:
                        to_delete.append(custom_field)

            if filter_set.get('custom_relations_filter'):
                for custom_relation in filter_set.get('custom_relations_filter'):
                    if filter_set.get('custom_relations_filter').get(custom_relation) != []:
                        to_delete.append(custom_relation)

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
        dropdown_item_locator = (By.XPATH, f"//div[@class='multiple-dropdown-content' and text()=' {value_name} ']//..")
        item = self.find_element(dropdown_item_locator)
        if 'selected' in item.get_attribute('class'):
            return True
        else:
            return False

    def check_value(self, value_name):
        dropdown_item_locator = (By.XPATH, f"//div[@class='multiple-dropdown-content' and text()=' {value_name} ']//..")
        if not self.is_filter_value_checked(value_name):
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(dropdown_item_locator))
            self.find_and_click(dropdown_item_locator)
        else:
            pass

    def uncheck_value(self, value_name):
        dropdown_item_locator = (By.XPATH, f"//div[@class='multiple-dropdown-content' and text()=' {value_name} ']//..")
        if self.is_filter_value_checked(value_name):
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(dropdown_item_locator))
            self.find_and_click(dropdown_item_locator)
        else:
            pass

    def set_gantt_filters(self, filter_set):
        """
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True,
                'Скрывать мероприятия при фильтрации': True
            },
            "custom_fields_filter": {
                'Тип одновременных работ': [],
                'Функциональный план': [],
                'Готовность': [],
                'Тип работ': [],

            },
            "custom_relations_filter": {
                'Персонал': [],
                'Зона': [],
                'Влияние на показатели': [],
                'Риски': [],
                'События для ИМ': []
            }

        }
        """

        if filter_set.get('unfilled_events_filter'):
            if filter_set.get('unfilled_events_filter').get('Отображать незаполненные мероприятия') is True:
                self.switch_on_empty_events()
            elif filter_set.get('unfilled_events_filter').get('Отображать незаполненные мероприятия') is False:
                self.switch_off_empty_events()

            if filter_set.get('unfilled_events_filter').get('Только незаполненные мероприятия') is True:
                self.switch_on_empty_only_events()
            elif filter_set.get('unfilled_events_filter').get('Только незаполненные мероприятия') is False:
                self.switch_off_empty_only_events()

            if filter_set.get('unfilled_events_filter').get('Скрывать мероприятия при фильтрации') is True:
                self.switch_on_events_hiding()
            elif filter_set.get('unfilled_events_filter').get('Скрывать мероприятия при фильтрации') is False:
                self.switch_off_events_hiding()

        if filter_set.get('custom_fields_filter'):
            for field in filter_set.get('custom_fields_filter'):
                if field == 'Тип работ':
                    field = 'Тип мероприятия'
                values = filter_set.get('custom_fields_filter').get(field)
                if values:
                    # self.clear_filter_values(field)
                    self.set_filter(field, values)

        if filter_set.get('custom_relations_filter'):
            for field in filter_set.get('custom_relations_filter'):
                values = filter_set.get('custom_relations_filter').get(field)
                if values:
                    # self.clear_filter_values(field)
                    self.set_filter(field, values)

    def reset_filters(self):
        self.find_and_click(self.LOCATOR_CANCEL_BUTTON)

    def is_all_filters_empty(self):
        filters = self.driver.find_elements(*self.LOCATOR_FILTERS_VALUE)
        for filter in filters:
            self.driver.execute_script("arguments[0].scrollIntoView();", filter)
            if filter.text != '':
                return False
        return True

    def get_filter_set(self):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': self.is_show_empty_events_only(),
                'Отображать незаполненные мероприятия': self.is_show_empty_events(),
                'Скрывать мероприятия при фильтрации': self.is_hide_events()
            },
            "custom_fields_filter": {
                'Тип одновременных работ': self.get_filter_values('Тип одновременных работ'),
                'Функциональный план': self.get_filter_values('Функциональный план'),
                'Готовность': self.get_filter_values('Готовность'),
                'Тип мероприятия': self.get_filter_values('Тип мероприятия')
            },
            "custom_relations_filter": {
                'Персонал': self.get_filter_values('Персонал'),
                'Зона': self.get_filter_values('Зона'),
                'Влияние на показатели': self.get_filter_values('Влияние на показатели'),
                'Риски': self.get_filter_values('Риски'),
                'События для ИМ': self.get_filter_values('События для ИМ')
            }

        }
        return filter_set






