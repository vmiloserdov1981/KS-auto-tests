from core import BasePage
from core import antistale
from pages.components.eu_filter import EuFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from pages.components.modals import NewEventModal
from pages.components.modals import Modals
import allure
from selenium.common.exceptions import TimeoutException
import time
from variables import PkmVars as Vars


class EventsPlan(NewEventModal, Modals, EuFilter):
    LOCATOR_VERSION_BUTTON = (By.XPATH, "//pkm-button[.//button[contains(text(), 'Наборы данных')]]")
    #LOCATOR_VERSION_DROPDOWN = (By.XPATH, "//div[@stylesmodule='pr']")
    LOCATOR_VERSION_DROPDOWN = (By.XPATH, "//div[contains(@class, 'gantt-overlay-menu')]")
    LOCATOR_BASE_VERSION_VALUE = (By.XPATH, "//div[contains(@class, 'filter-dropdown-item') and contains(@class, 'selected') and ./div[.=' 1 ']]")
    LOCATOR_EVENT_NAME = (By.XPATH, "//div[contains(@class, 'gantt-indicator-name-value ')]")
    LOCATOR_LAST_EVENT_NAME = (By.XPATH, "(//div[contains(@class, 'gantt-indicator-name-value ')])[last()]")
    LOCATOR_ADD_EVENT_BUTTON = (By.XPATH, "//div[contains(@class, 'controls-base-block')]//fa-icon[@icon='plus']")
    LOCATOR_TRASH_ICON = (By.XPATH, "//div[@class='controls-base-block']//fa-icon[@icon='trash']")
    LOCATOR_COPY_ICON = (By.XPATH, "//div[@class='controls-base-block']//fa-icon[@icon='clone']")
    LOCATOR_GROUPING_ICON = (By.XPATH, "//div[@class='controls-base-block']//fa-icon[@icon='indent']")
    LOCATOR_GANTT_DATA = (By.XPATH, "//div[@class='gantt_grid_data']")
    LOCATOR_GANTT_LAST_ROW = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
    LOCATOR_GANTT_SCROLL = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def open_versions_list(self):
        try:
            dropdown = self.find_element(self.LOCATOR_VERSION_DROPDOWN, time=2)
        except TimeoutException:
            dropdown = None
        if not dropdown:
            self.find_and_click(self.LOCATOR_VERSION_BUTTON)
            self.find_element(self.LOCATOR_VERSION_DROPDOWN)

    def close_versions_list(self):
        try:
            dropdown = self.find_element(self.LOCATOR_VERSION_DROPDOWN, time=2)
        except TimeoutException:
            dropdown = None
        if dropdown:
            self.find_and_click(self.LOCATOR_VERSION_BUTTON)
            assert self.is_element_disappearing(self.LOCATOR_VERSION_DROPDOWN, wait_display=False), 'Дропдаун версий плана не скрывается'

    def get_active_version_name(self):
        self.open_versions_list()
        active_base_version = self.get_element_text(self.LOCATOR_BASE_VERSION_VALUE)
        active_base_version = active_base_version.split('\n')[0]
        self.close_versions_list()
        return active_base_version

    def set_version(self, version_name, force=False):
        self.open_versions_list()
        base_active_version = self.get_element_text(self.LOCATOR_BASE_VERSION_VALUE).split('\n')[0]
        target_version_locator = (By.XPATH, f"//div[contains(@class, 'filter-dropdown-item') and .//div[.='{version_name}']]")
        selected_version_locator = (By.XPATH, "(//div[contains(@class, 'filter-dropdown-item') and contains(@class, 'selected')])")
        if base_active_version != version_name:
            self.find_and_click(target_version_locator)
        for selected_version in self.elements_generator(selected_version_locator):
            if selected_version.text.split('\n')[0] != version_name:
                selected_version.click()
                time.sleep(2)
        self.close_versions_list()

    @antistale
    def is_event_exists(self, event_name):
        try:
            event = self.get_event(event_name)
            if event:
                return True
        except AssertionError:
            return False

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
            NewEventModal.set_field(self, 'Тип одновременных работ', data.get('works_type'), alter_field_name='Тип работ')
            NewEventModal.set_field(self, 'Функциональный план', data.get('plan'))
            NewEventModal.set_field(self, 'Готовность', data.get('ready'))
            NewEventModal.fill_field(self, 'Комментарий', data.get('comment'))
            NewEventModal.fill_field(self, 'Ответственный', data.get('responsible'))
            if data.get('is_cross_platform'):
                NewEventModal.check_option(self, 'Кросс-функциональное мероприятие')
            if data.get('is_need_attention'):
                NewEventModal.check_option(self, 'Требует повышенного внимания')
            completed_data = NewEventModal.get_event_data(self) if check else None
            NewEventModal.save_event(self)
            time.sleep(Vars.PKM_API_WAIT_TIME)
            return completed_data

    def events_generator(self, names_only=False):
        # Самый актуальный
        # перебирает мероприятия построчно в соответствии с подгрузкой ганта
        last_row_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
        rows_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')]")
        stop_gen = False

        # скролл в начало диаграммы
        self.scroll_to_gantt_top()
        time.sleep(5)

        # Перебор мероприятий которые уже отрисованы
        while not stop_gen:
            try:
                self.find_element(rows_locator, time=10)
            except TimeoutException:
                stop_gen = True
                yield None

            if not stop_gen:
                time.sleep(3)
                rows = self.driver.find_elements(*rows_locator)
                for row in rows:
                    if row.text == '':
                        self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=false);",
                                                   row)
                    if names_only:
                        yield row.text
                    else:
                        yield row
                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                try:
                    self.find_element(scroll_area, time=2)
                except TimeoutException:
                    stop_gen = True

            # настройка построчного перебора
            if not stop_gen:
                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                scrollbar = self.find_element(scroll_area, time=2)
                total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                gantt = self.find_element((By.XPATH, "//pkm-gantt-diagram"))
                last_row = self.find_element(last_row_locator)
                cell_height = self.driver.execute_script("return arguments[0].clientHeight", last_row) + 1
                last_target_row_html = last_row.get_attribute('innerHTML')
                target_row_top = self.driver.execute_script("return arguments[0].offsetTop", last_row)
                screen_height = self.driver.execute_script("return arguments[0].offsetHeight", scrollbar)
                scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                screen_height_range = range(scroll_top, scroll_top + screen_height + cell_height)


                # построчный перебор
                while not stop_gen:
                    if target_row_top in screen_height_range:
                        target_row_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@style, 'top: {target_row_top}px')]")
                        try:
                            target_row = self.find_element(target_row_locator, time=5)
                        except TimeoutException:
                            break
                        if target_row.get_attribute('innerHTML') != last_target_row_html:
                            self.scroll_to_element(target_row)
                            if names_only:
                                yield target_row.text
                            else:
                                yield target_row
                        target_row_top += cell_height
                        if target_row_top >= total_height - 2:
                            break
                        last_target_row_html = target_row.get_attribute('innerHTML')
                        self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, cell_height)
                    else:
                        self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, cell_height)
                        time.sleep(3)

                    if target_row_top + cell_height + cell_height >= total_height - 2:
                        time.sleep(5)
                    scrollbar = self.find_element(scroll_area, time=2)
                    scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                    screen_height_range = range(scroll_top, scroll_top + screen_height + cell_height)
                    total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                break

    def events_generator_old(self, names_only=False):
        # Первый вариант
        # перебирает мероприятия построчно в соответствии с подгрузкой ганта
        last_row_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
        rows_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')]")
        stop_gen = False

        # скролл в начало диаграммы
        self.scroll_to_gantt_top()
        time.sleep(5)

        # Перебор мероприятий которые уже отрисованы
        while not stop_gen:
            try:
                self.find_element(rows_locator, time=10)
            except TimeoutException:
                stop_gen = True
                yield None

            if not stop_gen:
                time.sleep(3)
                rows = self.driver.find_elements(*rows_locator)
                for row in rows:
                    if row.text == '':
                        self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=false);",
                                                   row)
                    if names_only:
                        yield row.text
                    else:
                        yield row
                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                try:
                    self.find_element(scroll_area, time=2)
                except TimeoutException:
                    stop_gen = True

            # настройка построчного перебора
            if not stop_gen:
                scroll_area = (By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]")
                scrollbar = self.find_element(scroll_area, time=2)
                total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                last_row = self.find_element(last_row_locator)
                cell_height = self.driver.execute_script("return arguments[0].clientHeight", last_row) + 1
                last_target_row_html = last_row.get_attribute('innerHTML')
                last_row_top = self.driver.execute_script("return arguments[0].offsetTop", last_row)
                screen_height = self.driver.execute_script("return arguments[0].offsetHeight", scrollbar)
                target_row_top = last_row_top
                scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                screen_height_range = range(scroll_top, scroll_top + screen_height + cell_height)

                # построчный перебор
                while not stop_gen:
                    if target_row_top in screen_height_range:
                        target_row_locator = (By.XPATH,
                                              f"//div[contains(@class, 'gantt_row') and contains(@style, 'top: {target_row_top}px')]")
                        try:
                            target_row = self.find_element(target_row_locator, time=2)
                        except TimeoutException:
                            break
                        if target_row.get_attribute('innerHTML') != last_target_row_html:
                            self.scroll_to_element(target_row)
                            if names_only:
                                yield target_row.text
                            else:
                                yield target_row
                        target_row_top += cell_height
                        last_target_row_html = target_row.get_attribute('innerHTML')
                    else:
                        self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, cell_height)
                        if scroll_top + screen_height + cell_height > total_height:
                            time.sleep(5)
                        scrollbar = self.find_element(scroll_area, time=2)
                        scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                        screen_height_range = range(scroll_top, scroll_top + screen_height + cell_height)
                        total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                        if target_row_top not in screen_height_range:
                            stop_gen = True
                break

    def get_event(self, event_name, wait_timeout=1) -> WebElement:
        # Нужен рефакторинг в связи с динамической подгрузкой ганта
        event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, ' {event_name} ')]")
        try:
            target = self.find_element(event_locator, time=5)
            self.scroll_to_element(target)
            time.sleep(1)
            return self.find_element(event_locator, time=wait_timeout)
        except TimeoutException:
            # Проверка наличия скролла
            try:
                scrollbar = self.find_element((By.XPATH, "//div[contains(@class, 'gantt_ver_scroll')]"), time=2)
            except TimeoutException:
                scrollbar = None

        if scrollbar:
            # скролл в начало диаграммы
            self.scroll_to_gantt_top()
            time.sleep(5)

            # Поэкранный перебор
            total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
            screen_height = self.driver.execute_script("return arguments[0].clientHeight", scrollbar)
            actual_height = screen_height

            while actual_height - screen_height <= total_height:
                try:
                    target = self.find_element(event_locator, time=wait_timeout)
                    self.scroll_to_element(target)
                    time.sleep(1)
                    return self.find_element(event_locator, time=wait_timeout)
                except TimeoutException:
                    self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, screen_height)
                    actual_height += screen_height

        raise AssertionError(f'Мероприятие {event_name} не найдено на диаграмме')

    @antistale
    def select_event(self, name):
        event = self.get_event(name)
        event.click()
        time.sleep(1)
        return True

    def delete_event(self, name):
        with allure.step(f'Удалить мероприятие'):
            self.select_event(name)
            self.find_and_click(self.LOCATOR_TRASH_ICON)
            self.find_and_click(Modals.LOCATOR_ACCEPT_BUTTON)
        with allure.step(f'Проверить исчезание мероприятия после удаления'):
            event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, '{name}')]")
            assert self.is_element_disappearing(event_locator, wait_display=False, time=15), 'Мероприятие не исчезает после удаления'

    def copy_event(self, name):
        self.select_event(name)
        self.find_and_click(self.LOCATOR_COPY_ICON)
        self.find_element(self.LOCATOR_MODAL_TITLE, time=10)

    @antistale
    def open_event(self, event_name, **kwargs):
        # Экспериментальная версия
        event = self.get_event(event_name)
        action = ActionChains(self.driver)
        event.click()
        time.sleep(2)
        action.double_click(event).perform()
        title = self.get_title()
        assert title == event_name
        return True

    @antistale
    def scroll_to_gantt_top(self):
        try:
            scroll = self.find_element(self.LOCATOR_GANTT_SCROLL, time=3)
        except TimeoutException:
            return None
        self.driver.execute_script("arguments[0].scrollTop = 0;", scroll)

    @antistale
    def get_events(self, names_only=False, grouped=False):
        if grouped:
            events = {}

            def add_in_group(item, dictionary, group_value):
                if ' , ' in group_value:
                    group_values = group_value.split(' , ')
                    for value in group_values:
                        if value in dictionary.keys():
                            dictionary[value].append(item)
                        else:
                            dictionary[value] = [item]
                else:
                    if group_value in dictionary.keys():
                        dictionary[group_value].append(item)
                    else:
                        dictionary[group_value] = [item]
                return dictionary

            summary = None
            for event in self.events_generator():
                if not event:
                    return events
                if 'summary-bar' in event.get_attribute('class'):
                    summary = event.text
                else:
                    if names_only:
                        add_in_group(event.text, events, summary)
                    else:
                        add_in_group(event, events, summary)
            return events
        else:
            events = [event for event in self.events_generator(names_only=names_only) if event is not None]
            return events

    @antistale
    def check_plan_events(self, plan_uuid, version, login, filter_set, group_by=None):
        api = self.api_creator.get_api_eu()
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

        if filter_set.get('unfilled_events_filter').get('Скрывать мероприятия при фильтрации') is False:
            all_api_events = api.api_get_events(version, plan_uuid, login, group_by=group_by)
            filtered_api_events = api.api_get_events(version, plan_uuid, login, filter_set=filter_set)
            if group_by:
                ui_events = {}
            else:
                ui_events = []
            for event in self.events_generator():
                event_name = event.text
                assert event_name in all_api_events
                if event_name in all_api_events and event_name in filtered_api_events:
                    assert 'filter-hide' not in event.get_attribute('class')
                elif event_name in all_api_events and event_name not in filtered_api_events:
                    assert 'filter-hide' in event.get_attribute('class')
                if group_by:
                    summary = None
                    if 'summary-bar' in event.get_attribute('class'):
                        summary = event.text
                    self.add_in_group(event_name, ui_events, summary)
                else:
                    ui_events.append(event_name)
            assert self.compare_lists(all_api_events, ui_events), f'Мероприятия в API и UI не совпадают. API - {len(all_api_events)} шт, UI - {len(ui_events) if type(ui_events) is list else "None"} шт \n ui_events: \n {ui_events}'

        else:
            api_events = api.api_get_events(version, plan_uuid, login, filter_set=filter_set, group_by=group_by)
            ui_events = self.get_events(grouped=group_by, names_only=True)
            if type(ui_events) is dict:
                self.compare_dicts(ui_events, api_events)
            else:
                assert self.compare_lists(api_events, ui_events), f'Мероприятия в API и UI не совпадают. API - {len(api_events)} шт, UI - {len(ui_events) if type(ui_events) is list else "None"} шт \n ui_events: \n {ui_events} \n api_events: \n {api_events}'

    def set_grouping(self, group_value):
        self.find_and_click(self.LOCATOR_GROUPING_ICON)
        value_locator = (By.XPATH, f"//div[contains(@class, 'gantt-overlay-menu')]//div[contains(@class, 'filter-dropdown-item') and text()=' {group_value} ']")
        value = self.find_element(value_locator)
        if 'selected' in value.get_attribute('class'):
            pass
        else:
            value.click()
        time.sleep(3)
        self.find_and_click(self.LOCATOR_GROUPING_ICON)

    def unset_grouping(self, group_value):
        self.find_and_click(self.LOCATOR_GROUPING_ICON)
        value_locator = (By.XPATH, f"//div[contains(@class, 'gantt-overlay-menu')]//div[contains(@class, 'filter-dropdown-item') and text()=' {group_value} ']")
        value = self.find_element(value_locator)
        if 'selected' in value.get_attribute('class'):
            value.click()
        else:
            pass
        time.sleep(3)
        self.find_and_click(self.LOCATOR_GROUPING_ICON)

    def get_grouping_value(self):
        self.find_and_click(self.LOCATOR_GROUPING_ICON)
        values_locator = (By.XPATH, f"//div[contains(@class, 'gantt-overlay-menu')]//div[contains(@class, 'selected')]")
        row = self.find_element(values_locator)
        value = row.text.split('\n')[0]
        self.find_and_click(self.LOCATOR_GROUPING_ICON)
        return value

    def get_versions_names(self):
        self.open_versions_list()
        version_name_locator = (By.XPATH, "//div[contains(@class, 'filter-dropdown-item')]//div[1]")
        names = [version.text for version in self.elements_generator(version_name_locator)]
        self.close_versions_list()
        return names
