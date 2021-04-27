from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals, TableObjectsSetModal
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from core import antistale
import allure
import time


class TablePage(EntityPage):
    LOCATOR_TABLE_PAGE_TYPE_VALUE = (By.XPATH, "//div[contains(@class, 'form-row')]//div[@class='input-container']")
    LOCATOR_TABLE_PAGE_TYPE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'form-row')]//div[contains(@class, 'dropdown')]")
    LOCATOR_TABLE_COLUMN_TITLE = (By.XPATH, "//pkm-table-header-top//pkm-table-header-cell")
    LOCATOR_TABLE_ROW_TITLE = (By.XPATH, "//pkm-table-header-left//pkm-table-header-cell")
    LOCATOR_TABLE_CELL = (By.XPATH, "//pkm-table-cell")
    LOCATOR_DELETE_TABLE_ENTITY_ICON = (By.XPATH, "//div[contains(@class, 'list-element-buttons')]//fa-icon[@icon='times']")
    LOCATOR_ADD_OBJECT_ICON = (By.XPATH, "//div[contains(@class, 'table-buttons')]//fa-icon[@ng-reflect-icon='plus']")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)
        self.objects_modal = TableObjectsSetModal(driver)

    @staticmethod
    def table_entity_locator_creator(entity_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='list-header' and .='Поля']]//div[contains(@class, 'list-item') and .='{entity_name}']")
        return locator

    @staticmethod
    def entity_block_locator_creator(entity_type, entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'constructor-list') and .//div[@class='list-header' and .='{entity_type}']]//div[@class='structure-list'][.//label[.='{entity_name}'] or .//div[.='{entity_name}']]")
        return locator

    @staticmethod
    def entity_sort_button_creator(entity_type, entity_name):
        entity_xpath = TablePage.entity_block_locator_creator(entity_type, entity_name)[1]
        locator = (By.XPATH, f"{entity_xpath}//fa-icon[@icon='sort']")
        return locator

    @staticmethod
    def entity_drag_zone_locator_creator(entity_type, entity_name):
        entity_block_xpath = TablePage.entity_block_locator_creator(entity_type, entity_name)[1]
        locator = (By.XPATH, f"({entity_block_xpath}//div[contains(@class, 'multi-select')])[1]")
        return locator

    @staticmethod
    def entity_type_drag_zone_locator_creator(entity_type):
        locator = (By.XPATH, f"//div[@class='list-header' and .='{entity_type}']")
        return locator

    @staticmethod
    def displaying_option_checkbox_locator_creator(option_name: str):
        locator = (By.XPATH, f"//pkm-constructor-settings//pkm-checkbox[.='{option_name}']//div[contains(@class, 'checkbox-container')]")
        return locator

    def create_data_table(self, model_name, table_name):
        with allure.step(f'Создать таблицу {table_name} в ноде "{model_name}"'):
            self.find_and_context_click(self.tree.node_locator_creator(model_name), time=20)
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Таблица данных'))
        with allure.step(f'Укзать название таблицы {table_name} и создать ее'):
            self.modal.enter_and_save(table_name)
        with allure.step(f'Проверить переход на страницу таблицы {table_name}'):
            self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, table_name.upper())
        with allure.step(f'Подождать стабилизацию страницы сущности'):
            self.wait_stable_page()
        with allure.step(f'Проверить отображение таблицы {table_name} в режиме конструктора'):
            self.wait_table_page_type('Конструктор')
        with allure.step(f'Проверить отображение таблицы {table_name} в дереве моделей выбранной'):
            self.tree.wait_selected_node_name(table_name, timeout=20)

    def wait_table_page_type(self, page_type):
        self.wait_until_text_in_element(self.LOCATOR_TABLE_PAGE_TYPE_VALUE, page_type, time=5)

    def switch_table_page_type(self, page_type):
        dropdown = self.find_element(self.LOCATOR_TABLE_PAGE_TYPE_DROPDOWN)
        if 'focused' not in dropdown.get_attribute('class'):
            dropdown.click()
        self.find_and_click(self.dropdown_value_locator_creator(page_type))
        self.wait_stable_page()
        self.wait_table_page_type(page_type)

    def set_base_structure_old(self):
        rows_drag_zone_locator = self.entity_type_drag_zone_locator_creator('Строки')
        cols_drag_zone_locator = self.entity_type_drag_zone_locator_creator('Столбцы')
        objects_entity_locator = self.table_entity_locator_creator('Настройка объекта')
        datasets_entity_locator = self.table_entity_locator_creator('Наборы данных')
        indicators_entity_locator = self.table_entity_locator_creator('Показатели')
        self.drag_and_drop(objects_entity_locator, rows_drag_zone_locator)
        self.objects_modal.set_all_objects('Объекты')
        self.drag_and_drop(datasets_entity_locator, cols_drag_zone_locator)
        datasets_entity_locator = self.entity_drag_zone_locator_creator('Столбцы', 'Наборы данных')
        self.drag_and_drop(indicators_entity_locator, datasets_entity_locator)
        time.sleep(3)

    def set_entity(self, entity_data):
        """
        entity_data = {
            'name': 'some_name',
            'entity_type': 'Строки',
            'parent_entity_name': None,
            'additional_action': ('func', 'args', 'kwargs'),
            'children': [
                {'name': 'yo', 'entity_type': 'Строки', 'children': None, 'additional_action': None}
            ]
        }
        """

        entity_name = entity_data.get('name')
        entity_type = entity_data.get('entity_type')
        parent_entity_name = entity_data.get('parent_entity_name')
        additional_action = entity_data.get('additional_action')
        children = entity_data.get('children')

        assert entity_name, 'Не указано название сущности'
        assert entity_type, 'Не указан тип сущности'

        drag_zone_locator = self.entity_type_drag_zone_locator_creator(
            entity_type) if not parent_entity_name else self.entity_drag_zone_locator_creator(entity_type,
                                                                                              parent_entity_name)
        entity_locator = self.table_entity_locator_creator(entity_name)
        self.drag_and_drop(entity_locator, drag_zone_locator)
        if additional_action:
            function = additional_action[0]
            try:
                args = additional_action[1]
            except IndexError:
                args = ()
            try:
                kwargs = additional_action[2]
            except IndexError:
                kwargs = {}
            function(*args, **kwargs)
            time.sleep(1)

        if children:
            for children_data in children:
                children_data['parent_entity_name'] = entity_name
                self.set_entity(children_data)

    def set_base_structure(self):
        with allure.step('Задать структуру таблицы'):
            rows = {
                'name': 'Настройка объекта',
                'entity_type': 'Строки',
                'additional_action': (self.objects_modal.set_all_objects, (), {}),
            }
            columns = {
                'name': 'Наборы данных',
                'entity_type': 'Столбцы',
                'children': [
                    {'name': 'Показатели', 'entity_type': 'Столбцы'}
                ]
            }
            self.set_entity(rows)
            self.set_entity(columns)
            time.sleep(3)

        with allure.step('Задать сортировку по имени (А-Я)'):
            entities = [('Строки', 'Объекты'), ('Столбцы', 'Наборы данных'), ('Столбцы', 'Показатели')]
            for i in entities:
                sort_button_locator = self.entity_sort_button_creator(i[0], i[1])
                sort_by_name_locator = (
                By.XPATH, "//div[@class='overlay']//div[contains(@class, 'overlay-item') and .=' По названию, А - Я ']")
                self.find_and_click(sort_button_locator)
                self.find_and_click(sort_by_name_locator)
                time.sleep(2)

    def set_class_objects_structure(self, class_name):
        with allure.step('Задать структуру таблицы'):
            rows = {
                'name': 'Настройка объекта',
                'entity_type': 'Строки',
                'additional_action': (self.objects_modal.set_class_objects, [class_name]),
            }
            columns = {
                'name': 'Наборы данных',
                'entity_type': 'Столбцы',
                'children': [
                    {'name': 'Показатели', 'entity_type': 'Столбцы'}
                ]
            }
            self.set_entity(rows)
            self.set_entity(columns)
            time.sleep(3)

        with allure.step('Задать сортировку по имени (А-Я)'):
            entities = [('Строки', 'Объекты класса'), ('Столбцы', 'Наборы данных'), ('Столбцы', 'Показатели')]
            for i in entities:
                sort_button_locator = self.entity_sort_button_creator(i[0], i[1])
                sort_by_name_locator = (
                By.XPATH, "//div[@class='overlay']//div[contains(@class, 'overlay-item') and .=' По названию, А - Я ']")
                self.find_and_click(sort_button_locator)
                self.find_and_click(sort_by_name_locator)
                time.sleep(2)

    @staticmethod
    def get_cell_style_value(style_name: str, cell: WebElement):
        styles = cell.get_attribute('style')
        style_value = styles.split(f'{style_name}: ')[1].split(';')[0]
        int_value = int(style_value.split('px')[0])
        return int_value

    def get_table_rows_titles(self, names_only: bool = False):
        if names_only:
            result = []
            for row_title in self.elements_generator(self.LOCATOR_TABLE_ROW_TITLE):
                result.append(row_title.text)
        else:
            result = {}
            for row_title in self.elements_generator(self.LOCATOR_TABLE_ROW_TITLE):
                row_height = self.get_cell_style_value('height', row_title)
                row_top = self.get_cell_style_value('top', row_title)
                height_range = range(row_top, row_top + row_height - 1)
                result[height_range] = row_title.text
        return result

    def get_table_cols_titles(self, level_only: int = None, names_only: bool = False):
        if names_only:
            result = []
            for col_title in self.elements_generator(self.LOCATOR_TABLE_COLUMN_TITLE):
                result.append(col_title.text)
            return result

        else:
            result = {}
            for col_title in self.elements_generator(self.LOCATOR_TABLE_COLUMN_TITLE):
                col_width = self.get_cell_style_value('width', col_title)
                col_left = self.get_cell_style_value('left', col_title)
                col_top = self.get_cell_style_value('top', col_title)
                width_range = range(col_left, col_left + col_width)
                result[(col_top, width_range)] = col_title.text
            if not level_only:
                return result
            else:
                tops = list(set([i[0] for i in result]))
                tops.sort()
                assert level_only <= len(tops), 'Заданый уровень заголовков больше количества фактических уровней'
                target_top = tops[level_only - 1]
                copy = result.copy()
                for i in result:
                    if i[0] != target_top:
                        del copy[i]
                return copy

    def get_table_data(self):
        self.wait_stable_page()
        rows_titles = self.get_table_rows_titles()
        cols_titles_datasets = self.get_table_cols_titles(level_only=1)
        cols_titles_indicators = self.get_table_cols_titles(level_only=2)
        data = []
        for cell in self.elements_generator(self.LOCATOR_TABLE_CELL):

            cell_left = self.get_cell_style_value('left', cell) + 1
            cell_top = self.get_cell_style_value('top', cell)
            cell_value = cell.text
            if cell_value and cell_value != '':
                cell_object = None
                cell_dataset = None
                cell_indicator = None

                for i in cols_titles_datasets:
                    if cell_left in i[1]:
                        cell_dataset = cols_titles_datasets[i]
                        break
                for i in cols_titles_indicators:
                    if cell_left in i[1]:
                        cell_indicator = cols_titles_indicators[i]
                        break
                for i in rows_titles:
                    if cell_top in i:
                        cell_object = rows_titles[i]
                        break

                cell_data = {
                    'object_name': cell_object,
                    'dataset_name': cell_dataset,
                    'indicator_name': cell_indicator,
                    'value': cell_value
                }

                data.append(cell_data)
        return data

    def cell_locator_creator(self, cell_data: dict, table_fields_data=None):
        """
        cell_data = {
            'object_name': 'dsd',
            'dataset_name': 'dsdf',
            'indicator_name': 'dsa'
        }
        """
        if table_fields_data is None:
            table_fields_data = {}
        table_rows_titles = table_fields_data.get('objects') or self.get_table_rows_titles()
        cols_titles_datasets = table_fields_data.get('datasets') or self.get_table_cols_titles(level_only=1)
        cols_titles_indicators = table_fields_data.get('indicators') or self.get_table_cols_titles(level_only=2)
        expected_top = None
        expected_left = None
        target_dataset_range = None

        for i in table_rows_titles:
            if table_rows_titles.get(i) == cell_data.get('object_name'):
                expected_top = i[0]
                break

        columns_lefts = []
        for i in cols_titles_indicators:
            if cols_titles_indicators[i] == cell_data.get('indicator_name'):
                columns_lefts.append(i[1][0])

        for i in cols_titles_datasets:
            if cols_titles_datasets[i] == cell_data.get('dataset_name'):
                target_dataset_range = i[1]
                break

        for i in columns_lefts:
            if i in target_dataset_range:
                expected_left = i
                break

        locator = By.XPATH, f"//pkm-table-cell[contains(@style, 'top: {expected_top}px') and contains(@style, 'left: {expected_left}px')]"
        return locator

    def fill_cells(self, cells_data: list, table_fields_data: dict = None):
        table_fields_data = table_fields_data or {'objects': self.get_table_rows_titles(), 'datasets': self.get_table_cols_titles(level_only=1), 'indicators': self.get_table_cols_titles(level_only=2)}

        for cell_data in cells_data:
            cell_locator = self.cell_locator_creator(cell_data, table_fields_data=table_fields_data)
            editable_cell_locator = (By.XPATH, f"{cell_locator[1]}//div[@contenteditable='true']")
            self.find_and_click(cell_locator)
            action_chains = ActionChains(self.driver)
            action_chains.send_keys(cell_data.get('value')).perform()
            self.find_element(editable_cell_locator).send_keys(Keys.ENTER)
            time.sleep(5)

    def wait_cell_value(self, cell_data):
        cell_locator = self.cell_locator_creator(cell_data)
        self.wait_until_text_in_element(cell_locator, cell_data.get('value'), time=20)

    def wait_cells_value(self, cells_calc_data: list, timeout=30):
        table_fields_data = {'objects': self.get_table_rows_titles(), 'datasets': self.get_table_cols_titles(level_only=1), 'indicators': self.get_table_cols_titles(level_only=2)}
        for cell_data in cells_calc_data:
            cell_locator = self.cell_locator_creator(cell_data, table_fields_data=table_fields_data)
            try:
                self.wait_until_text_in_element(cell_locator, cell_data.get('value'), time=timeout)
            except TimeoutException:
                raise AssertionError(f'Значение ячейки не соответствует ожидаемому. Ожидаемые данные: \n {cell_data}')

    def sort_entities_by_name(self):
        entities = [('Строки', 'Объекты'), ('Столбцы', 'Наборы данных'), ('Столбцы', 'Показатели')]
        for i in entities:
            sort_button_locator = self.entity_sort_button_creator(i[0], i[1])
            sort_by_name_locator = (By.XPATH, "//div[@class='overlay']//div[contains(@class, 'overlay-item') and .=' По названию, А - Я ']")
            self.find_and_click(sort_button_locator)
            self.find_and_click(sort_by_name_locator)
            time.sleep(2)

    def clear_structure(self):
        while True:
            try:
                self.find_and_click(self.LOCATOR_DELETE_TABLE_ENTITY_ICON, time=5)
                time.sleep(2)
            except TimeoutException:
                break

    @antistale
    def check_displaying_option(self, option_name: str):
        checkbox_locator = self.displaying_option_checkbox_locator_creator(option_name)
        checkbox = self.find_element(checkbox_locator)
        if "checkbox-selected" not in checkbox.get_attribute('class'):
            self.find_and_click(checkbox_locator)

    @antistale
    def uncheck_displaying_option(self, option_name: str):
        checkbox_locator = self.displaying_option_checkbox_locator_creator(option_name)
        checkbox = self.find_element(checkbox_locator)
        if "checkbox-selected" in checkbox.get_attribute('class'):
            self.find_and_click(checkbox_locator)

    def enable_objects_adding(self):
        self.check_displaying_option('Разрешить добавление объектов')
        time.sleep(3)

    def add_table_object(self, object_name: str):
        self.find_and_click(self.LOCATOR_ADD_OBJECT_ICON)
        self.modal.enter_and_save(object_name)
        self.wait_row_title(object_name)

    def wait_row_title(self, object_name, timeout=20) -> bool:
        expected_row_locator = (By.XPATH, f"({self.LOCATOR_TABLE_ROW_TITLE[1]})[.=' {object_name} ']")
        try:
            self.find_element(expected_row_locator, time=timeout)
            return True
        except TimeoutException:
            return False

