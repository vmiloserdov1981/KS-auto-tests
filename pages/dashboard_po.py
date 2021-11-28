from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from pages.components.modals import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure


class DashboardPage(EntityPage):
    LOCATOR_DASHBOARD_SETTINGS_BUTTON = (By.XPATH, "//ks-button[.//*[local-name()='svg' and @data-icon='cog']]")
    LOCATOR_DASHBOARD_ADD_INPUT_EVENT_BUTTON = (By.XPATH, "//pkm-dashboard-settings-group[.//div[.='Входящие события']]//fa-icon[.//*[local-name()='svg' and @data-icon='plus']]")
    LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON = (By.XPATH, "//pkm-dashboard-side-panel//button[.=' Сохранить ' or .='Сохранить']")
    LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR = (By.XPATH, "//pkm-dashboard-settings-group[.//div[.='Связанная сущность']]")
    LOCATOR_DASHBOARD_COMMON_SETTINGS_DROPDOWN_LOCATOR = (By.XPATH, "//pkm-dashboard-settings-group[.//div[.='Общие настройки']]")
    LOCATOR_ADD_INPUT_EVENT_BUTTON_LOCATOR = (By.XPATH, "//pkm-dashboard-settings-group[.//div[.='Входящие события']]//fa-icon[.//*[local-name()='svg' and contains(@data-icon, 'plus')]]")
    LOCATOR_DASHBOARD_TWO_SPLIT_BUTTON = (By.XPATH, "//div[contains(@class, 'overlay-item') and .//fa-icon[.//*[local-name()='svg' and @data-icon='faCell-2/1']]]")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    @staticmethod
    def dashboard_cell_locator_creator(cell_name):
        locator = (By.XPATH, f"(//pkm-dashboard-cell[.//div[contains(@class, 'cell-title') and .=' {cell_name} ']])[last()]")
        return locator

    @staticmethod
    def option_locator_creator(option_name):
        locator = (By.XPATH, f"(//*[local-name()='ks-checkbox' or local-name()='pkm-checkbox'])[.//div[contains(@class, 'checkbox-label') and .='{option_name}']]")
        return locator

    def wait_page_title(self, title, timeout=15):
        expected_title_locator = (By.XPATH, f"//div[contains(@class, 'header__title' ) and .=' {title} ']")
        try:
            self.find_element(expected_title_locator, time=timeout)
        except TimeoutException:
            raise AssertionError('Переход на страницу дашборда не осуществлен')

    def create_dashboard(self, parent_node, dashboard_name):
        with allure.step(f'Создать дашборд {dashboard_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать интерфейс'))
            self.tree.modal.enter_and_save(dashboard_name)
        with allure.step(f'Проверить отображение дашборда {dashboard_name} в дереве выбранным'):
            self.tree.wait_selected_node_name(dashboard_name)
        with allure.step(f'Проверить переход на страницу вновь соданного дашборда'):
            self.wait_page_title(dashboard_name)

    def set_single_input_event_dropdown(self, dropdown_name, dropdown_value):
        dropdown_locator = (By.XPATH, f"//div[contains(@class, 'form-col') and .//div[.='{dropdown_name}']]//ks-dropdown")
        option_locator = (By.XPATH, f"//div[@class='single-dropdown-item' and .=' {dropdown_value} ']")
        self.find_and_click(dropdown_locator)
        self.find_and_click(option_locator)

    def set_multiple_input_event_dropdown(self, dropdown_name, dropdown_values):
        dropdown_locator = (By.XPATH, f"//div[@class='form-col' and .//div[.='{dropdown_name}']]//ks-dropdown")
        self.find_and_click(dropdown_locator)
        for dropdown_value in dropdown_values:
            option_locator = (By.XPATH, f"//div[@class='multiple-dropdown-item' and .=' {dropdown_value} ']")
            self.find_and_click(option_locator)
        self.find_and_click(dropdown_locator)

    def set_menu_dashboard(self, menu_diagram_name):
        with allure.step('Задать входящее событие дашборда'):
            self.find_and_click(self.LOCATOR_DASHBOARD_SETTINGS_BUTTON)
            self.find_and_click(self.LOCATOR_DASHBOARD_ADD_INPUT_EVENT_BUTTON)
            self.set_single_input_event_dropdown('Тип события', 'Получение интерфейса')
            self.set_single_input_event_dropdown('Действие', 'Получить')
            self.set_multiple_input_event_dropdown('Источник', ['Ячейка 0'])
            self.find_and_click(self.modal.LOCATOR_SAVE_BUTTON)
            self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)
        with allure.step(f'Свяать ячейку с диаграммой {menu_diagram_name}'):
            self.find_and_click((By.XPATH, "//pkm-dashboard-cell"))
            self.find_and_click(self.LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR)
            self.set_single_input_event_dropdown('Тип сущности', 'Диаграмма')
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Диаграмма']"), menu_diagram_name)
            self.find_and_click(self.dropdown_value_locator_creator(menu_diagram_name))
        with allure.step('Отключить отображение навигатора'):
            self.uncheck_option('Отображать навигатор')
        with allure.step('Сохранить настройки ячейки'):
            self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)

    def double_split_cell(self, cell_name):
        split_cell_button_locator = (By.XPATH, f"//div[contains(@class, 'cell-content-container') and .//div[contains(@class, 'cell-title') and .=' {cell_name} ']]//fa-icon[.//*[local-name()='svg' and @data-icon='table']]")
        self.find_and_click(split_cell_button_locator)
        self.find_and_click(self.LOCATOR_DASHBOARD_TWO_SPLIT_BUTTON)

    def check_option(self, option_name):
        option_locator = self.option_locator_creator(option_name)
        if 'checkbox-selected' not in self.get_element_html(option_locator):
            self.find_and_click(option_locator)

    def uncheck_option(self, option_name):
        option_locator = self.option_locator_creator(option_name)
        if 'checkbox-selected' in self.get_element_html(option_locator):
            self.find_and_click(option_locator)

    def set_dictionaries_dashboard(self, dictionaries_diagram_name, table_name):
        with allure.step('Разделить дашборд на 2 ячейки'):
            self.double_split_cell('Ячейка 0')
        with allure.step(f'Связать ячейку 1 с диаграммой {dictionaries_diagram_name}'):
            self.find_and_click(self.dashboard_cell_locator_creator('Ячейка 1'))
            self.find_and_click(self.LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR)
            self.set_single_input_event_dropdown('Тип сущности', 'Диаграмма')
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Диаграмма']"), dictionaries_diagram_name)
            self.find_and_click(self.dropdown_value_locator_creator(dictionaries_diagram_name))
        with allure.step('Добавить входящее событие для ячейки'):
            self.find_and_click(self.LOCATOR_ADD_INPUT_EVENT_BUTTON_LOCATOR)
            self.set_single_input_event_dropdown('Тип события', 'Подсветить фигуру')
            self.set_multiple_input_event_dropdown('Источник', ['Ячейка 1'])
            self.find_and_click(self.modal.LOCATOR_SAVE_BUTTON)
        with allure.step('Отключить отображение навигатора'):
            self.uncheck_option('Отображать навигатор')
        with allure.step('Сохранить настройки ячейки'):
            self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)

        with allure.step(f'Связать ячейку 2 с таблицей {table_name}'):
            self.find_and_click(self.dashboard_cell_locator_creator('Ячейка 2'))
            self.find_and_click(self.LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR)
            self.set_single_input_event_dropdown('Тип сущности', 'Таблица')
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Таблица']"), table_name)
            self.find_and_click(self.dropdown_value_locator_creator(table_name))
        with allure.step('Добавить входящее событие для ячейки'):
            self.find_and_click(self.LOCATOR_ADD_INPUT_EVENT_BUTTON_LOCATOR)
            self.set_single_input_event_dropdown('Тип события', 'Получение таблицы')
            self.set_single_input_event_dropdown('Действие', 'Поместить')
            self.set_multiple_input_event_dropdown('Источник', ['Ячейка 1'])
            self.find_and_click(self.modal.LOCATOR_SAVE_BUTTON)
        with allure.step('Сохранить настройки ячейки'):
            self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)

    def set_events_plan_dashboard(self, model_name, gantt_name, table_name):
        cell_name_input_locator = (By.XPATH, "//div[contains(@class, 'form-row') and .//div[contains(@class, 'form-label') and .='Название ячейки']]//input")
        name_size_input_locator = (By.XPATH, "//div[contains(@class, 'form-row') and .//div[contains(@class, 'form-label') and .='Размер названия']]//input")
        with allure.step('Разделить дашборд на 2 ячейки'):
            self.double_split_cell('Ячейка 0')
        with allure.step('Изменить название ячейки 1 на "План мероприятий"'):
            self.find_and_click(self.dashboard_cell_locator_creator('Ячейка 1'))
            self.find_and_click(self.LOCATOR_DASHBOARD_COMMON_SETTINGS_DROPDOWN_LOCATOR)
            cell_name_input = self.find_element(cell_name_input_locator)
            cell_name_input.send_keys(Keys.CONTROL + "a")
            cell_name_input.send_keys(Keys.DELETE)
            self.find_and_enter(cell_name_input_locator, 'План мероприятий')
        with allure.step('Задать отображение крупного текста в ячейке'):
            self.find_and_click(name_size_input_locator)
            self.find_and_click(self.dropdown_value_locator_creator('Крупный'))
        with allure.step(f'Связать ячейку "План мероприятий" с диаграммой Ганта {gantt_name}'):
            self.find_and_click(self.LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR)
            self.set_single_input_event_dropdown('Тип сущности', 'Диаграмма Ганта')
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Модель']"), model_name)
            self.find_and_click(self.dropdown_value_locator_creator(model_name))
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Диаграмма Ганта']"), gantt_name)
            self.find_and_click(self.dropdown_value_locator_creator(gantt_name))
        with allure.step(f'Настроить опции диаграммы Ганта'):
            self.check_option('Добавление/удаление элементов')
            self.check_option('Компактный режим')
            self.check_option('Настройка отображения')
            self.check_option('Фильтрация')
            self.uncheck_option('Сравнение')
            self.check_option('Настройка масштаба')
        with allure.step('Сохранить настройки ячейки'):
            self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)

        with allure.step('Изменить название ячейки 2 на "График затрат"'):
            self.find_and_click(self.dashboard_cell_locator_creator('Ячейка 2'))
            self.find_and_click(self.LOCATOR_DASHBOARD_COMMON_SETTINGS_DROPDOWN_LOCATOR)
            cell_name_input = self.find_element(cell_name_input_locator)
            cell_name_input.send_keys(Keys.CONTROL + "a")
            cell_name_input.send_keys(Keys.DELETE)
            self.find_and_enter(cell_name_input_locator, 'График затрат')
        with allure.step('задать отображение крупного текста в ячейке'):
            self.find_and_click(name_size_input_locator)
            self.find_and_click(self.dropdown_value_locator_creator('Крупный'))
        with allure.step(f'Связать ячейку "График затрат" с таблицей {table_name}'):
            self.find_and_click(self.LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR)
            self.set_single_input_event_dropdown('Тип сущности', 'Таблица')
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Модель']"), model_name)
            self.find_and_click(self.dropdown_value_locator_creator(model_name))
            self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Таблица']"), table_name)
            self.find_and_click(self.dropdown_value_locator_creator(table_name))
        with allure.step(f'Настроить опции таблицы'):
            self.check_option('Подсветка изменений')
            self.uncheck_option('Фильтр таблицы')
            self.uncheck_option('Генерация событий по заголовкам')
            self.uncheck_option('Генерация событий по ячейкам')
        with allure.step('Сохранить настройки ячейки'):
            self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)
