from core import BasePage
from api.api import BaseApi
from selenium.webdriver.common.by import By
from variables import PkmVars as Vars
import time
from selenium.common.exceptions import TimeoutException


class Modals(BasePage):
    LOCATOR_NAME_INPUT = (By.XPATH, "//input[@placeholder='Введите имя']")
    LOCATOR_CLASS_INPUT = (By.XPATH, "//input[@placeholder='Выберите класс']")
    LOCATOR_SAVE_BUTTON = (By.XPATH, "//div[contains(@class, 'modal-window-footer')]//button[text()=' Сохранить ']")
    LOCATOR_CREATE_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Создать ']")
    LOCATOR_ERROR_NOTIFICATION = (By.XPATH, "//div[contains(@class,'notification-type-error') and text()='Ошибка сервера']")
    LOCATOR_MODAL_TITLE = (By.XPATH, "//div[@class='modal-window-title']//div[@class='title-text']")
    LOCATOR_ACCEPT_BUTTON = (By.XPATH, "//div[contains(@class, 'modal-window-footer')]//button[text()=' Принять ']")

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
    LOCATOR_MODAL_TITLE = (By.XPATH, "//div[contains(@class, 'modal-window-title')]//div[contains(@class, 'title-text')]")
    LOCATOR_START_DATE_FIELD = (By.XPATH, "//*[contains (text(), 'Дата начала*')]//..//input")
    LOCATOR_EVENT_NAME_FIELD = (By.XPATH, "//input[@id='title']")
    LOCATOR_EVENT_START_DATE_FIELD = (By.XPATH, f"//*[contains(text(), 'Дата начала*')]//..//input[contains(@class,'datepicker-input')]")
    LOCATOR_EVENT_END_DATE_FIELD = (By.XPATH, f"//*[contains(text(), 'Дата окончания')]//..//input[contains(@id,'end-date')]")
    LOCATOR_EVENT_DURATION_FIELD = (By.XPATH, f"//*[contains(text(), 'Длительность*')]//..//input[contains(@id,'duration-period')]")
    LOCATOR_NEXT_BUTTON = (By.XPATH, "//div[contains(@class, 'modal-window-footer')]//button[text()=' Дальше ']")
    LOCATOR_SAVE_BUTTON = (By.XPATH, "//div[contains(@class, 'modal-window-footer')]//button[text()=' Сохранить ']")
    LOCATOR_CANCEL_BUTTON = (By.XPATH, "//div[contains(@class, 'modal-window-footer')]//button[text()=' Отмена ']")

    def get_title(self):
        title = self.get_element_text(self.LOCATOR_MODAL_TITLE, time=15)
        return title

    def fill_name(self, text):
        field = self.find_element(self.LOCATOR_EVENT_NAME_FIELD)
        if field.get_attribute('value') != '':
            field.clear()
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
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//following-sibling::input")
        field = self.find_element(field_locator)
        if field.get_attribute('value') != '':
            field.clear()
        else:
            pass
        field.send_keys(text)

    def get_field_value(self, field_name):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//following-sibling::input")
        field = self.find_element(field_locator)
        return field.get_attribute('value')

    def set_field(self, field_name, option):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicators-list-item') and ./div[text()=' {field_name} ']]//div[contains(@class, 'dropdown')]")
        value_locator = (By.XPATH, f"//div[@class='content' and text()=' {option} ']")
        self.find_and_click(field_locator)
        self.find_and_click(value_locator)

    def get_field_option(self, field_name):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicators-list-item') and ./div[text()=' {field_name} ']]//div[contains(@class, 'dropdown')]")
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
        start_date = self.get_start_date()
        duration = int(self.get_input_value(self.LOCATOR_EVENT_DURATION_FIELD))
        expected_end = self.get_feature_date(start_date, duration)
        assert self.get_end_date() == expected_end, 'дата окончания рассчитана неправильно'

    def set_duration(self, duration):
        start_date = self.get_start_date()
        field = self.find_element(self.LOCATOR_EVENT_DURATION_FIELD)
        if field.get_attribute('value') != '':
            field.clear()
        else:
            pass
        field.send_keys(duration)
        expected_end = self.get_feature_date(start_date, int(duration))
        time.sleep(1)
        assert self.get_end_date() == expected_end, 'дата окончания рассчитана неправильно'

    def save_event(self):
        button_locator = (By.XPATH, "//div[contains(@class, 'modal-window-footer')]//button[.=' Сохранить ']")
        button = self.find_element(button_locator)
        while button.text == 'Дальше':
            button.click()
            button = self.find_element(button_locator)
        self.find_and_click(self.LOCATOR_SAVE_BUTTON)
        time.sleep(Vars.PKM_USER_WAIT_TIME)

    def get_event_data(self):
        # time.sleep(3)
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

    def modify_event(self, data):
        """
        Пример:
        data = {
            'event_name': event_name,
            'start_day': '10',
            'duration': '5',
            'event_type': 'Текущая',
            'works_type': 'Бурение',
            'plan': 'План отгрузок',
            'ready': 'Готово к реализации',
            'comment': 'Авто тест',
            'responsible': 'Олег Петров',
            'is_cross_platform': True,
            'is_need_attention': True
        }
        """
        exists_event_data = self.get_event_data()
        new_event_data = {
            'event_name': None,
            'start_date': None,
            'duration': None,
            'end_date': None,
            'event_type': None,
            'works_type': None,
            'plan': None,
            'ready': None,
            'comment': None,
            'responsible': None,
            'is_cross_platform': None,
            'is_need_attention': None
        }
        if data.get('event_name'):
            NewEventModal.fill_name(self, data.get('event_name'))
            new_event_data['event_name'] = data.get('event_name')
        else:
            new_event_data['event_name'] = exists_event_data.get('event_name')

        if data.get('start_day'):
            NewEventModal.set_start_day(self, data.get('start_day'))
            new_event_data['start_date'] = self.get_start_date()
        else:
            new_event_data['start_date'] = exists_event_data.get('start_date')

        if data.get('duration'):
            NewEventModal.set_duration(self, data.get('duration'))
            new_event_data['duration'] = data.get('duration')
        else:
            new_event_data['duration'] = exists_event_data.get('duration')

        if data.get('start_date') or data.get('duration'):
            new_event_data['end_date'] = self.get_end_date()
        else:
            new_event_data['end_date'] = exists_event_data.get('end_date')

        if data.get('event_type'):
            NewEventModal.set_field(self, 'Тип мероприятия', data.get('event_type'))
            new_event_data['event_type'] = data.get('event_type')
        else:
            new_event_data['event_type'] = exists_event_data.get('event_type')

        if data.get('works_type'):
            NewEventModal.set_field(self, 'Тип одновременных работ', data.get('works_type'))
            new_event_data['works_type'] = data.get('works_type')
        else:
            new_event_data['works_type'] = exists_event_data.get('works_type')

        if data.get('plan'):
            NewEventModal.set_field(self, 'Функциональный план', data.get('plan'))
            new_event_data['plan'] = data.get('plan')
        else:
            new_event_data['plan'] = exists_event_data.get('plan')

        if data.get('ready'):
            NewEventModal.set_field(self, 'Готовность', data.get('ready'))
            new_event_data['ready'] = data.get('ready')
        else:
            new_event_data['ready'] = exists_event_data.get('ready')

        if data.get('comment'):
            NewEventModal.fill_field(self, 'Комментарий', data.get('comment'))
            new_event_data['comment'] = data.get('comment')
        else:
            new_event_data['comment'] = exists_event_data.get('comment')

        if data.get('responsible'):
            NewEventModal.fill_field(self, 'Ответственный', data.get('responsible'))
            new_event_data['responsible'] = data.get('responsible')
        else:
            new_event_data['responsible'] = exists_event_data.get('responsible')

        if data.get('is_cross_platform') is not None:
            if data.get('is_cross_platform') is True:
                NewEventModal.check_option(self, 'Кросс-функциональное мероприятие')
                new_event_data['is_cross_platform'] = True
            if data.get('is_cross_platform') is False:
                NewEventModal.uncheck_option(self, 'Кросс-функциональное мероприятие')
                new_event_data['is_cross_platform'] = False
        else:
            new_event_data['is_cross_platform'] = exists_event_data.get('is_cross_platform')

        if data.get('is_need_attention') is not None:
            if data.get('is_need_attention') is True:
                NewEventModal.check_option(self, 'Требует повышенного внимания')
                new_event_data['is_need_attention'] = True
            if data.get('is_need_attention') is False:
                NewEventModal.uncheck_option(self, 'Требует повышенного внимания')
                new_event_data['is_need_attention'] = False
        else:
            new_event_data['is_need_attention'] = exists_event_data.get('is_need_attention')

        completed_data = NewEventModal.get_event_data(self)
        assert completed_data == new_event_data, 'Поля отображают неправильные значения'
        NewEventModal.save_event(self)
        return completed_data

    def check_event(self, expected_data):
        """
                Пример:
                expected_data = {
                    'event_name': event_name,
                    'start_date': ['11', '05', '2020'],
                    'end_date': ['12', '05', '2020'],
                    'duration': '1',
                    'event_type': 'Текущая',
                    'works_type': 'Бурение',
                    'plan': None,
                    'ready': 'Готово к реализации',
                    'comment': 'Авто тест',
                    'responsible': 'Олег Петров',
                    'is_cross_platform': True,
                    'is_need_attention': True
                }
                """
        actual_data = self.get_event_data()
        for indicator in actual_data:
            if actual_data.get(indicator) == '' or actual_data.get(indicator) == [''] or actual_data.get(indicator) == 'Не заполнено':
                actual_data[indicator] = None

        for indicator in expected_data:
            if expected_data.get(indicator) == '' or expected_data.get(indicator) == [''] or expected_data.get(indicator) == 'Не заполнено':
                expected_data[indicator] = None

        if expected_data.get('is_cross_platform') is None:
            expected_data['is_cross_platform'] = False

        if expected_data.get('is_need_attention') is None:
            expected_data['is_need_attention'] = False

        if actual_data == expected_data:
            return True
        else:
            return False


class ProjectModal(BasePage):
    LOCATOR_SELECT_PROJECT_MODAL = (By.XPATH, "//div[@class='title-text' and text()='Выбор проекта']/ancestor:: div[@class='modal-window']")
    LOCATOR_ENTER_PROJECT_BUTTON = (By.XPATH, "//button[.=' Войти в проект ']")
    LOCATOR_REMEMBER_PROJECT = (By.XPATH, "//div[contains(@class, 'checkbox-wrapper') and .=' Запомнить мой выбор ']//div[@class='checkbox-container']")

    def is_project_modal_displaying(self):
        try:
            self.find_element(self.LOCATOR_SELECT_PROJECT_MODAL)
            return True
        except TimeoutException:
            return False

    def select_project(self, project_name, remember_choice=False):
        choice_locator = (By.XPATH, f"//div[contains(@class, 'choice-project') and .='{project_name}']")
        self.find_and_click(choice_locator)
        if remember_choice:
            self.find_and_click(self.LOCATOR_REMEMBER_PROJECT)
        self.find_and_click(self.LOCATOR_ENTER_PROJECT_BUTTON)
