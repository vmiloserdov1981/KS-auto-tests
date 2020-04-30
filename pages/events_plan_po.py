from core import BasePage
from pages.components.eu_header import EuHeader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.components.modals import Modals


class EventsPlan(EuHeader, Modals, BasePage):
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

    def create_event(self, data):
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
        self.find_and_click(self.LOCATOR_ADD_EVENT_BUTTON)
        title = Modals.get_title(self)
        assert title == 'Параметры мероприятия', 'Неверный тайтл'
        self.fill_name('Название*', data.get('event_name'))
        self.set_field('Готовность', 'Выполнено')
        self.fill_field('Комментарий', 'Ололо')
        self.check_option('Требует повышенного внимания')
        self.uncheck_option('Требует повышенного внимания')
        pass



