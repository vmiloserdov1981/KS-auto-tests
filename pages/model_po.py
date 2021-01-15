from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
import time
import allure


class ModelPage(EntityPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    def get_model_page_data(self) -> dict:
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

    def create_model(self, parent_node, model_name):
        with allure.step(f'Создать модель {model_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать модель'))
            self.tree.modal.enter_and_save(model_name)
        with allure.step(f'Проверить отображение модели {model_name} в дереве моделей выбранной'):
            assert self.tree.get_selected_node_name() == model_name, f'В дереве не выбрана нода {model_name}'
        with allure.step(f'Проверить переход на страницу вновь соданной модели'):
            assert self.get_entity_page_title() == model_name.upper(), f'Некорректный заголовок на странице модели'
