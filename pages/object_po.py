from pages.components.entity_page import NewEntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
from core import antistale
import allure


class ObjectPage(NewEntityPage):

    LOCATOR_CLASS_FIELD = (By.XPATH, "//div[contains(@class, 'entity__short-name_sub-title-name')]")

    RELATIONS_LIST_NAME = 'Связи'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    @staticmethod
    def relation_row_locator_creator(src_object, relation_name, dst_object):
        locator = (By.XPATH, f"//div[contains(@class, 'object-relation-item') and .//div[contains(@class, 'body-item__up-container') and .=' {relation_name} '] and (.//div[contains(@class, 'left-name') or contains(@class, 'right-name')])[.='{src_object}' or .='{dst_object}']]")
        return locator

    @staticmethod
    def input_locator_creator(form_control_name):
        locator = (By.XPATH, f"//input[@formcontrolname='{form_control_name}']")
        return locator

    def create_object(self, object_name: str, model_name, class_name) -> dict:
        with allure.step(f'Создать объект {object_name} в ноде "{model_name}"'):
            self.find_and_context_click(self.tree.node_locator_creator(model_name), time=20)
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Объект'))
        with allure.step(f'Укзать название объекта {object_name}, класс {class_name} и создать его'):
            self.modal.object_enter_and_save(object_name, class_name)
        with allure.step(f'Проверить отображение объекта {object_name} в дереве классов выбранным'):
            self.tree.wait_selected_node_name(object_name)
        with allure.step(f'Проверить переход на страницу объекта'):
            self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, object_name)
        with allure.step(f'Собрать данные страницы объекта'):
            actual_data = self.get_object_page_data()

        return actual_data

    def get_object_description(self):
        description_input = self.input_locator_creator('shortName')
        value = self.get_input_value(description_input, time=5, return_empty=False)
        return value

    def get_object_class(self):
        class_field_value = self.get_element_text(self.LOCATOR_CLASS_FIELD)
        value = class_field_value.split('Класс:\n')[1]
        return value

    @antistale
    def get_object_relations(self):
        relation_block_locator = (By.XPATH, "//div[contains(@class, 'object-relation-item') or @class='body-item']")
        relations = []
        for element in self.elements_generator(relation_block_locator, time=5):
            value = element.text
            if '\nДобавить' in value:
                value = value.replace("\nДобавить", "")
            relation_elements = value.split('\n')
            relation = [relation_elements[1], relation_elements[0], relation_elements[2]]
            if 'faArrowAltLeftH' in element.get_attribute('innerHTML'):
                relation = relation[::-1]
            relations.append(relation)
        return relations

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
        add_relation_button_locator = (By.XPATH, f"//div[@class='body-item' and .//div[contains(@class, 'body-item__up-container') and .=' {classes_relation_name} Добавить']]//ks-button[.='Добавить']")
        related_object_input_locator = (By.XPATH, "//pkm-modal-window//input")
        src_object_name = self.get_entity_page_title()

        self.find_and_click(add_relation_button_locator)
        self.find_and_click(related_object_input_locator)
        self.find_and_click(self.dropdown_value_locator_creator(relation_object_name))
        self.find_and_click(self.modal.LOCATOR_CREATE_BUTTON)
        created_relation = self.find_element(self.relation_row_locator_creator(src_object_name, classes_relation_name, relation_object_name))
        relation_elements = created_relation.text.split('\n')
        relation = [relation_elements[1], relation_elements[0], relation_elements[2]]
        if 'faArrowAltLeftH' in created_relation.get_attribute('innerHTML'):
            relation = relation[::-1]
        return relation

    def delete_relation(self, src_name, relation_name, dst_name):
        relation_locator = self.relation_row_locator_creator(src_name, relation_name, dst_name)
        delete_button_locator = (By.XPATH, f"{relation_locator[1]}//fa-icon[@icon='trash']")
        self.hover_over_element(relation_locator)
        self.find_and_click(delete_button_locator)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON, time=10)
        assert self.is_element_disappearing(relation_locator, time=15, wait_display=False), "связь не исчезает из списка"

    def rename_title(self, title_name):
        title_container_locator = (By.XPATH, "//div[contains(@class, 'page-title-container')]")
        title_input_locator = (By.XPATH, "//div[contains(@class, 'page-title-container')]//input")
        title_save_icon_locator = (By.XPATH, "//div[contains(@class, 'page-title-container')]//*[local-name()='svg' and @data-icon='check']")
        self.find_and_click(title_container_locator)
        self.find_and_double_click(title_input_locator)
        self.find_and_enter(title_input_locator, title_name)
        self.find_and_click(title_save_icon_locator)
        self.wait_page_title(title_name)
