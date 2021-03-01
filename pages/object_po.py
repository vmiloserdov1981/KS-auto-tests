from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
import allure


class ObjectPage(EntityPage):

    LOCATOR_CLASS_FIELD = (By.XPATH, "//div[contains(@class, 'class-field')]")

    RELATIONS_LIST_NAME = 'Связи'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    def create_object(self, object_name: str, model_name, class_name) -> dict:
        with allure.step(f'Создать объект {object_name} в ноде "{model_name}"'):
            self.find_and_context_click(self.tree.node_locator_creator(model_name))
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Объект'))
        with allure.step(f'Укзать название объекта {object_name}, класс {class_name} и создать его'):
            self.modal.object_enter_and_save(object_name, class_name)

        with allure.step(f'Проверить отображение объекта {object_name} в дереве классов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, object_name)

        actual_data = self.get_object_page_data()
        return actual_data

    def get_object_description(self):
        description_input = self.input_locator_creator('shortName')
        value = self.get_input_value(description_input, time=5, return_empty=False)
        return value

    def get_object_class(self):
        class_field_value = self.get_element_text(self.LOCATOR_CLASS_FIELD)
        value = class_field_value.split('Класс: ')[1]
        return value

    def get_object_relations(self):
        elements = []
        for element in self.elements_generator(self.list_elements_creator(self.RELATIONS_LIST_NAME), time=5):
            relation_elements = element.text.split('\n')
            if 'point-left' in element.get_attribute('innerHTML'):
                relation_elements = relation_elements[::-1]
            elements.append(relation_elements)
        return elements if elements != [] else None

    def get_object_page_data(self):
        template = {
            'object_name': (self.get_entity_page_title, (), {"return_raw": True}),
            # 'changes': [self.get_change_data],
            'description': [self.get_object_description],
            'object_class': [self.get_object_class],
            'relations': [self.get_object_relations]
        }
        data = self.get_page_data_by_template(template)
        return data
