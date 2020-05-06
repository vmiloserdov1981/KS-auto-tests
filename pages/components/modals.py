from core import BasePage
from api.api import BaseApi
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from variables import PkmVars as Vars
import time


class Modals(BasePage):
    LOCATOR_NAME_INPUT = (By.XPATH, "//input[@placeholder='Введите имя']")
    LOCATOR_CLASS_INPUT = (By.XPATH, "//input[@placeholder='Выберите класс']")
    LOCATOR_SAVE_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Сохранить ']")
    LOCATOR_CREATE_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Создать ']")
    LOCATOR_ERROR_NOTIFICATION = (By.XPATH, "//div[contains(@class,'notification-type-error') and text()='Ошибка сервера']")
    LOCATOR_MODAL_TITLE = (By.XPATH, "//div[@class='modal-window-title']//div[@class='title-text']")
    LOCATOR_ACCEPT_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Принять ']")

    def enter_and_save(self, name):
        self.find_and_enter(self.LOCATOR_NAME_INPUT, name)
        self.find_and_click(self.LOCATOR_SAVE_BUTTON)

    def object_enter_and_save(self, object_name, class_name):
        self.find_and_enter(self.LOCATOR_NAME_INPUT, object_name)
        self.find_and_enter(self.LOCATOR_CLASS_INPUT, class_name)
        self.find_and_click((By.XPATH, f"//div[@class='overlay']//div[contains(@class, 'dropdown-item') and text()=' {class_name} ']"))
        self.find_and_click(self.LOCATOR_CREATE_BUTTON)

    def check_error_displaying(self, wait_disappear=False):
        assert self.find_element(self.LOCATOR_ERROR_NOTIFICATION), 'Окно с ошибкой не отображается'
        if wait_disappear:
            assert self.is_element_disappearing(self.LOCATOR_ERROR_NOTIFICATION), "Окно с ошибкой не исчезает"


class Calendar(BasePage, BaseApi):
    LOCATOR_CALENDAR = (By.XPATH, "//mat-calendar")

    @staticmethod
    def convert_mount(abr):
        months = {
            'JAN': '01',
            'FEB': '02',
            'MAR': '03',
            'APR': '04',
            'MAY': '05',
            'JUN': '06',
            'JUL': '07',
            'AUG': '08',
            'SEP': '09',
            'OCT': '10',
            'NOV': '11',
            'DEC': '12'
        }
        res = months.get(abr)
        return res

    def check_calendar_displaying(self):
        assert self.find_element(self.LOCATOR_CALENDAR, time=5), 'Календарь не отображается'

    def get_calendar_selected_date(self):
        date = []
        self.find_and_click((By.XPATH, "//label[text()='Дата начала*']//..//input"))
        selected_date_locator = (By.XPATH, "//div[contains (@class, 'mat-calendar-body-selected')]")
        period_button_locator = (By.XPATH, "//button[contains(@class, 'mat-calendar-period-button')]//span")
        selected_date = self.get_element_text(selected_date_locator)
        date.append(selected_date)
        period = self.get_element_text(period_button_locator).split(' ')
        mon = self.convert_mount(period[0])
        period[0] = mon
        date.extend(period)
        return date

    def check_current_date_selection(self):
        current_date = self.get_calendar_selected_date()
        today_date = self.get_utc_date()
        if current_date == today_date:
            return True
        else:
            return False

    def select_day(self, day):
        day_locator = (By.XPATH, f"//div[contains (@class, 'mat-calendar-body-cell-content') and text()=' {day} ']")
        self.find_and_click(day_locator)


class NewEventModal(Calendar, BasePage):
    LOCATOR_MODAL_TITLE = (By.XPATH, "//div[@class='modal-window-title']//div[@class='title-text']")
    LOCATOR_START_DATE_FIELD = (By.XPATH, "//label[text()='Дата начала*']//..//input")
    LOCATOR_EVENT_NAME_FIELD = (By.XPATH, f"//label[@for='title' and text()='Название*']//following-sibling::input[@id='title']")
    LOCATOR_EVENT_START_DATE_FIELD = (By.XPATH, f"//label[text()='Дата начала*']//..//input[contains(@class,'datepicker-input')]")
    LOCATOR_EVENT_END_DATE_FIELD = (By.XPATH, f"//label[text()='Дата окончания']//..//input[contains(@id,'end-date')]")
    LOCATOR_EVENT_DURATION_FIELD = (By.XPATH, f"//label[text()='Длительность*']//..//input[contains(@id,'duration-period')]")
    LOCATOR_NEXT_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Дальше ']")
    LOCATOR_SAVE_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Сохранить ']")
    LOCATOR_CANCEL_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Отмена ']")

    def get_title(self):
        title = self.get_element_text(self.LOCATOR_MODAL_TITLE)
        return title

    def fill_name(self, text):
        action = ActionChains(self.driver)
        field = self.find_element(self.LOCATOR_EVENT_NAME_FIELD)
        if field.get_attribute('value') != '':
            action.double_click(field).perform()
            field.send_keys(Keys.DELETE)
        else:
            pass
        field.send_keys(text)

    def get_start_date(self):
        date = self.get_input_value(self.LOCATOR_EVENT_START_DATE_FIELD)
        date = date.split('.')
        return date

    def get_end_date(self):
        date = self.get_input_value(self.LOCATOR_EVENT_END_DATE_FIELD)
        date = date.split('-')
        return date

    def fill_field(self, field_name, text):
        action = ActionChains(self.driver)
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//following-sibling::input")
        field = self.find_element(field_locator)
        if field.get_attribute('value') != '':
            action.double_click(field).perform()
            field.send_keys(Keys.DELETE)
        else:
            pass
        field.send_keys(text)

    def get_field_value(self, field_name):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//following-sibling::input")
        field = self.find_element(field_locator)
        return field.get_attribute('value')

    def set_field(self, field_name, option):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//..//div[contains(@class, 'dropdown')]")
        value_locator = (By.XPATH, f"//div[@class='content' and text()=' {option} ']")
        self.find_and_click(field_locator)
        self.find_and_click(value_locator)

    def get_field_option(self, field_name):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//..//div[@class='display-value-text']")
        field = self.find_element(field_locator)
        return field.text

    def check_option(self, option_name):
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'checkbox-label ') and text()=' {option_name} ']//preceding-sibling::div")
        checkbox = self.find_element(checkbox_locator)
        if 'checkbox-selected' in checkbox.get_attribute('class'):
            pass
        else:
            self.find_and_click(checkbox_locator)

    def uncheck_option(self, option_name):
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'checkbox-label ') and text()=' {option_name} ']//preceding-sibling::div")
        checkbox = self.find_element(checkbox_locator)
        if 'checkbox-selected' in checkbox.get_attribute('class'):
            self.find_and_click(checkbox_locator)
        else:
            pass

    def option_is_checked(self, option_name):
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'checkbox-label ') and text()=' {option_name} ']//preceding-sibling::div")
        checkbox = self.find_element(checkbox_locator)
        if 'checkbox-selected' in checkbox.get_attribute('class'):
            return True
        else:
            return False

    @staticmethod
    def convert_mount(abr):
        months = {
            'JAN': '01',
            'FEB': '02',
            'MAR': '03',
            'APR': '04',
            'MAY': '05',
            'JUN': '06',
            'JUL': '07',
            'AUG': '08',
            'SEP': '09',
            'OCT': '10',
            'NOV': '11',
            'DEC': '12'
        }
        res = months.get(abr)
        return res

    def set_start_day(self, day):
        self.find_and_click(self.LOCATOR_START_DATE_FIELD)
        Calendar.check_calendar_displaying(self)
        Calendar.select_day(self, day)

    def save_event(self):
        button_locator = (By.XPATH, "(//div[@class='modal-window-footer']//button)[last()]")
        button = self.find_element(button_locator)
        while button.text == 'Дальше':
            button.click()
            button = self.find_element(button_locator)
        self.find_and_click(self.LOCATOR_SAVE_BUTTON)
        time.sleep(Vars.PKM_USER_WAIT_TIME)

    def get_event_data(self):
        data = {
            'event_name': self.get_input_value(self.LOCATOR_EVENT_NAME_FIELD),
            'start_date': self.get_start_date(),
            'duration': self.get_input_value(self.LOCATOR_EVENT_DURATION_FIELD),
            'end_date': self.get_end_date(),
            'event_type': self.get_field_option('Тип мероприятия'),
            'works_type': self.get_field_option('Тип одновременных работ'),
            'plan': self.get_field_option('Функциональный план'),
            'ready': self.get_field_option('Готовность'),
            'comment': self.get_field_value('Комментарий'),
            'responsible': self.get_field_value('Ответственный'),
            'is_cross_platform': self.option_is_checked('Кросс-функциональное мероприятие'),
            'is_need_attention': self.option_is_checked('Требует повышенного внимания')
        }
        return data
