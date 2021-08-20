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
    LOCATOR_VERSION_DROPDOWN = (By.XPATH, "//div[@stylesmodule='pr']")
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
        self.close_versions_list()
        time.sleep(2)

    @antistale
    def get_event_names(self):
        names = [event for event in self.events_generator(names_only=True)]
        return names

    @antistale
    def is_event_exists_old(self, event_name):
        try:
            self.find_element(self.LOCATOR_EVENT_NAME)
        except TimeoutException:
            return False
        for event in self.events_generator(names_only=True):
            if event_name == event:
                return True
        return False

    @antistale
    def is_event_exists(self, event_name):
        try:
            event = self.get_event(event_name)
            if event:
                return True
        except AssertionError:
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

    def events_generator_screens(self, names_only=False):
        # перебирает мероприятия поэкранно, менее стабильный, но более быстрый
        last_row_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()]")
        prelast_row_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')][last()-1]")
        rows_locator = (By.XPATH, "//div[contains(@class, 'gantt_row')]")
        stop_gen = False

        # скролл в начало диаграммы
        self.scroll_to_gantt_top()
        time.sleep(5)

        # Перебор мероприятий
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
                delta = start_height % step
                total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                new_height = 0
                while True:
                    # last screen actions

                    if new_height + step + start_height > total_height:
                        if new_height + start_height + (cell_height * 2) - delta < total_height:
                            row = self.find_element(prelast_row_locator)
                        else:
                            row = self.find_element(last_row_locator)
                        self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=false);",
                                                   row)
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
                            self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=false);",
                                                       last_row)
                            if names_only:
                                last_row_text = last_row.text
                                last_row_name = last_row_text.split('\n')[1]
                                yield last_row_name
                            else:
                                yield last_row
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
                            if names_only:
                                row_text = row.text
                                row_name = row_text.split('\n')[1]
                                yield row_name
                            else:
                                yield row

    def events_generator_new(self, names_only=False):
        # Новый
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
                last_target_row_html = last_row_html = last_row.get_attribute('innerHTML')
                last_row_top = self.driver.execute_script("return arguments[0].offsetTop", last_row)
                scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                screen_height = self.driver.execute_script("return arguments[0].offsetHeight", scrollbar)
                screen_height_range = range(scroll_top, scroll_top + screen_height)
                target_row_top = last_row_top
                # построчный перебор
                while last_row_top + (cell_height * 2) < total_height:
                    self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, cell_height)
                    self.wait_element_changing(last_row_html, last_row_locator, time=2, ignore_timeout=True)
                    last_row = self.find_element(last_row_locator)
                    last_row_html = last_row.get_attribute('innerHTML')
                    scrollbar = self.find_element(scroll_area, time=2)
                    scroll_top = self.driver.execute_script("return arguments[0].scrollTop", scrollbar)
                    screen_height_range = range(scroll_top, scroll_top + screen_height+cell_height)

                    while target_row_top in screen_height_range:
                        target_row_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@style, 'top: {target_row_top}px')]")
                        target_row = self.find_element(target_row_locator)
                        if last_target_row_html != target_row.get_attribute('innerHTML'):
                            self.scroll_to_element(target_row)
                            if names_only:
                                yield target_row.text
                            else:
                                yield target_row
                        last_target_row_html = self.find_element(target_row_locator).get_attribute('innerHTML')
                        target_row_top += cell_height
                    last_row_top = self.driver.execute_script("return arguments[0].offsetTop", last_row)
                    last_row_html = last_row.get_attribute('innerHTML')

                    if last_row_top + (cell_height * 2) >= total_height:
                        time.sleep(5)
                        scrollbar = self.find_element(scroll_area, time=2)
                        total_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollbar)
                break

    def events_generator(self, names_only=False):
        # отрефакторенный
        # перебирает мероприятия построчно, стабильный но менее быстрый
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
                cell_height = self.driver.execute_script("return arguments[0].clientHeight", last_row)
                prelast_row_html = last_row.get_attribute('innerHTML')

                # построчный перебор
                while self.driver.execute_script("return arguments[0].offsetTop", last_row) + (
                        cell_height * 2) < total_height:
                    self.driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scrollbar, cell_height)
                    self.wait_element_changing(last_row.get_attribute('innerHTML'), last_row_locator, time=2,
                                               ignore_timeout=True)
                    last_row = self.find_element(last_row_locator)
                    last_row_html = last_row.get_attribute('innerHTML')

                    # Защита от дублирования мероприятий
                    if last_row_html != prelast_row_html:
                        self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=false);", last_row)
                        if names_only:
                            yield last_row.text
                        else:
                            yield last_row
                    prelast_row_html = last_row_html
                break

    def get_event(self, event_name, wait_timeout=1) -> WebElement:
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
    def select_event_old(self, name):
        for event in self.events_generator(names_only=True):
            try:
                if event == name:
                    event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, ' {name} ')]")
                    # self.driver.execute_script("arguments[0].scrollIntoView();", event)
                    self.find_and_click(event_locator)
                    # assert 'gantt_selected' in event.get_attribute('class')
                    return True
            except IndexError:
                pass
        raise AssertionError(f'Мероприятие "{name}" не найдено')

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

    '''
    Стандартное открытие, отключил т.к. есть вероятность что не всегда открывает
    
    @antistale
    def open_event(self, event_name, start_date=None, end_date=None, from_top=False):
        found = False
        event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, ' {event_name} ')]")
        if from_top:
            for event in self.events_generator(names_only=False):
                if event.text.split('\n')[1] == event_name:
                    found = True
                    break
        else:
            try:
                time.sleep(Vars.PKM_USER_WAIT_TIME)
                self.find_element(event_locator, time=5)
                found = True
            except TimeoutException:
                found = False
                for event in self.events_generator(names_only=False):
                    if event.text.split('\n')[1] == event_name:
                        found = True
                        break
        if found:
            action = ActionChains(self.driver)
            aria_label = self.find_element(event_locator).get_attribute('aria-label')
            aria_name = aria_label.split(' Start date: ')[0].split(' Task: ')[1]
            assert aria_name == event_name
            if start_date:
                aria_start = aria_label.split(' Start date: ')[1].split(' End date: ')[0].split('-')[::-1]
                assert aria_start == start_date
            if end_date:
                aria_end = aria_label.split(' End date: ')[1].split('-')[::-1]
                assert aria_end == end_date
            self.find_and_click(event_locator)
            time.sleep(2)
            action.double_click(self.find_element(event_locator)).perform()
            title = self.get_title()
            assert title == event_name
            return True
        else:
            raise AssertionError(f'Мероприятие "{event_name}" не найдено на диаграмме')
    '''

    @antistale
    def open_event_old(self, event_name, start_date=None, end_date=None, from_top=False):
        # Ранее работающая стабильная версия
        event_locator = (By.XPATH, f"//div[contains(@class, 'gantt_row') and contains(@aria-label, ' {event_name} ')]")
        try:
            time.sleep(Vars.PKM_USER_WAIT_TIME)
            self.find_element(event_locator, time=5)
            found = True
        except TimeoutException:
            found = False
            for event in self.events_generator(names_only=False):
                if event.text.split('\n')[1] == event_name:
                    found = True
                    self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=true);", event)
                    break
        if found:
            action = ActionChains(self.driver)
            self.find_and_click(event_locator)
            time.sleep(2)
            action.double_click(self.find_element(event_locator)).perform()
            title = self.get_title()
            assert title == event_name
            return True
        else:
            raise AssertionError(f'Мероприятие "{event_name}" не найдено на диаграмме')

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
    def get_grouped_events(self):
        events = {}

        def add_in_group(item, dictionary, group_value):
            if group_value in dictionary.keys():
                dictionary[group_value].append(item)
            else:
                dictionary[group_value] = [item]
            return dictionary
        summary = None
        for event in self.events_generator():
            if 'summary-bar' in event.get_attribute('class'):
                summary = event.text.split('\n')[1]
            else:
                add_in_group(event.text.split('\n')[1], events, summary)
        return events

    @antistale
    def get_events(self, names_only=False, grouped=False):
        if grouped:
            events = {}

            def add_in_group(item, dictionary, group_value):
                if ' . ' in group_value:
                    group_values = group_value.split(' . ')
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
                    summary = event.text.split('\n')[1]
                else:
                    if names_only:
                        add_in_group(event.text.split('\n')[1], events, summary)
                    else:
                        add_in_group(event, events, summary)
            return events
        else:
            events = [event for event in self.events_generator(names_only=names_only) if event is not None]
            return events

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
                        summary = event.text.split('\n')[1]
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
                assert self.compare_lists(api_events, ui_events), f'Мероприятия в API и UI не совпадают. API - {len(api_events)} шт, UI - {len(ui_events) if type(ui_events) is list else "None"} шт \n ui_events: \n {ui_events}'

    def set_grouping(self, group_value):
        self.find_and_click(self.LOCATOR_GROUPING_ICON)
        value_locator = (By.XPATH, f"//div[contains(@class, 'gantt-overlay-menu')]//div[contains(@class, 'filter-dropdown-item') and text()=' {group_value} ']")
        value = self.find_element(value_locator)
        if 'selected' in value.get_attribute('class'):
            pass
        else:
            value.click()
        self.find_and_click(self.LOCATOR_GROUPING_ICON)

    def unset_grouping(self, group_value):
        self.find_and_click(self.LOCATOR_GROUPING_ICON)
        value_locator = (By.XPATH, f"//div[contains(@class, 'gantt-overlay-menu')]//div[contains(@class, 'filter-dropdown-item') and text()=' {group_value} ']")
        value = self.find_element(value_locator)
        if 'selected' in value.get_attribute('class'):
            value.click()
        else:
            pass
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
