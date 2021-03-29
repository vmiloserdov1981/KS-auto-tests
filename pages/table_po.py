from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import allure
import time


class TablePage(EntityPage):
    LOCATOR_TABLE_PAGE_TYPE_VALUE = (By.XPATH, "//div[contains(@class, 'form-row')]//div[@class='input-container']")
    LOCATOR_TABLE_PAGE_TYPE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'form-row')]//div[contains(@class, 'dropdown')]")
    LOCATOR_TABLE_COLUMN_TITLE = (By.XPATH, "//pkm-table-header-top//pkm-table-header-cell")
    LOCATOR_TABLE_ROW_TITLE = (By.XPATH, "//pkm-table-header-left//pkm-table-header-cell")
    LOCATOR_TABLE_CELL = (By.XPATH, "//pkm-table-cell")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    @staticmethod
    def table_entity_locator_creator(entity_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='list-header' and .='Поля']]//div[contains(@class, 'list-item') and .='{entity_name}']")
        return locator

    @staticmethod
    def entity_block_locator_creator(entity_type, entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'constructor-list') and .//div[@class='list-header' and .='{entity_type}']]//div[@class='structure-list' and .//span[.='{entity_name}']]")
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
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, table_name, time=20)

    def wait_table_page_type(self, page_type):
        self.wait_until_text_in_element(self.LOCATOR_TABLE_PAGE_TYPE_VALUE, page_type, time=5)

    def switch_table_page_type(self, page_type):
        dropdown = self.find_element(self.LOCATOR_TABLE_PAGE_TYPE_DROPDOWN)
        if 'focused' not in dropdown.get_attribute('class'):
            dropdown.click()
        self.find_and_click(self.dropdown_value_locator_creator(page_type))
        self.wait_stable_page()
        self.wait_table_page_type(page_type)

    def set_base_structure(self):
        rows_drag_zone_locator = self.entity_type_drag_zone_locator_creator('Строки')
        cols_drag_zone_locator = self.entity_type_drag_zone_locator_creator('Столбцы')
        objects_entity_locator = self.table_entity_locator_creator('Объекты')
        datasets_entity_locator = self.table_entity_locator_creator('Наборы данных')
        indicators_entity_locator = self.table_entity_locator_creator('Показатели')
        self.drag_and_drop(objects_entity_locator, rows_drag_zone_locator)
        self.drag_and_drop(datasets_entity_locator, cols_drag_zone_locator)
        datasets_entity_locator = self.entity_drag_zone_locator_creator('Столбцы', 'Наборы данных')
        self.drag_and_drop(indicators_entity_locator, datasets_entity_locator)
        time.sleep(3)

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

    def get_table_cols_titles(self, first_rows: bool = False, names_only: bool = False):
        def take_first(data):
            return data[0]

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

            keys = list(result.keys())
            keys.sort(key=take_first, reverse=True) if not first_rows else keys.sort(key=take_first)
            target_top = keys[0][0]
            copy = result.copy()
            for i in result:
                if i[0] != target_top:
                    del copy[i]
            return copy

    def get_table_data(self):
        rows_titles = self.get_table_rows_titles()
        cols_titles_datasets = self.get_table_cols_titles(first_rows=True)
        cols_titles_indicators = self.get_table_cols_titles()
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
                    'object': cell_object,
                    'dataset': cell_dataset,
                    'indicator': cell_indicator,
                    'value': cell_value
                }

                data.append(cell_data)
        return data

    def cell_locator_creator(self, cell_data: dict):
        """
        cell_data = {
            'object_name': 'dsd',
            'dataset_name': 'dsdf',
            'indicator_name': 'dsa'
        }
        """
        table_rows_titles = self.get_table_rows_titles()
        cols_titles_datasets = self.get_table_cols_titles(first_rows=True)
        cols_titles_indicators = self.get_table_cols_titles()
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

    def fill_cell(self, cell_data, cell_value):
        cell_locator = self.cell_locator_creator(cell_data)
        editable_cell_locator = (By.XPATH, f"{cell_locator[1]}//div[@contenteditable='true']")
        cell = self.find_element(cell_locator)
        action_chains = ActionChains(self.driver)
        action_chains.double_click(cell).perform()
        self.find_and_enter(editable_cell_locator, cell_value)
        self.find_element(editable_cell_locator).send_keys(Keys.ENTER)

    def wait_cell_value(self, cell_data, expected_value):
        cell_locator = self.cell_locator_creator(cell_data)
        self.wait_until_text_in_element(cell_locator, expected_value, time=20)

    def sort_entities_by_name(self):
        entities = [('Строки', 'Объекты'), ('Столбцы', 'Наборы данных'), ('Столбцы', 'Показатели')]
        for i in entities:
            sort_button_locator = self.entity_sort_button_creator(i[0], i[1])
            sort_by_name_locator = (By.XPATH, "//div[@class='overlay']//div[contains(@class, 'overlay-item') and .=' По названию, А - Я ']")
            self.find_and_click(sort_button_locator)
            self.find_and_click(sort_by_name_locator)
            time.sleep(2)
