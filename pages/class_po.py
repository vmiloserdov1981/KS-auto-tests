from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
import time
import allure


class ClassPage(EntityPage):
    INDICATORS_LIST_NAME = 'Показатели'
    DIMENSIONS_LIST_NAME = 'Измерения'
    RELATIONS_LIST_NAME = 'Связи'
    FORMULAS_LIST_NAME = 'Формулы'
    BASE_INDICATOR_NAME = 'Показатель'
    BASE_CLASS_RELATION_NAME = 'Класс-связь'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    def get_class_dimensions(self):
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME)
        return elements

    def get_class_indicators(self):
        elements = self.get_list_elements_names(self.INDICATORS_LIST_NAME)
        return elements

    def get_class_relations(self):
        elements = self.get_list_elements_names(self.RELATIONS_LIST_NAME)
        relations = [relation.split('\n')[1] for relation in elements] if elements else None
        return relations

    def select_relation(self, relation_name):
        self.find_and_click(self.class_relation_link_locator_creator(relation_name))
        time.sleep(3)

    def get_indicator_dimensions(self):
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME)
        return elements

    def get_indicator_formulas(self):
        elements = self.get_list_elements_names(self.FORMULAS_LIST_NAME)
        return elements

    def create_class(self, parent_node, class_name):
        with allure.step(f'Создать класс {class_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать класс'))
            self.tree.modal.enter_and_save(class_name)
        with allure.step(f'Проверить отображение класса {class_name} в дереве классов выбранным'):
            assert self.tree.get_selected_node_name() == class_name, f'В дереве не выбрана нода {class_name}'
        with allure.step(f'Проверить переход на страницу вновь соданного класса'):
            self.wait_page_title(class_name.upper())
        with allure.step(f'Проверить что справочник создан без показателей'):
            assert not self.get_class_indicators()
        with allure.step(f'Проверить что справочник создан без измерений'):
            assert not self.get_class_dimensions()
        with allure.step(f'Проверить что справочник создан без связей'):
            assert not self.get_class_relations()

    def create_indicator(self, indicator_name: str, tree_parent_node: str = None) -> dict:
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
        with allure.step(f'Проверить отображение показателя {indicator_name} в дереве классов выбранным'):
            #assert self.tree.get_selected_node_name() == indicator_name, f'В дереве не выбрана нода {indicator_name}'
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
                'default_consolidation': 'Не выбрано',
                'dimensions': None,
                'formulas': None
            }
            actual_data = self.get_indicator_page_data()
            assert actual_data == expected_data, 'Страница показателя заполнена некорректными данными'
            actual_data['indicator_name'] = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
        return actual_data

    def get_indicator_page_data(self) -> dict:
        self.wait_stable_page()
        data = {
            'indicator_name': self.get_entity_page_title(return_raw=True),
            'indicator_data_type':  self.get_element_text(self.dropdown_locator_creator('dataType')),
            'format': self.get_input_value(self.input_locator_creator('dataFormat'), return_empty=False),
            'indicator_value_type': self.get_element_text(self.dropdown_locator_creator('valueType')),
            'can_be_timed': self.is_input_checked(self.input_locator_creator('canBeTimed')),
            'is_common_for_datasets': self.is_input_checked(self.input_locator_creator('common')),
            'unit_measurement': self.get_input_value(self.input_locator_creator('unitMeasurement'), return_empty=False),
            'default_consolidation': self.get_element_text(self.dropdown_locator_creator('defaultConsolidation')),
            'dimensions': self.get_indicator_dimensions(),
            'formulas': self.get_indicator_formulas()
        }
        return data

    def create_relation(self, relation_name: str, destination_class_name: str, tree_parent_node: str = None) -> dict:
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
                self.find_and_click(self.add_entity_button_locator_creator('Связи'))
        with allure.step(f'Укзать название класса назначения {destination_class_name}'):
            self.find_and_enter(self.modal.LOCATOR_CLASS_INPUT, destination_class_name)
            self.find_and_click(self.modal.dropdown_item_locator_creator(destination_class_name))
        with allure.step(f'Укзать название связи {relation_name} и создать ее'):
            self.modal.enter_and_create(relation_name)
        with allure.step(f'Проверить отображение связи {relation_name} в дереве классов выбранной'):
            #assert self.tree.get_selected_node_name() == relation_name, f'В дереве не выбрана нода {relation_name}'
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, relation_name)
        with allure.step(f'Проверить заполнение созданной связи данными по умолчанию'):
            expected_data = {
                'relation_name': relation_name,
                'source_class_name': source_class_name,
                'destination_class_name': destination_class_name,
                'dimensions': None,
                'indicators': None
            }
            actual_data = self.get_relation_page_data()
            assert actual_data == expected_data, 'Страница связи заполнена некорректными данными'
            actual_data['relation_name'] = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
        return actual_data

    def get_relation_page_data(self) -> dict:
        self.wait_stable_page()
        data = {
            'relation_name': self.get_entity_page_title(return_raw=True),
            'source_class_name': self.get_input_value(self.async_dropdown_locator_creator('source')),
            'destination_class_name': self.get_input_value(self.async_dropdown_locator_creator('destination')),
            'dimensions': self.get_list_elements_names(self.DIMENSIONS_LIST_NAME),
            'indicators': self.get_list_elements_names(self.INDICATORS_LIST_NAME)
        }
        return data

    def rename_indicator(self, indicator_name, new_indicator_name):
        indicators = self.get_class_indicators()
        self.hover_over_element(self.list_element_creator('Показатели', indicator_name))
        self.find_and_click(self.list_element_edit_button_locator_creator(self.INDICATORS_LIST_NAME, indicator_name))
        self.modal.enter_and_save(new_indicator_name, clear_input=True)
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
        #assert self.is_element_disappearing(indicator_locator, wait_display=False), f'Показатель {indicator_name} не исчезает из списка показателей класса'
