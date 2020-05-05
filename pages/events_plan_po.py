from core import BasePage
from pages.components.eu_header import EuHeader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.components.modals import NewEventModal
import allure
import time
from variables import PkmVars as Vars


class EventsPlan(NewEventModal, EuHeader, BasePage):
    LOCATOR_VERSION_INPUT = (By.XPATH, "//div[@class='controls-base-block']//input[contains(@class, 'dropdown-input')]")
    LOCATOR_VERSION_INPUT_VALUE = (By.XPATH, "//div[@class='controls-base-block']//div[@class='display-value-text']")
    LOCATOR_EVENT_NAME = (By.XPATH, "//div[contains(@class, 'gantt-indicator-name-value ')]")
    LOCATOR_ADD_EVENT_BUTTON = (By.XPATH, "//div[contains(@class, 'controls-base-block')]//fa-icon[@icon='plus']")

    def set_version(self, version_name):
        current_version = self.get_element_text(self.LOCATOR_VERSION_INPUT_VALUE)
        if current_version == version_name:
            pass
        else:
            target_version = (By.XPATH, f"//div[@class='content' and text()=' {version_name} ']")
            self.find_and_click(self.LOCATOR_VERSION_INPUT)
            self.find_and_click(target_version)
            self.wait_until_text_in_element(self.LOCATOR_VERSION_INPUT_VALUE, version_name)
            grid_data_locator = (By.XPATH, "//div[@class='gantt_grid_data']")
            self.find_element(grid_data_locator)

    def get_event_names(self):
        names = []
        self.find_element(self.LOCATOR_EVENT_NAME)
        names_elements = self.driver.find_elements(*self.LOCATOR_EVENT_NAME)
        for name in names_elements:
            self.driver.execute_script("arguments[0].scrollIntoView();", name)
            event_name = name.text
            names.append(event_name)
        return names

    def create_unique_event_name(self, base_name):
        events_list = self.get_event_names()
        count = 0
        new_name = base_name
        while new_name in events_list:
            count += 1
            new_name = "{0}_{1}".format(base_name, count)
        return new_name

    def create_event(self, data, check=True):
        '''
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
        '''
        today = self.get_utc_date()
        tomorrow = self.get_feature_date(self.get_utc_date(), 1)
        self.find_and_click(self.LOCATOR_ADD_EVENT_BUTTON)
        title = NewEventModal.get_title(self)
        assert title == 'Параметры мероприятия', 'Неверный тайтл'
        if check:
            with allure.step(f'Проверить, дата начала и длительность рассчитаны правильно, а все остальные поля - пустые'):
                self.find_and_click(self.LOCATOR_NEXT_BUTTON)
                assert self.find_element(self.LOCATOR_EVENT_NAME_FIELD)
                assert self.get_input_value(self.LOCATOR_EVENT_NAME_FIELD) == ''
                assert self.get_start_date() == today
                assert self.get_input_value(self.LOCATOR_EVENT_DURATION_FIELD) == '1'
                assert self.get_end_date() == tomorrow
                assert self.get_field_option('Тип мероприятия') == ''
                assert self.get_field_option('Тип одновременных работ') == ''
                assert self.get_field_option('Функциональный план') == ''
                assert self.get_field_option('Готовность') == ''
                assert self.get_field_value('Комментарий') == ''
                assert self.get_field_value('Ответственный') == ''
                assert not self.option_is_checked('Кросс-функциональное мероприятие')
                assert not self.option_is_checked('Требует повышенного внимания')
        with allure.step(f'Заполнить данные мероприятия'):
            NewEventModal.fill_name(self, data.get('event_name'))
            NewEventModal.set_start_day(self, data.get('start_day'))
            NewEventModal.set_field(self, 'Тип мероприятия', data.get('event_type'))
            NewEventModal.set_field(self, 'Тип одновременных работ', data.get('works_type'))
            NewEventModal.set_field(self, 'Функциональный план', data.get('plan'))
            NewEventModal.set_field(self, 'Готовность', data.get('ready'))
            NewEventModal.fill_field(self, 'Комментарий', data.get('comment'))
            NewEventModal.fill_field(self, 'Ответственный', data.get('responsible'))
            if data.get('is_cross_platform'):
                NewEventModal.check_option(self, 'Кросс-функциональное мероприятие')
            if data.get('is_need_attention'):
                NewEventModal.check_option(self, 'Требует повышенного внимания')
            completed_data = NewEventModal.get_event_data(self)
            NewEventModal.save_event(self)
            return completed_data

    def check_event(self, name, start_date, end_date):
        grid_data_locator = (By.XPATH, "//div[@class='gantt_grid_data']")
        self.find_element(grid_data_locator)
        time.sleep(Vars.PKM_USER_WAIT_TIME)
        event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, '{name}')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(event_locator))
        aria_label = self.find_element(event_locator).get_attribute('aria-label')
        aria_name = aria_label.split(' Start date: ')[0].split(' Task: ')[1]
        aria_start = aria_label.split(' Start date: ')[1].split(' End date: ')[0].split('-')[::-1]
        aria_end = aria_label.split(' End date: ')[1].split('-')[::-1]
        assert aria_name == name
        assert aria_start == start_date
        assert aria_end == end_date

    def open_event(self, event_name):
        grid_data_locator = (By.XPATH, "//div[@class='gantt_grid_data']")
        self.find_element(grid_data_locator)
        event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, '{event_name}')]")
        action = ActionChains(self.driver)
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(event_locator))
        time.sleep(Vars.PKM_USER_WAIT_TIME)
        action.double_click(self.find_element(event_locator)).perform()
        assert self.get_title() == event_name
