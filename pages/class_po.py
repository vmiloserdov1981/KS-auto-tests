from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
import allure
from variables import PkmVars as Vars


class ClassPage(EntityPage):

    INDICATORS_LIST_NAME = 'Показатели'
    DIMENSIONS_LIST_NAME = 'Измерения'
    RELATIONS_LIST_NAME = 'Связи'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    def get_class_dimensions(self):
        elements = [element.text for element in self.elements_generator(self.list_elements_creator(self.DIMENSIONS_LIST_NAME), time=1)]
        return elements if elements != [] else None

    def get_class_indicators(self):
        elements = [element.text for element in self.elements_generator(self.list_elements_creator(self.INDICATORS_LIST_NAME), time=1)]
        return elements if elements != [] else None

    def get_class_relations(self):
        elements = [element.text for element in self.elements_generator(self.list_elements_creator(self.RELATIONS_LIST_NAME), time=1)]
        return elements if elements != [] else None

    def create_class(self, parent_node, class_name):
        with allure.step(f'Создать класс {class_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать класс'))
            self.tree.modal.enter_and_save(class_name)
        with allure.step(f'Проверить отображение класса {class_name} в дереве классов выбранным'):

            #выключить!
            self.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
            #выключить!

            assert self.tree.get_selected_node_name() == class_name, f'В дереве не выбрана нода {class_name}'
        with allure.step(f'Проверить переход на страницу вновь соданного класса'):
            assert self.get_entity_page_title() == class_name.upper(), f'Некорректный заголовок на странице класса'
        with allure.step(f'Проверить что справочник создан без показателей'):
            assert not self.get_class_indicators()
        with allure.step(f'Проверить что справочник создан без измерений'):
            assert not self.get_class_dimensions()
        with allure.step(f'Проверить что справочник создан без связей'):
            assert not self.get_class_relations()
