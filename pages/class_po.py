from core import BasePage
from api.api import ApiClasses
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from variables import PkmVars as Vars
from pages.components.modals import Modals as Modal
import time


class ClassPage(ApiClasses, Modal, BasePage):
    LOCATOR_INDICATOR_VALUES = (By.XPATH, "//div[@class='title' and text()=' Показатели ']//..//following-sibling::div[contains(@class, 'list-body')]//div[@class='list-item-name']")
    LOCATOR_ADD_INDICATOR_BUTTON = (By.XPATH, "//div[@class='list-header' and contains(div, ' Показатели ' )]//div[@class='header-buttons']")
    LOCATOR_TREE_TARGET_BUTTON = (By.XPATH, "//div[contains(@class,'menu-buttons')]//fa-icon[@ng-reflect-icon='far,dot-circle']")

    def __init__(self, driver, login, password, token=None):
        BasePage.__init__(self, driver)
        ApiClasses.__init__(self, login, password, token=token)

    def check_page(self, save_test_data=True, class_name=None):
        page_title = self.get_element_text(self.LOCATOR_PAGE_TITLE_BLOCK)
        self.find_and_click(self.LOCATOR_PAGE_TITLE_BLOCK)
        input_field = self.find_element(self.LOCATOR_TITLE_INPUT)
        class_page_name = input_field.get_attribute('value')
        class_page_uuid = self.get_uuid_from_url()
        nodes = self.api_get_nodes().get('data')
        if save_test_data:
            for count, node in enumerate(nodes):
                if node.get('referenceUuid') == class_page_uuid:
                    node_dict = {
                        'name': class_page_name,
                        'node_uuid': node.get('uuid')
                    }
                    self.driver.test_data[f'root_class_{count}'] = node_dict
        if class_name:
            assert class_name == class_page_name
        api_name = self.api_get_class_name_by_id(class_page_uuid)
        assert class_page_name == api_name
        assert page_title == api_name.upper()

    def get_indicators_list(self):
        list_elements = []
        elements = self.driver.find_elements(By.XPATH, "//div[@class='title' and text()=' Показатели "
                                                       "']//..//following-sibling::div[contains(@class, "
                                                       "'list-body')]//div[@class='list-item-name']")
        for element in elements:
            list_elements.append(element.text)
        return list_elements

    def add_indicator(self, ind_name):
        self.find_and_click(self.LOCATOR_ADD_INDICATOR_BUTTON)
        Modal.enter_and_save(self, ind_name)
        self.find_and_click(self.LOCATOR_TREE_TARGET_BUTTON)

    def delete_indicator(self, indicator_name):
        indicator = (By.XPATH, f"(//div[@class='title' and contains(text(), 'Показатели')]//..//following-sibling::div[contains(@class, 'list-body')]//div[@class='list-item-name'])[text()=' {indicator_name} ']")
        self.hover_over_element(indicator)
        del_icon = (By.XPATH, f"(//div[@class='title' and contains(text(), 'Показатели')]//..//..//div[@class='list-item-name'])[text()=' {indicator_name} ']//..//fa-icon[@icon='trash']")
        self.find_and_click(del_icon)
        try:
            self.find_element(indicator, time=0.5)
        except TimeoutException:
            return True
        try:
            self.wait_element_disappearing(indicator)
        except TimeoutException:
            raise AssertionError('показатель не исчез из списка показателей на странице класса')

    def rename_indicator(self, ind_name, new_ind_name):
        indicator = (By.XPATH, f"(//div[@class='title' and text()=' Показатели ']//..//following-sibling::div[contains(@class, 'list-body')]//div[@class='list-item-name'])[text()=' {ind_name} ']")
        self.hover_over_element(indicator)
        rename_icon = (By.XPATH, f"(//div[@class='title' and text()=' Показатели ']//..//..//div[@class='list-item-name'])[text()=' {ind_name} ']//..//fa-icon[@icon='pencil-alt']")
        self.find_and_click(rename_icon)
        Modal.rename_field(self, Modal.LOCATOR_NAME_INPUT, new_ind_name)
        Modal.find_and_click(self, Modal.LOCATOR_SAVE_BUTTON)


class IndicatorPage(ApiClasses, Modal, BasePage):
    LOCATOR_INDICATOR_TYPE_INPUT = (By.XPATH, "//div[@class='page-content']//input[contains(@class, 'dropdown-input')]")
    LOCATOR_ADD_FORMULA_BUTTON = (By.XPATH, "//div[@class='list-header' and contains(div, ' Формулы ' )]//div[@class='header-buttons']")
    LOCATOR_FORMULAS_VALUES = (By.XPATH, "//div[@class='title' and text()=' Формулы ']//..//following-sibling::div[contains(@class, 'list-body')]//div[contains(@class, 'list-item ')]")
    LOCATOR_FORMULA_TITLE = (By.XPATH, "//formula-field//div[@class='title']")
    LOCATOR_FORMULA_PLACEHOLDER = (By.XPATH, "//formula-field//div[@class='input-field' and @placeholder='Пустая формула']")
    LOCATOR_FORMULA_ADD_INDICATOR_BUTTON = (By.XPATH, "//formula-field//fa-icon[@icon='plus']")
    LOCATOR_FORMULA_ADD_OPERATOR_BUTTON = (By.XPATH, "//div[@class='icon-button' and text()=' ± ']")
    LOCATOR_SEARCH_INDICATORS_INPUT = (By.XPATH, "//async-dropdown-search//input")
    LOCATOR_ERROR_CIRCLE = (By.XPATH, "//formula-field//fa-icon[@icon='circle']")

    def __init__(self, driver, login, password, token=None):
        BasePage.__init__(self, driver)
        ApiClasses.__init__(self, login, password, token=token)

    def check_page(self, indicator_name, parent_class_uuid=None):
        self.wait_until_text_in_element(self.LOCATOR_PAGE_TITLE_BLOCK, indicator_name.upper())
        self.find_and_click(self.LOCATOR_PAGE_TITLE_BLOCK)
        input_field = self.find_element(self.LOCATOR_TITLE_INPUT)
        indicator_page_name = input_field.get_attribute('value')
        indicator_uuid = self.get_uuid_from_url()
        indicator_types = Vars.PKM_INDICATOR_NAME_TYPE
        assert indicator_name == indicator_page_name, 'Неверный тайтл страницы'
        indicator_type = self.find_element(self.LOCATOR_INDICATOR_TYPE_INPUT)
        assert indicator_type.get_attribute('value') == ' Число ', 'Отображается неверный тип показателя по умолчанию'
        if parent_class_uuid:
            class_indicators_names = self.api_get_indicator_names_by_class(parent_class_uuid)
            assert indicator_page_name in class_indicators_names, 'Созданного показателя нет в списке показателей ' \
                                                                  'родительского класса '
            class_indicators = self.api_get_indicators(parent_class_uuid)
            for i in class_indicators:
                if i.get('uuid') == indicator_uuid:
                    assert i.get('name') == indicator_name, 'Имя показателя в апи и на странице не совпадают'
                    assert i.get('indicator_type') == indicator_types.get(i.get(indicator_type)), 'Тип показателя в ' \
                                                                                                  'апи и на странице ' \
                                                                                                  'не совпадают '

    def set_indicator_type(self, typename):
        self.find_and_click(self.LOCATOR_INDICATOR_TYPE_INPUT)
        drop_option = (By.XPATH, f"//div[@class='dropdown-menu app-scrollbar ng-star-inserted']//div[text()=' {typename} ']//..")
        self.find_and_click(drop_option)
        self.wait_until_text_in_element_value(self.LOCATOR_INDICATOR_TYPE_INPUT, f' {typename} ')

    def get_formulas_list(self):
        list_elements = []
        elements = self.driver.find_elements(*self.LOCATOR_FORMULAS_VALUES)
        for element in elements:
            list_elements.append(element.text)
        return list_elements

    def create_formula(self, formula_name):
        self.find_and_click(self.LOCATOR_ADD_FORMULA_BUTTON)
        Modal.enter_and_save(self, formula_name)
        time.sleep(Vars.PKM_API_WAIT_TIME)
        formulas_list = self.get_formulas_list()
        assert formula_name in formulas_list

    def open_formula(self, f_name):
        formula = (By.XPATH, f"//div[@class='title' and contains(text(), 'Формулы')]//..//..//div[contains(@class,'list-item') and contains(text(), '{f_name}')]")
        self.find_and_click(formula)
        formula_title = self.get_element_text(self.LOCATOR_FORMULA_TITLE)
        assert formula_title == f_name.upper()
        self.find_element(self.LOCATOR_FORMULA_PLACEHOLDER)

    def set_consolidation_formula(self, ind_1, ind_2, consolidation_type):
        indicator_1 = (By.XPATH, f"(//div[contains(@class, 'dropdown-item')]//div[@class='search-item-title']//div[text()=' {ind_1} ']//..)[1]")
        indicator_2 = (By.XPATH, f"(//div[contains(@class, 'dropdown-item')]//div[@class='search-item-title']//div[text()=' {ind_2} ']//..)[1]")
        operator_button = (By.XPATH, f"//div[contains(@class, 'functions-container')]//div[contains(@class, 'function-symbol') and text()=' {consolidation_type} ']")
        self.find_and_click(self.LOCATOR_FORMULA_ADD_INDICATOR_BUTTON)
        self.find_and_click(indicator_1)
        self.find_and_click(self.LOCATOR_FORMULA_ADD_OPERATOR_BUTTON)
        self.find_and_click(operator_button)
        self.find_and_click(self.LOCATOR_SEARCH_INDICATORS_INPUT)
        self.find_and_click(indicator_2)
        self.wait_element_disappearing(self.LOCATOR_ERROR_CIRCLE)


