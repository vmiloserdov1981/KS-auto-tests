from pages.components.entity_page import NewEntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import allure


class ClassPage(NewEntityPage):
    LOCATOR_ADD_FORMULA_INDICATOR_BUTTON = (By.XPATH, "//pkm-indicator-formula-field//fa-icon[@icon='plus']")
    LOCATOR_FX_FORMULA_BUTTON = (By.XPATH, "//pkm-indicator-formula-field//div[@class='icon-button' and .='fx']")
    LOCATOR_ADD_FORMULA_INDICATOR_FIELD = (By.XPATH, "//pkm-indicator-formula-field//input")
    LOCATOR_FUNCTIONS_CONTAINER = (By.XPATH, "//div[contains(@class, 'functions-container')]")

    INDICATORS_LIST_NAME = 'Показатели'
    DIMENSIONS_LIST_NAME = 'Измерения'
    RELATIONS_LIST_NAME = 'Связи'
    FORMULAS_LIST_NAME = 'Формулы'
    BASE_INDICATOR_NAME = 'Показатель'
    BASE_CLASS_RELATION_NAME = 'Класс-связь'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    @staticmethod
    def function_button_locator_creator(function_name):
        locator = (By.XPATH, f"(//div[contains(@class, 'function-symbol')])[.='{function_name}' or .=' {function_name} ']")
        return locator

    @staticmethod
    def function_modal_button_locator_creator(function_name):
        locator = (By.XPATH, f"(//div[contains(@class, 'function-item')])[.='{function_name}' or .=' {function_name} ']")
        return locator

    def get_class_dimensions(self, timeout=5):
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME, timeout=timeout)
        return elements

    def get_class_indicators(self, timeout=5):
        elements = self.get_list_elements_names(self.INDICATORS_LIST_NAME, timeout=timeout)
        return elements

    def get_class_relations(self, timeout=5):
        relation_name_locator = (By.XPATH, "//div[contains(@class, 'container-table') and .//div[contains(@class, 'header__title') and .='Связи']]//div[contains(@class, 'content__row_up-relation')]")
        relation_elements = self.elements_generator(relation_name_locator, time=timeout)
        relations = [element.text for element in relation_elements] if relation_elements else None
        return relations

    def select_relation(self, relation_name):
        self.find_and_click(self.class_relation_link_locator_creator(relation_name))
        time.sleep(3)

    def get_indicator_dimensions(self, timeout=5):
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME, timeout=timeout)
        return elements

    def get_indicator_formulas(self, timeout=5):
        current_tab_name = self.get_active_page_tab_name()
        self.switch_to_tab('Формулы')
        elements = self.get_list_elements_names(self.FORMULAS_LIST_NAME, timeout=timeout)
        self.switch_to_tab(current_tab_name)
        return elements

    def get_class_page_data(self, timeout: int = None) -> dict:
        if timeout:
            template = {
                'class_name': (self.get_entity_page_title, (), {"return_raw": True, "timeout": timeout}),
                'indicators': [self.get_class_indicators, (), {"timeout": timeout}],
                'dimensions': [self.get_class_dimensions, (), {"timeout": timeout}],
                'relations': [self.get_class_relations, (), {"timeout": timeout}]
            }
        else:
            template = {
                'class_name': (self.get_entity_page_title, (), {"return_raw": True}),
                'indicators': [self.get_class_indicators],
                'dimensions': [self.get_class_dimensions],
                'relations': [self.get_class_relations]
            }
        data = self.get_page_data_by_template(template)
        return data

    def create_class(self, parent_node, class_name, with_check=False):
        with allure.step(f'Создать класс {class_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать класс'))
            self.tree.modal.enter_and_save(class_name)
        with allure.step(f'Проверить переход на страницу вновь соданного класса'):
            self.wait_page_title(class_name)
        with allure.step(f'Проверить отображение класса {class_name} в дереве классов выбранным'):
            self.tree.wait_selected_node_name(class_name)
        if with_check:
            with allure.step(f'Проверить заполнение класса данными по умолчанию'):
                actual = self.get_class_page_data(timeout=3)
                expected = {
                    'class_name': class_name,
                    'indicators': None,
                    'dimensions': None,
                    'relations': None
                }
                self.compare_dicts(actual, expected)

    def create_indicator(self, indicator_name: str, tree_parent_node: str = None, with_check: bool = False) -> dict:
        if tree_parent_node:
            with allure.step(f'Создать показатель {indicator_name} в ноде "{tree_parent_node}"'):
                self.find_and_context_click(self.tree.node_locator_creator(tree_parent_node))
                self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
                self.find_and_click(self.tree.submenu_option_locator_creator('Показатель'))
        else:
            with allure.step(f'Создать показатель {indicator_name} на странице класса'):
                self.find_and_click(self.add_entity_button_locator_creator('Показатель'))
        with allure.step(f'Укзать название показателя {indicator_name} и сохранить его'):
            self.modal.enter_and_save(indicator_name)
        with allure.step(f'Проверить переход на страницу вновь соданного показателя'):
            self.wait_page_title(indicator_name)

        if with_check:
            with allure.step(f'Проверить отображение показателя {indicator_name} в дереве классов выбранным'):
                self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, indicator_name)

            with allure.step(f'Проверить заполнение созданного показателя данными по умолчанию'):
                expected_data = {
                    'indicator_name': indicator_name,
                    'indicator_data_type': 'Число',
                    'format': None,
                    'indicator_value_type': 'Максимизирующий',
                    'can_be_timed': False,
                    'is_common_for_datasets': False,
                    'unit_measurement': None,
                    'default_consolidation': 'Сумма',
                    'dimensions': None,
                    'formulas': None
                }
                actual_data = self.get_indicator_page_data(timeout=3)
                assert actual_data == expected_data, 'Страница показателя заполнена некорректными данными'
                actual_data['indicator_name'] = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
            return actual_data

    def create_relation_indicator(self, indicator_name: str, tree_parent_node: str = None, with_check: bool = False) -> dict:
        time.sleep(5)
        if tree_parent_node:
            with allure.step(f'Создать показатель {indicator_name} в ноде "{tree_parent_node}"'):
                self.find_and_context_click(self.tree.node_locator_creator(tree_parent_node))
                self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
                self.find_and_click(self.tree.submenu_option_locator_creator('Показатель'))
        else:
            with allure.step(f'Создать показатель {indicator_name} на странице класса'):
                self.find_and_click(self.add_entity_button_locator_creator('Показатели'))
        with allure.step(f'Укзать название показателя {indicator_name} и сохранить его'):
            self.modal.enter_and_save(indicator_name)

        with allure.step(f'Проверить переход на страницу вновь соданного показателя'):
            self.wait_page_title(indicator_name.upper())

        if with_check:
            with allure.step(f'Проверить заполнение созданного показателя данными по умолчанию'):
                expected_data = {
                    'indicator_name': indicator_name,
                    'indicator_data_type': 'Число',
                    'format': None,
                    'indicator_value_type': 'Не указано',
                    'can_be_timed': False,
                    'is_common_for_datasets': False,
                    'unit_measurement': None,
                    'default_consolidation': 'Сумма',
                    'dimensions': None,
                    'formulas': None
                }
                actual_data = self.get_indicator_page_data(timeout=3)
                assert actual_data == expected_data, 'Страница показателя заполнена некорректными данными'
                actual_data['indicator_name'] = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
            return actual_data

    def get_indicator_page_data(self, timeout: int = None) -> dict:
        if timeout:
            template = {
                'indicator_name': (self.get_entity_page_title, (), {"return_raw": True, "timeout": timeout}),
                'indicator_data_type': (self.get_element_text, [self.dropdown_locator_creator('dataType')], {'time': timeout}),
                'format': (self.get_input_value, [self.input_locator_creator('dataFormat')], {'return_empty': False, 'time': timeout}),
                'indicator_value_type': (self.get_element_text, [self.dropdown_locator_creator('valueType')], {'time': timeout}),
                'can_be_timed': (self.is_checkbox_checked, [self.checkbox_locator_creator('canBeTimed', label='Может содержать временное измерение')], {'time': timeout}),
                'is_common_for_datasets': (self.is_checkbox_checked, [self.checkbox_locator_creator('common')], {'time': timeout}),
                'unit_measurement': (self.get_input_value, [self.input_locator_creator('unitMeasurement')], {'return_empty': False, 'time': timeout}),
                'default_consolidation': (self.get_element_text, [self.dropdown_locator_creator('defaultConsolidation')], {'time': timeout}),
                'dimensions': (self.get_indicator_dimensions, [], {'timeout': timeout}),
            }
        else:
            template = {
                'indicator_name': (self.get_entity_page_title, (), {"return_raw": True}),
                'indicator_data_type': (self.get_element_text, [self.dropdown_locator_creator('dataType')], {}),
                'format': (self.get_input_value, [self.input_locator_creator('dataFormat')], {'return_empty': False}),
                'indicator_value_type': (self.get_element_text, [self.dropdown_locator_creator('valueType')], {}),
                'can_be_timed': (self.is_checkbox_checked, [self.checkbox_locator_creator('canBeTimed', label='Может содержать временное измерение')], {}),
                'is_common_for_datasets': (self.is_checkbox_checked, [self.checkbox_locator_creator('common')], {}),
                'unit_measurement': (self.get_input_value, [self.input_locator_creator('unitMeasurement')], {'return_empty': False}),
                'default_consolidation': (self.get_element_text, [self.dropdown_locator_creator('defaultConsolidation')], {}),
                'dimensions': (self.get_indicator_dimensions, [], {}),
            }
        data = self.get_page_data_by_template(template)
        data['formulas'] = self.get_indicator_formulas()
        return data

    def create_relation(self, relation_name: str, destination_class_name: str, tree_parent_node: str = None, with_check: bool = False) -> dict:
        time.sleep(5)
        if tree_parent_node:
            source_class_name = tree_parent_node
            with allure.step(f'Создать класс-связь {relation_name} в ноде "{tree_parent_node}"'):
                self.find_and_context_click(self.tree.node_locator_creator(tree_parent_node))
                self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
                self.find_and_click(self.tree.submenu_option_locator_creator('Связь'))
        else:
            source_class_name = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
            with allure.step(f'Создать класс-связь {relation_name} на странице класса'):
                self.find_and_click(self.add_entity_button_locator_creator('Связь'))
        with allure.step(f'Укзать название класса назначения {destination_class_name}'):
            self.find_and_enter(self.modal.LOCATOR_CLASS_INPUT, destination_class_name)
            self.find_and_click(self.modal.dropdown_item_locator_creator(destination_class_name))
        with allure.step(f'Укзать название связи {relation_name} и создать ее'):
            self.modal.enter_and_create(relation_name)
        with allure.step(f'Проверить отображение связи {relation_name} в дереве классов выбранной'):
            self.tree.wait_selected_node_name(relation_name)

        if with_check:
            with allure.step(f'Проверить заполнение созданной связи данными по умолчанию'):
                expected_data = {
                    'relation_name': relation_name,
                    'source_class_name': source_class_name,
                    'destination_class_name': destination_class_name,
                    'dimensions': None,
                    'indicators': None
                }
                actual_data = self.get_relation_page_data(timeout=3)
                assert actual_data == expected_data, 'Страница связи заполнена некорректными данными'
                actual_data['relation_name'] = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
            return actual_data

    def get_relation_page_data(self, timeout: int = None) -> dict:
        if timeout:
            template = {
                'relation_name': (self.get_entity_page_title, [], {'return_raw': True, 'timeout': timeout}),
                'source_class_name': (self.get_input_value, [self.async_dropdown_locator_creator('source')], {'time': timeout}),
                'destination_class_name': (
                self.get_input_value, [self.async_dropdown_locator_creator('destination')], {'time': timeout}),
                'dimensions': (self.get_list_elements_names, [self.DIMENSIONS_LIST_NAME], {'timeout': timeout}),
                'indicators': (self.get_list_elements_names, [self.INDICATORS_LIST_NAME], {'timeout': timeout})
            }
        else:
            template = {
                'relation_name': (self.get_entity_page_title, [], {'return_raw': True}),
                'source_class_name': (self.get_input_value, [self.async_dropdown_locator_creator('source')], {}),
                'destination_class_name': (self.get_input_value, [self.async_dropdown_locator_creator('destination')], {}),
                'dimensions': (self.get_list_elements_names, [self.DIMENSIONS_LIST_NAME], {}),
                'indicators': (self.get_list_elements_names, [self.INDICATORS_LIST_NAME], {})
            }
        data = self.get_page_data_by_template(template)
        return data

    def rename_indicator(self, indicator_name, new_indicator_name):
        indicators = self.get_class_indicators()
        self.hover_over_element(self.list_element_creator('Показатели', indicator_name))
        self.find_and_click(self.list_element_edit_button_locator_creator(self.INDICATORS_LIST_NAME, indicator_name))
        self.modal.enter_and_save(new_indicator_name, clear_input=True)
        self.find_element(self.list_element_creator('Показатели', new_indicator_name), time=20)
        for n, i in enumerate(indicators):
            if i == indicator_name:
                indicators[n] = new_indicator_name
        assert self.get_class_indicators() == indicators, 'Некорректный список показателей класса после переименования показателя'

    def delete_indicator(self, indicator_name):
        indicator_locator = self.list_element_creator(self.INDICATORS_LIST_NAME, indicator_name)
        delete_button_locator = self.list_element_delete_button_creator(self.INDICATORS_LIST_NAME, indicator_name)
        self.hover_over_element(indicator_locator)
        self.find_and_click(delete_button_locator)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(indicator_locator, wait_display=False), f'Показатель {indicator_name} не исчезает из списка показателей класса'

    def set_indicator(self, data: dict):
        """
        data = {
            'name': 'Тип работ',
            'type': 'Справочник значений',
            'dictionary_name': 'dictionary',
            'can_be_timed': False,
            'format': '0,0.00',
            'formula': {
                        0: {
                            'type': 'function',
                            'value': 'ЕСЛИ',
                            'arguments': {
                                'Условие': {
                                    0: {
                                        'type': 'text',
                                        'value': '123+11'
                                        }
                                },
                                'Истина': {
                                    0: {
                                    'type': 'indicator',
                                    'value': 'ind_1'
                                    },
                                    1: {
                                    'type': 'text',
                                    'value': '+'
                                    },
                                    2: {
                                        'type': 'indicator',
                                        'value': 'ГОД',
                                        'arguments': {
                                            0: {
                                                'type': 'text',
                                                'value': '123'
                                            }
                                        }
                                    }
                                },
                                'Ложь': {
                                    'type': 'function',
                                    'value': '1234'
                                },
                            }
                        },
                        1: {
                            'type': 'text',
                            'value': '+'
                        },
                        2: {
                                'type': 'indicator',
                                'value': 'ind_1'
                            }
                    }
        }
        """
        if data.get('type'):
            self.set_indicator_data_type(data.get('type'))

        if data.get('dictionary_name'):
            self.set_indicator_dictionary(data.get('dictionary_name'))

        if data.get('format'):
            self.set_indicator_format(data.get('format'))

        if data.get('can_be_timed') is not None:
            self.set_indicator_timed_type(data.get('can_be_timed'))

        if data.get('formula'):
            self.create_formula(data.get('formula'))

    def set_indicator_data_type(self, data_type):
        dropdown_locator = self.dropdown_locator_creator('dataType')
        actual_type = self.get_element_text(dropdown_locator)
        if actual_type != data_type:
            self.find_and_click(dropdown_locator)
            self.find_and_click(self.dropdown_value_locator_creator(data_type))
            self.wait_until_text_in_element(dropdown_locator, data_type)

    def set_indicator_dictionary(self, dictionary_name):
        dictionary_input_locator = self.async_dropdown_locator_creator('dictionary')
        self.find_and_click(dictionary_input_locator)
        self.find_and_enter(dictionary_input_locator, dictionary_name)
        self.find_and_click(self.dropdown_value_locator_creator(dictionary_name))

    def set_indicator_timed_type(self, can_be_timed: bool):
        checkbox_locator = self.input_locator_creator('canBeTimed')
        if self.is_input_checked(checkbox_locator) != can_be_timed:
            self.find_and_click(checkbox_locator)
            assert self.is_input_checked(checkbox_locator) == can_be_timed

    def set_indicator_format(self, indicator_format: str):
        format_input_locator = self.input_locator_creator('dataFormat')
        if self.get_input_value(format_input_locator) != indicator_format:
            self.find_and_enter(format_input_locator, indicator_format)

    def create_formula(self, formula_data):
        add_formula_button_locator = self.add_entity_button_locator_creator('ФормулыКомментарий')
        last_formula_locator = (By.XPATH, f"({self.list_elements_creator('Формулы')[1]})[last()]")
        formulas_list_locator = (By.XPATH, "//div[@class='list' and .//div[@class='title' and .='Формулы'] ]//div[@class='list-body']")
        with allure.step('Создать формулу'):
            formulas_list_html = self.find_element(formulas_list_locator).get_attribute('innerHTML')
            self.find_and_click(add_formula_button_locator)
            self.wait_element_changing(formulas_list_html, formulas_list_locator)
        with allure.step('Настроить формулу'):
            self.find_and_click(last_formula_locator)
            for main_element_index in formula_data:
                self.add_formula_element(formula_data[main_element_index])

    def add_formula_element(self, element: dict, parent_function_name: str = None, parent_argument_index: int = None):

        def argument_cell_locator_creator(function_name, argument_index: int):
            locator = (By.XPATH, f"(//div[contains(@class, 'function-body') and ./div[contains(@class, 'function-title') and .=' {function_name} ']]/div/pkm-formula-list[{str(argument_index + 1)}]/div//div[@class='input-field'])[last()]")
            return locator

        main_empty_space_locator = (By.XPATH, "(//pkm-formula-list//div[@class='input-field'])[last()]")

        if parent_function_name is not None and parent_argument_index is not None:
            self.find_and_click(argument_cell_locator_creator(parent_function_name, parent_argument_index))
        else:
            self.find_and_click(main_empty_space_locator)

        if element.get('type') == 'function':
            try:
                self.find_element(self.LOCATOR_FUNCTIONS_CONTAINER, time=2)
            except TimeoutException:
                self.find_and_click(self.LOCATOR_FX_FORMULA_BUTTON)
            function_locator = ClassPage.function_button_locator_creator(element.get('value'))
            try:
                self.find_and_click(function_locator, time=3)
            except TimeoutException:
                self.find_and_click(ClassPage.function_button_locator_creator('...'))
                self.find_and_click(self.function_modal_button_locator_creator(element.get('value')))
                self.find_and_click((By.XPATH, "//button[.=' Добавить ']"))
            if element.get('arguments'):
                for argument in element.get('arguments'):
                    for argument_number in element.get('arguments').get(argument):
                        self.add_formula_element(element.get('arguments').get(argument).get(argument_number), parent_function_name=element.get('value'), parent_argument_index=argument)

        if element.get('type') == 'text':
            if parent_function_name is not None and parent_argument_index is not None:
                self.find_and_enter(argument_cell_locator_creator(parent_function_name, parent_argument_index), element.get('value'))
            else:
                self.find_and_enter(main_empty_space_locator, element.get('value'))

        if element.get('type') == 'indicator':
            self.select_formula_indicator(element.get('value'))

        self.find_and_click((By.XPATH, "(//pkm-indicator-formula-field//div[contains(@class, 'title')])[1]"))
        time.sleep(1)

    def select_formula_indicator(self, indicator_name):
        try:
            self.find_and_click(self.LOCATOR_ADD_FORMULA_INDICATOR_BUTTON, time=1)
        except TimeoutException:
            pass
        self.find_and_click(self.LOCATOR_ADD_FORMULA_INDICATOR_FIELD)
        indicator_locator = (By.XPATH, f"//div[contains(@class, 'search-item-name') and .=' {indicator_name} ']")
        self.find_and_click(indicator_locator)
