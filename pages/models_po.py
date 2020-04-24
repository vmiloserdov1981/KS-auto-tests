from core import BasePage
from api.api import ApiModels
from selenium.webdriver.common.by import By
from variables import PkmVars as Vars
from pages.components.modals import Modals as Modal
from selenium.webdriver import ActionChains
import time


class ModelsPage(ApiModels, Modal, BasePage):
    LOCATOR_ADD_DATASET_BUTTON = (By.XPATH, "//div[@class='list-header' and contains(div, ' Наборы данных ' )]//div[@class='header-buttons']")

    def __init__(self, driver, login, password, token=None):
        BasePage.__init__(self, driver)
        ApiModels.__init__(self, login, password, token=token)

    def add_dataset(self, dataset_name):
        self.find_and_click(self.LOCATOR_ADD_DATASET_BUTTON)
        Modal.enter_and_save(self, dataset_name)


class TableConstructor(BasePage):
    LOCATOR_ROW_FIELD = (By.XPATH, "//div[@class='list-header' and contains(div, 'Строки')]")
    LOCATOR_COL_FIELD = (By.XPATH, "//div[@class='list-header' and contains(div, 'Столбцы')]")
    LOCATOR_DATASET_ENTITY = (By.XPATH, "(//div[@class='list-item-name' and text()='Наборы данных']//..)[contains(@class, 'list-item ')]")
    LOCATOR_OBJECT_ENTITY = (By.XPATH, "(//div[@class='list-item-name' and text()='Объекты']//..)[contains(@class, 'list-item ')]")
    LOCATOR_INDICATOR_ENTITY = (By.XPATH, "(//div[@class='list-item-name' and text()='Показатели']//..)[contains(@class, 'list-item ')]")
    LOCATOR_DATASET_SELECTED_ENTITY = (By.XPATH, "//pkm-multiple-dropdown[@ng-reflect-placeholder='Наборы данных']/div")
    LOCATOR_TABLE_TYPE_ARROW = (By.XPATH, "//div[@class='field']//div[@class='arrow-wrapper']")
    LOCATOR_TABLE_TYPE_TABLE = (By.XPATH, "//div[contains(@class, 'dropdown-item ') and contains(div, 'Таблица')]")

    def create_base_structure(self):
        objects = self.find_element(self.LOCATOR_OBJECT_ENTITY)
        datasets = self.find_element(self.LOCATOR_DATASET_ENTITY)
        row_field = self.find_element(self.LOCATOR_ROW_FIELD)
        col_field = self.find_element(self.LOCATOR_COL_FIELD)
        self.drag_and_drop(objects, row_field)
        self.drag_and_drop(datasets, col_field)
        indicators = self.find_element(self.LOCATOR_INDICATOR_ENTITY)
        selected_dataset = self.find_element(self.LOCATOR_DATASET_SELECTED_ENTITY)
        self.drag_and_drop(indicators, selected_dataset)

    def switch_to_table(self):
        self.find_and_click(self.LOCATOR_TABLE_TYPE_ARROW)
        self.find_and_click(self.LOCATOR_TABLE_TYPE_TABLE)


class TablePage(BasePage):
    LOCATOR_TABLE_CANVAS = (By.XPATH, "//pkm-table-cell-container//canvas")
    LOCATOR_TABLE_CELL = (By.XPATH, "//pkm-editable-cell/div[contains(@class, 'selected-cell')]")
    LOCATOR_TABLE_CELL_RESULT = (By.XPATH, "//pkm-editable-cell/div[contains(@class, 'selected-cell')]//div[contains(@class, 'simple-cell')]")
    LOCATOR_SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Сохранить')]")
    LOCATOR_REFRESH_BUTTON = (By.XPATH, "//button[contains(text(),'Обновить данные')]")

    def fill_cell(self, position, text):
        self.find_and_click_by_offset(self.LOCATOR_TABLE_CANVAS, position[0], position[1])
        self.find_and_click(self.LOCATOR_TABLE_CELL)
        ActionChains(self.driver).send_keys(text).perform()

    def read_cell(self, position):
        self.find_and_click_by_offset(self.LOCATOR_TABLE_CANVAS, position[0], position[1])
        self.find_and_click(self.LOCATOR_TABLE_CELL)
        result = self.get_element_text(self.LOCATOR_TABLE_CELL_RESULT)
        return result

    def check_table_calculation(self):
        self.fill_cell((-250, -10), '77')
        self.fill_cell((-250, 10), '11')
        self.fill_cell((-150, -10), '22')
        self.fill_cell((-150, 10), '15')
        self.find_and_click(self.LOCATOR_SAVE_BUTTON)
        time.sleep(Vars.PKM_API_WAIT_TIME)
        self.find_and_click(self.LOCATOR_REFRESH_BUTTON)
        res_1 = self.read_cell((-50, -10))
        res_2 = self.read_cell((-50, 10))
        assert res_1 == '99', 'Расчет прошел неправильно'
        assert res_2 == '26', 'Расчет прошел неправильно'
