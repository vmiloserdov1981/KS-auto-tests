from pages.components.entity_page import NewEntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals, TableObjectsSetModal
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from core import antistale
import allure
import time


class TablePage(NewEntityPage):
    LOCATOR_TABLE_PAGE_TYPE_VALUE = (By.XPATH, "//ks-tabs-group[contains(@class, 'table__tabs')]//div[contains(@class, 'tab-title') and contains(@class, 'active')]")
    LOCATOR_TABLE_PAGE_TYPE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'form-row')]//div[contains(@class, 'dropdown')]")
    LOCATOR_TABLE_COLUMN_TITLE = (By.XPATH, "//pkm-table-header-top//pkm-table-header-cell")
    LOCATOR_TABLE_ROW_TITLE = (By.XPATH, "//pkm-table-header-left//pkm-table-header-cell")
#    LOCATOR_TABLE_ROW_TITLE2 = (By.XPATH, "//pkm-table-cells-container//ks-table-cell")
#    LOCATOR_TABLE_CELL = (By.XPATH, "//pkm-table-cell")
    LOCATOR_TABLE_CELL = (By.XPATH, "//ks-table-cell")
    LOCATOR_DELETE_TABLE_ENTITY_ICON = (By.XPATH, "//div[contains(@class, 'structure-list__element-buttons')]//ks-button[.//*[local-name()='svg' and @data-icon='trash']]")
    LOCATOR_ADD_OBJECT_ICON = (By.XPATH, "//div[contains(@class, 'options-container')]//ks-button[.//*[local-name()='svg' and @data-icon='plus']]")
    LOCATOR_TABLE_SCROLL_ZONE = (By.XPATH, "//pkm-table-cells-container")
    LOCATOR_ENTITY_PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'ks-page__entity-title')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)
        self.objects_modal = TableObjectsSetModal(driver)

    @staticmethod
    def table_entity_locator_creator(entity_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='list-header' and .='Поля']]//div[contains(@class, 'list-item') and .='{entity_name}']")
        return locator

    @staticmethod
    def entity_block_locator_creator(entity_type, entity_name):
        locator = (By.XPATH, f"(//div[contains(@class, 'constructor-list') and .//div[.='{entity_type}']]//pkm-structure-list-element[.//div[.='{entity_name}']])[last()]")
        return locator

    @staticmethod
    def entity_expand_arrow_locator_creator(entity_type, entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'constructor-list') and .//div[contains(@class, 'constructor-list__header-title') and .=' {entity_type} ']]//div[contains(@class, 'structure-list__element') and .//div[contains(@class, 'ks__form-column-label') and .=' {entity_name} ']]//div[contains(@class, 'arrow-wrapper')]")
        return locator

    @staticmethod
    def entity_clear_button_locator_creator(entity_type, entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'constructor-list') and .//div[contains(@class, 'constructor-list__header-title') and .=' {entity_type} ']]//div[contains(@class, 'structure-list__element') and .//div[contains(@class, 'ks__form-column-label') and .=' {entity_name} ']]//div[contains(@class, 'ks-dropdown-times')]")
        return locator

    @staticmethod
    def entity_sort_button_creator(entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'structure-list__element') and .//div[contains(@class, 'ks__form-column-label') and .=' {entity_name} ']]//ks-button[.//*[local-name()='svg' and @data-icon='sort-amount-down']]")
        return locator

    @staticmethod
    def entity_drag_zone_locator_creator(entity_type, entity_name):
        locator = TablePage.entity_block_locator_creator(entity_type, entity_name)
        return locator

    @staticmethod
    def entity_type_drag_zone_locator_creator(entity_type):
        locator = (By.XPATH, f"//div[@class='list-header' and .='{entity_type}']")
        return locator

    @staticmethod
    def displaying_option_checkbox_locator_creator(option_name: str):
        locator = (By.XPATH, f"//ks-constructor-settings//ks-checkbox[.='{option_name}']//div[contains(@class, 'checkbox-container')]")
        return locator

    def create_data_table(self, model_name, table_name):
        with allure.step(f'Создать таблицу {table_name} в ноде "{model_name}"'):
            self.tree.tree_chain_actions(model_name, ["Создать", "Таблица данных"])
        with allure.step(f'Укзать название таблицы {table_name} и создать ее'):
            self.modal.enter_and_save(table_name)
        with allure.step(f'Проверить переход на страницу таблицы {table_name}'):
            self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, table_name)
        with allure.step(f'Подождать стабилизацию страницы сущности'):
            self.wait_stable_page()
        with allure.step(f'Проверить отображение таблицы {table_name} в режиме конструктора'):
            self.wait_table_page_type('Конструктор')
        with allure.step(f'Проверить отображение таблицы {table_name} в дереве моделей выбранной'):
            self.tree.wait_selected_node_name(table_name, timeout=20)

    def wait_table_page_type(self, page_type):
        self.wait_until_text_in_element(self.LOCATOR_TABLE_PAGE_TYPE_VALUE, page_type, time=5)

    def switch_table_page_type(self, page_type):
        target_type_button_locator = (By.XPATH, f"//ks-tabs-group[contains(@class, 'table__tabs')]//div[contains(@class, 'tab-title') and .=' {page_type} ']")
        if 'active' not in self.find_element(target_type_button_locator).get_attribute('class'):
            self.find_and_click(target_type_button_locator)
        self.wait_stable_page()
        self.wait_table_page_type(page_type)

    def set_entity_values(self, entity_type: str, entity_name: str, values: list):
        clean_button_locator = self.entity_clear_button_locator_creator(entity_type, entity_name)
        expand_button_locator = self.entity_expand_arrow_locator_creator(entity_type, entity_name)
        try:
            self.find_and_click(clean_button_locator, time=1)
        except TimeoutException:
            self.find_and_click(expand_button_locator)
        time.sleep(1)
        for value in values:
            value_locator = (By.XPATH, f"//div[contains(@class, 'multiple-dropdown-item') and .=' {value} ']")
            self.find_and_click(value_locator)
            time.sleep(1)
        time.sleep(2)
        self.find_and_click(expand_button_locator)

    def set_entity_old(self, entity_data):
        """
        entity_data = {
            'name': 'some_name',
            'entity_type': 'Строки',
            'parent_entity_name': None,
            'additional_action': ('func', 'args', 'kwargs'),
            'values': ['option_1', 'option_2']
            'children': [
                {'name': 'yo', 'entity_type': 'Строки', 'children': None, 'additional_action': None, 'alter_parent_name': 'changed_name'}
            ]
        }
        """

        entity_name = entity_data.get('name')
        entity_type = entity_data.get('entity_type')
        parent_entity_name = entity_data.get('parent_entity_name')
        additional_action = entity_data.get('additional_action')
        children = entity_data.get('children')
        values = entity_data.get('values')

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

        if values:
            self.set_entity_values(entity_type, entity_name, values)

        if children:
            for children_data in children:
                children_data['parent_entity_name'] = entity_name if not children_data.get('alter_parent_name') else children_data.get('alter_parent_name')
                self.set_entity(children_data)
        time.sleep(2)

    def set_entity(self, entity_data):
        """
        entity_data = {
            'name': 'some_name',
            'entity_type': 'Строки',
            'parent_entity_name': None,
            'additional_action': ('func', 'args', 'kwargs'),
            'values': ['option_1', 'option_2']
            'children': [
                {'name': 'yo', 'entity_type': 'Строки', 'children': None, 'additional_action': None, 'alter_parent_name': 'changed_name'}
            ]
        }
        """

        entity_name = entity_data.get('name')
        entity_type = entity_data.get('entity_type')
        parent_entity_name = entity_data.get('parent_entity_name')
        additional_action = entity_data.get('additional_action')
        children = entity_data.get('children')
        values = entity_data.get('values')

        assert entity_name, 'Не указано название сущности'
        assert entity_type, 'Не указан тип сущности'

        if not parent_entity_name:
            add_entity_button_locator = (By.XPATH, f"//div[contains(@class, 'constructor-list__header') and .//ks-switch[.=' {entity_type} ']]//ks-add-field-button")
        else:
            add_entity_button_locator = (By.XPATH, f"//div[contains(@class, 'structure-list__element') and .//div[contains(@class, 'ks__form-column-label') and .=' {parent_entity_name} ']]//ks-add-field-button")
#        entity_type_locator = (By.XPATH, f"//div[contains(@class, 'overlay-item') and .=' {entity_name} ']")
        entity_type_locator = (By.XPATH, f"//div[contains(@class, 'overlay') and .='{entity_name}']")

        self.find_and_click(add_entity_button_locator)
        self.find_and_click(entity_type_locator)

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

        if values:
            self.set_entity_values(entity_type, entity_name, values)

        if children:
            for children_data in children:
                children_data['parent_entity_name'] = entity_name if not children_data.get('alter_parent_name') else children_data.get('alter_parent_name')
                self.set_entity(children_data)
        time.sleep(2)

    def build_table(self, model_name, table_name, table_entities, check_data: dict = None):
        with allure.step(f'Создать таблицу {table_name}'):
            self.create_data_table(model_name, table_name)

        with allure.step('Задать структуру таблицы'):
            for entity in table_entities:
                self.set_entity(entity)
        time.sleep(2)
        if check_data:
            with allure.step('Проверить корректное отображение созданной таблицы'):
                expected_cols = check_data.get('cols')
                expected_rows = check_data.get('rows')
                expected_cells = check_data.get('cells')
                self.switch_table_page_type('Таблица')
                if expected_cols:
                    with allure.step('Проверить корректное отображение колонок в таблице'):
                        actual_cols = self.get_table_cols_titles(names_only=True)
                        assert actual_cols == expected_cols, 'Фактические колонки не совпадают с ожидаемыми'
                    if expected_rows:
                        with allure.step('Проверить корректное отображение строк в таблице'):
                            actual_rows = self.get_table_rows_titles(names_only=True)
                            assert actual_rows == expected_rows, 'Фактические колонки не совпадают с ожидаемыми'
                    if expected_cells:
                        with allure.step('Проверить корректное отображение ячеек в таблице'):
                            actual_cells = self.get_table_data()
                            assert actual_cells == expected_cells, 'Фактические ячейки не совпадают с ожидаемыми'

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
            time.sleep(5)

        with allure.step('Задать сортировку по имени (А-Я)'):
            entities = [('Строки', 'Объекты'), ('Столбцы', 'Наборы данных'), ('Столбцы', 'Показатели')]
            for i in entities:
                sort_button_locator = self.entity_sort_button_creator(i[1])
                sort_by_name_locator = (By.XPATH, "//div[@class='overlay']//div[contains(@class, 'overlay-item') and .=' По названию, А - Я ']")
                self.find_and_click(sort_button_locator)
                time.sleep(1)
                option = self.find_element(sort_by_name_locator)
                if 'selected' not in option.get_attribute('class'):
                    self.find_and_click(sort_by_name_locator)
                    time.sleep(5)

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
            sort_button_locator = (By.XPATH, "//div[@class='structure-list' or @class='structure-list-element' ]//fa-icon[@icon='sort']")
            sort_by_name_locator = (
                By.XPATH, "//div[@class='overlay']//div[contains(@class, 'overlay-item') and .=' По названию, А - Я ']")
            for sort_button in self.elements_generator(sort_button_locator):
                sort_button.click()
                time.sleep(2)
                self.find_and_click(sort_by_name_locator)
                time.sleep(3)

    @staticmethod
    def get_cell_style_value(style_name: str, cell: WebElement):
        styles = [i.strip() for i in cell.get_attribute('style').split(';') if i.strip() != '']
        params = {}
        for style in styles:
            value = style.split(': ')
            params[value[0]] = value[1]                  #1 заменил на 2
        style_value = params[style_name]
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

    def columns_title_generator(self):
        scroll = self.find_element(self.LOCATOR_TABLE_SCROLL_ZONE, time=3)
        self.driver.execute_script("arguments[0].scrollTo(0, 0);", scroll)
        time.sleep(2)
        scroll_width = self.driver.execute_script("return arguments[0].scrollWidth", scroll)
        if scroll_width == 0:
            for col_title in self.elements_generator(self.LOCATOR_TABLE_COLUMN_TITLE):
                col_top = self.get_cell_style_value('top', col_title)
                col_left = self.get_cell_style_value('left', col_title)
                yield col_title, col_top, col_left

        else:
            screen_width = self.driver.execute_script("return arguments[0].clientWidth", scroll)
            left_scroll = self.driver.execute_script("return arguments[0].scrollLeft", scroll)
            previous_left_scroll = left_scroll
            title_positions = []
            while left_scroll + screen_width <= scroll_width:
                for col_title in self.elements_generator(self.LOCATOR_TABLE_COLUMN_TITLE, wait=3):
                    if col_title.text == '':
                        continue
                    col_top = self.get_cell_style_value('top', col_title)
                    col_left = self.get_cell_style_value('left', col_title)
                    position = (col_top, col_left)
                    if position not in title_positions:
                        title_positions.append(position)
                        yield col_title, col_top, col_left
                self.driver.execute_script("arguments[0].scrollBy(arguments[1], 0);", scroll, screen_width)
                left_scroll = self.driver.execute_script("return arguments[0].scrollLeft", scroll)
                if left_scroll == previous_left_scroll:
                    break
                previous_left_scroll = left_scroll

    def get_table_cols_titles(self, level_only: int = None, names_only: bool = False):
        def get_title_position(title: tuple):
            return title[1], title[2]

        if names_only:
            result = []
            for col_title in self.columns_title_generator():
                result.append((col_title[0].text, col_title[1], col_title[2]))
            result.sort(key=get_title_position)
            result = [col[0] for col in result]
            return result

        else:
            result = {}
            for col_title in self.columns_title_generator():
                col_width = self.get_cell_style_value('width', col_title[0])
                col_left = col_title[2]
                col_top = col_title[1]
                width_range = range(col_left, col_left + col_width)
                result[(col_top, width_range)] = col_title[0].text
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
            cell_value = cell.text.strip()
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
                expected_top = i[0]                     # expected_top = i[0]
#                print(expected_top)
                break

        columns_lefts = []
        for i in cols_titles_indicators:
            if cols_titles_indicators[i] == cell_data.get('indicator_name'):
                columns_lefts.append(i[1][0])           # columns_lefts.append(i[1][0])

        for i in cols_titles_datasets:
            if cols_titles_datasets[i] == cell_data.get('dataset_name'):
                target_dataset_range = i[1]              # target_dataset_range = i[1]
                break

        for i in columns_lefts:
            if i in target_dataset_range:
                expected_left = i                        # expected_left = i
#                print(expected_left)
                break

#        locator = By.XPATH, f"//pkm-table-cell[contains(@style, 'top: {expected_top}px') and contains(@style, 'left: {expected_left}px')]"
        locator = By.XPATH, f"//ks-table-cell[contains(@style, 'top: {expected_top}px') and contains(@style, 'left: {expected_left}px')]"
        return locator

    def fill_cells(self, cells_data: list, table_fields_data: dict = None):
        table_fields_data = table_fields_data or {'objects': self.get_table_rows_titles(), 'datasets': self.get_table_cols_titles(level_only=1), 'indicators': self.get_table_cols_titles(level_only=2)}

        for cell_data in cells_data:
            time.sleep(0.5)
            cell_locator = self.cell_locator_creator(cell_data, table_fields_data=table_fields_data)
            time.sleep(0.5)
            self.find_and_click(cell_locator)
            time.sleep(0.5)
            action_chains = ActionChains(self.driver)
            time.sleep(1)
            action_chains.send_keys(cell_data.get('value'), Keys.ENTER).perform()  # action_chains.send_keys(cell_data.get('value'), Keys.ENTER).perform()
            time.sleep(0.5)

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
                raise AssertionError(f'Значение ячейки не соответствует ожидаемому. Ожидаемые данные: \n {cell_data} \n Фактические данные: \n {self.get_element_text(cell_locator, ignore_error=True)}')

    def sort_entities_by_name(self):
        entities = [('Строки', 'Объекты'), ('Столбцы', 'Наборы данных'), ('Столбцы', 'Показатели')]
        for i in entities:
            sort_button_locator = self.entity_sort_button_creator(i[1])
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
        if "checkbox-icon_hidden" in self.get_element_html(checkbox_locator):
            self.find_and_click(checkbox_locator)

    def enable_objects_adding(self):
        self.check_displaying_option('Создать объект')       # self.check_displaying_option('Разрешить добавление объектов')
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
