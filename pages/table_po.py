from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals, Calendar
from core import antistale
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
# import datetime
import allure
import time


class TablePage(EntityPage):
    DIMENSIONS_LIST_NAME = ' Измерения '

    LOCATOR_TABLE_PAGE_TYPE_VALUE = (By.XPATH, "//div[contains(@class, 'form-row')]//div[@class='input-container']")
    LOCATOR_TABLE_PAGE_TYPE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'form-row')]//div[contains(@class, 'dropdown')]")

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
            self.find_and_context_click(self.tree.node_locator_creator(model_name))
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Таблица данных'))
        with allure.step(f'Укзать название таблицы {table_name} и создать ее'):
            self.modal.enter_and_save(table_name)
        with allure.step(f'Проверить отображение таблицы {table_name} в дереве моделей выбранной'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, table_name, time=20)
        with allure.step(f'Проверить переход на страницу таблицы {table_name}'):
            self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, table_name.upper())
        with allure.step(f'Подождать стабилизацию страницы сущности'):
            self.wait_stable_page()
        with allure.step(f'Проверить отображение таблицы {table_name} в режиме конструктора'):
            self.wait_table_page_type('Конструктор')

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
