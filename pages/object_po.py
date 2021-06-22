from pages.components.entity_page import EntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
from core import antistale
import allure


class ObjectPage(EntityPage):

    LOCATOR_CLASS_FIELD = (By.XPATH, "//div[contains(@class, 'class-field')]")

    RELATIONS_LIST_NAME = 'Связи'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    @staticmethod
    def relation_row_locator_creator(src_class, relation_name, dst_class):
        xpath = (f"(//div[@class='list' and .//div[@class='title' and .='{ObjectPage.RELATIONS_LIST_NAME}' ] ]"
                 + "//div[contains(@class, 'list-item ')])"
                 + f"[.//div[@class='object-relation-column' and .=' {src_class} '] "
                 + f"and .//div[@class='object-relation-column' and .=' {relation_name} '] "
                 + f"and .//div[@class='object-relation-column' and .=' {dst_class} ']]")
        locator = (By.XPATH, xpath)
        return locator

    def create_object(self, object_name: str, model_name, class_name) -> dict:
        with allure.step(f'Создать объект {object_name} в ноде "{model_name}"'):
            self.find_and_context_click(self.tree.node_locator_creator(model_name))
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Объект'))
        with allure.step(f'Укзать название объекта {object_name}, класс {class_name} и создать его'):
            self.modal.object_enter_and_save(object_name, class_name)

        with allure.step(f'Проверить отображение объекта {object_name} в дереве классов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, object_name)
        self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, object_name.upper())
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

    @antistale
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
            'description': [self.get_object_description],
            'object_class': [self.get_object_class],
            'relations': [self.get_object_relations]
        }
        data = self.get_page_data_by_template(template)
        return data

    def create_object_relation(self, src_class_name, classes_relation_name, dst_class_name, relation_object_name):
        current_object_name = self.get_entity_page_title(return_raw=True)
        current_object_class = self.get_object_class()
        classes_relation_row_locator = self.relation_row_locator_creator(src_class_name, classes_relation_name, dst_class_name)
        if current_object_class == dst_class_name:
            objects_relation_row_locator = self.relation_row_locator_creator(current_object_name, f'{classes_relation_name}:{relation_object_name}_{current_object_name}', relation_object_name)
        else:
            objects_relation_row_locator = self.relation_row_locator_creator(current_object_name, f'{classes_relation_name}:{current_object_name}_{relation_object_name}', relation_object_name)
        add_icon_locator = (By.XPATH, classes_relation_row_locator[1]+"//fa-icon")
        dropdown_locator = (By.XPATH, f"(//div[@class='list' and .//div[@class='title' and .='Связи' ] ]//div[contains(@class, 'list-item ')])[.//div[@class='object-relation-column' and .=' {classes_relation_name} '] ]//pkm-dropdown")
        dropdown_value_locator = self.dropdown_value_locator_creator(relation_object_name)
        self.find_and_click(add_icon_locator)
        self.find_and_click(dropdown_locator)
        self.find_and_click(dropdown_value_locator)
        self.find_element(objects_relation_row_locator)
        objects_relation_value = self.get_element_text(objects_relation_row_locator).split('\n')
        objects_relation_row = self.find_element(objects_relation_row_locator)
        if 'point-left' in objects_relation_row.get_attribute('innerHTML'):
            objects_relation_value = objects_relation_value[::-1]
        return objects_relation_value

    def delete_relation(self, src_name, relation_name, dst_name):
        relation_locator = self.relation_row_locator_creator(src_name, relation_name, dst_name)
        delete_button_locator = (By.XPATH, f"{relation_locator[1]}//fa-icon[@icon='trash']")
        self.hover_over_element(relation_locator)
        self.find_and_click(delete_button_locator)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON, time=10)
        assert self.is_element_disappearing(relation_locator, time=15, wait_display=False), "связь не исчезает из списка"
