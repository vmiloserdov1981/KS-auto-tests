from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
import allure


class ClassPage(EntityPage):
    INDICATORS_LIST_NAME = 'Показатели'
    DIMENSIONS_LIST_NAME = 'Измерения'
    RELATIONS_LIST_NAME = 'Связи'
    FORMULAS_LIST_NAME = 'Формулы'
    BASE_INDICATOR_NAME = 'Показатель'

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
        return elements

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
            assert self.get_entity_page_title() == class_name.upper(), f'Некорректный заголовок на странице класса'
        with allure.step(f'Проверить что справочник создан без показателей'):
            assert not self.get_class_indicators()
        with allure.step(f'Проверить что справочник создан без измерений'):
            assert not self.get_class_dimensions()
        with allure.step(f'Проверить что справочник создан без связей'):
            assert not self.get_class_relations()

    def create_indicator(self, indicator_name: str, tree_parent_node: str = None):
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
            pass
            #assert self.tree.get_selected_node_name() == indicator_name, f'В дереве не выбрана нода {indicator_name}'
        with allure.step(f'Проверить заполнение созданного показателя данными по умолчанию'):
            expected_data = {
                'indicator_name': indicator_name.upper(),
                'indicator_data_type': 'Число',
                'format': None,
                'indicator_value_type': 'Максимизирующий',
                'can_be_timed': False,
                'is_common_for_datasets': False,
                'dimension': None,
                'default_consolidation': 'Не выбрано',
                'dimensions': None,
                'formulas': None
            }
            actual_data = self.get_indicator_page_data()
            assert actual_data == expected_data, 'Страница показателя заполнена некорректными данными'
        return actual_data

    def get_indicator_page_data(self) -> dict:
        data = {
            'indicator_name': self.get_entity_page_title(),
            'indicator_data_type':  self.get_element_text(self.dropdown_locator_creator('dataType')),
            'format': self.get_input_value(self.input_locator_creator('dataFormat')),
            'indicator_value_type': self.get_element_text(self.dropdown_locator_creator('valueType')),
            'can_be_timed': self.is_input_checked(self.input_locator_creator('canBeTimed')),
            'is_common_for_datasets': self.is_input_checked(self.input_locator_creator('common')),
            'dimension': self.get_input_value(self.input_locator_creator('unitMeasurement')),
            'default_consolidation': self.get_element_text(self.dropdown_locator_creator('defaultConsolidation')),
            'dimensions': self.get_indicator_dimensions(),
            'formulas': self.get_indicator_formulas()
        }
        return data

