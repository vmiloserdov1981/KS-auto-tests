from core import BasePage
from pages.components.eu_header import EuHeader
from api.api import ApiEu
from pages.components.eu_filter import EuFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.components.modals import NewEventModal
from pages.components.modals import Modals
import allure
from selenium.common.exceptions import TimeoutException
import time
from variables import PkmVars as Vars


class EventsPlan(NewEventModal, Modals, ApiEu, EuFilter):
    LOCATOR_VERSION_INPUT = (By.XPATH, "//div[@class='controls-base-block']//input[contains(@class, 'dropdown-input')]")
    LOCATOR_VERSION_INPUT_VALUE = (By.XPATH, "//div[@class='controls-base-block']//div[@class='display-value-text']")
    LOCATOR_EVENT_NAME = (By.XPATH, "//div[contains(@class, 'gantt-indicator-name-value ')]")
    LOCATOR_LAST_EVENT_NAME = (By.XPATH, "(//div[contains(@class, 'gantt-indicator-name-value ')])[last()]")
    LOCATOR_ADD_EVENT_BUTTON = (By.XPATH, "//div[contains(@class, 'controls-base-block')]//fa-icon[@icon='plus']")
    LOCATOR_TRASH_ICON = (By.XPATH, "//div[@class='controls-base-block']//fa-icon[@icon='trash']")
    LOCATOR_GANTT_DATA = (By.XPATH, "//div[@class='gantt_grid_data']")
    LOCATOR_GANTT_LAST_ROW = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
    LOCATOR_GANTT_SCROLL = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")

    def __init__(self, driver, login=None, password=None, token=None):
        BasePage.__init__(self, driver)
        ApiEu.__init__(self, login, password, token=token)

    def get_active_version_name(self):
        current_version = self.get_element_text(self.LOCATOR_VERSION_INPUT_VALUE)
        return current_version

    def set_version(self, version_name):
        if self.get_active_version_name() == version_name:
            pass
        else:
            target_version = (By.XPATH, f"//div[@class='content' and text()=' {version_name} ']")
            self.find_and_click(self.LOCATOR_VERSION_INPUT)
            self.find_and_click(target_version)
            self.wait_until_text_in_element(self.LOCATOR_VERSION_INPUT_VALUE, version_name)
            grid_data_locator = (By.XPATH, "//div[@class='gantt_grid_data']")
            self.find_element(grid_data_locator)
            time.sleep(Vars.PKM_USER_WAIT_TIME)

    def get_event_names(self):
        names = [event for event in self.events_generator(names_only=True)]
        return names

    def is_event_exists(self, event_name):
        try:
            self.find_element(self.LOCATOR_EVENT_NAME)
        except TimeoutException:
            return False
        for event in self.events_generator(names_only=True):
            if event_name == event:
                return True
        return False

    def create_unique_event_name(self, base_name):
        events_list = self.get_event_names()
        count = 0
        new_name = base_name
        while new_name in events_list:
            count += 1
            new_name = "{0}_{1}".format(base_name, count)
        return new_name

    def create_event(self, data, check=True):
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
            NewEventModal.set_duration(self, data.get('duration'))
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
            time.sleep(Vars.PKM_API_WAIT_TIME)
            return completed_data

    def events_generator(self, names_only=False):
        # перебирает мероприятия поэкранно, стабильный
        last_row_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
        rows_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')]")
        stop_gen = False
        try:
            scrollbar = self.find_element((By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]"), time=5)
            self.driver.execute_script("arguments[0].scrollTop = 0;", scrollbar)
            time.sleep(5)
        except TimeoutException:
            pass

        while not stop_gen:
            try:
                self.find_element(rows_locator, time=5)
            except TimeoutException:
                stop_gen = True
                yield None

            if not stop_gen:
                time.sleep(3)
                rows = self.driver.find_elements(*rows_locator)
                for row in rows:
                    # self.driver.execute_script("arguments[0].scrollIntoView();", row)
                    if '\n' in row.text:
                        if names_only:
                            row_text = row.text
                            row_name = row_text.split('\n')[1]
                            yield row_name
                        else:
                            yield row

                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                try:
                    self.find_element(scroll_area, time=2)
                except TimeoutException:
                    stop_gen = True

            if not stop_gen:
                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                scrollbar = self.find_element(scroll_area, time=2)
                start_height = self.driver.execute_script("return arguments[0].clientHeight", scrollbar)
                cell_height = self.driver.execute_script("return arguments[0].clientHeight",
                                                         self.find_element(last_row_locator))
                step = ((start_height // cell_height) + 0) * cell_height
                total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                new_height = 0
                while True:
                    # last screen actions
                    if new_height + step + start_height >= total_height:
                        self.driver.execute_script("arguments[0].scrollIntoView();",
                                                   self.find_element(last_row_locator))
                        row = self.find_element(last_row_locator)
                        if names_only:
                            row_text = row.text
                            row_name = row_text.split('\n')[1]
                            yield row_name
                        else:
                            yield row

                        while new_height + cell_height + start_height <= total_height:
                            last_row = self.find_element(last_row_locator)
                            self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar,
                                                       cell_height)
                            try:
                                self.wait_element_replacing(last_row, last_row_locator, time=3)
                            except TimeoutException:
                                pass
                            new_height = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                            self.driver.execute_script("arguments[0].scrollIntoView();",
                                                       self.find_element(last_row_locator))
                            if names_only:
                                last_row_text = self.get_element_text(last_row_locator)
                                last_row_name = last_row_text.split('\n')[1]
                                yield last_row_name
                            else:
                                yield self.find_element(last_row_locator)
                        stop_gen = True
                        break

                    # Scroll down
                    last_row = self.find_element(last_row_locator)
                    self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, step)
                    new_height = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                    try:
                        self.wait_element_replacing(last_row, last_row_locator, time=3)
                    except TimeoutException:
                        pass
                    rows = self.driver.find_elements(*rows_locator)
                    for row in rows:
                        if '\n' in row.text:
                            # self.driver.execute_script("arguments[0].scrollIntoView();", row)
                            if names_only:
                                row_text = row.text
                                row_name = row_text.split('\n')[1]
                                yield row_name
                            else:
                                yield row

    def events_generator_rows(self, names_only=False):
        # перебирает мероприятия построчно, первый вариант
        last_row_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
        rows_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')]")
        # prelast_row_locator = (By.XPATH, "(//div[contains(@class, 'gantt_row')])[last()-1]")
        new_height = 0
        stop_gen = False
        try:
            scrollbar = self.find_element((By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]"), time=5)
            self.driver.execute_script("arguments[0].scrollTop = 0;", scrollbar)
            time.sleep(5)
        except TimeoutException:
            pass

        while not stop_gen:
            try:
                self.find_element(rows_locator, time=5)
            except TimeoutException:
                stop_gen = True
                yield None

            if not stop_gen:
                time.sleep(3)
                rows = self.driver.find_elements(*rows_locator)
                for row in rows:
                    self.driver.execute_script("arguments[0].scrollIntoView();", row)
                    if names_only:
                        row_text = row.text
                        row_name = row_text.split('\n')[1]
                        yield row_name
                    else:
                        yield row

                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                try:
                    self.find_element(scroll_area, time=2)
                except TimeoutException:
                    stop_gen = True

            if not stop_gen:
                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                scrollbar = self.find_element(scroll_area, time=2)
                start_height = self.driver.execute_script("return arguments[0].clientHeight", scrollbar)
                step = self.driver.execute_script("return arguments[0].clientHeight",
                                                  self.find_element(last_row_locator))
                total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                while True:
                    if new_height + step + start_height >= total_height:
                        self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, step)
                        self.driver.execute_script("arguments[0].scrollIntoView();",
                                                   self.find_element(last_row_locator))
                        if names_only:
                            last_row_text = self.get_element_text(last_row_locator)
                            last_row_name = last_row_text.split('\n')[1]
                            yield last_row_name
                        else:
                            yield self.find_element(last_row_locator)
                        stop_gen = True
                        break

                    # Scroll down
                    last_row = self.find_element(last_row_locator)
                    self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, step)
                    new_height = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                    if new_height + step + start_height < total_height:
                        try:
                            self.wait_element_replacing(last_row, last_row_locator, time=3)
                        except TimeoutException:
                            pass
                        last_row = self.find_element(last_row_locator)
                        self.driver.execute_script("arguments[0].scrollIntoView();", last_row)
                        if names_only:
                            last_row_text = last_row.text
                            name = last_row_text.split('\n')[1]
                            yield name
                        else:
                            yield last_row

    def check_event(self, name, start_date, end_date):
        for event in self.events_generator():
            if event.text.split('\n')[1] == name:
                aria_label = event.get_attribute('aria-label')
                aria_name = aria_label.split(' Start date: ')[0].split(' Task: ')[1]
                aria_start = aria_label.split(' Start date: ')[1].split(' End date: ')[0].split('-')[::-1]
                aria_end = aria_label.split(' End date: ')[1].split('-')[::-1]
                assert aria_name == name
                assert aria_start == start_date
                assert aria_end == end_date
                return True
        raise AssertionError(f'Мероприятие "{name}" не найдено')

    def select_event(self, name):
        for event in self.events_generator():
            try:
                if event.text.split('\n')[1] == name:
                    # self.driver.execute_script("arguments[0].scrollIntoView();", event)
                    event.click()
                    # assert 'gantt_selected' in event.get_attribute('class')
                    return True
            except IndexError:
                pass
        raise AssertionError(f'Мероприятие "{name}" не найдено')

    def delete_event(self, name):
        with allure.step(f'Удалить мероприятие'):
            self.select_event(name)
            self.find_and_click(self.LOCATOR_TRASH_ICON)
            self.find_and_click(Modals.LOCATOR_ACCEPT_BUTTON)
        with allure.step(f'Проверить исчезание мероприятия после удаления'):
            event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, '{name}')]")
            assert self.is_element_disappearing(event_locator, wait_display=False, time=15), 'Мероприятие не исчезает после удаления'

    def open_event(self, event_name, start_date=None, end_date=None):
        # names = []
        for event in self.events_generator():
            # names.append(event.text)
            if event.text.split('\n')[1] == event_name:
                action = ActionChains(self.driver)
                aria_label = event.get_attribute('aria-label')
                aria_name = aria_label.split(' Start date: ')[0].split(' Task: ')[1]
                assert aria_name == event_name
                if start_date:
                    aria_start = aria_label.split(' Start date: ')[1].split(' End date: ')[0].split('-')[::-1]
                    assert aria_start == start_date
                if end_date:
                    aria_end = aria_label.split(' End date: ')[1].split('-')[::-1]
                    assert aria_end == end_date
                action.double_click(event).perform()
                assert self.get_title() == event_name
                return True
        raise AssertionError(f'Мероприятие "{event_name}" не найдено на диаграмме')

    def set_gantt_filter(self, filter_set):
        """
                        filter_set = {
                            "unfilled_events_filter": {
                                'deleted_only': False,
                                'get_deleted': True
                            },
                            "custom_relations_filter": {}
                        }
        """

        if filter_set.get('unfilled_events_filter'):
            pass

    def check_plan_events(self, plan_uuid, version, login, filter_set=None):
        """
                filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
                """

        if filter_set is None:
            filter_set = {}

        deleted_only = filter_set.get('unfilled_events_filter').get('deleted_only')
        get_deleted = filter_set.get('unfilled_events_filter').get('get_deleted')

        if deleted_only:
            api_events = self.api_get_event_names(version, plan_uuid, login, deleleted_only=True)
        else:
            if get_deleted:
                api_events = self.api_get_event_names(version, plan_uuid, login, get_deleted=True)
            else:
                api_events = self.api_get_event_names(version, plan_uuid, login, get_deleted=False)
        ui_events = [event for event in self.events_generator(names_only=True) if event is not None]
        not_in_ui = [api_event for api_event in api_events if api_event not in ui_events]
        assert self.compare_lists(api_events, ui_events), f'Мероприятия на диаграмме и в API не совпадают, в ui не отображаются мероприятия "{not_in_ui}"'
