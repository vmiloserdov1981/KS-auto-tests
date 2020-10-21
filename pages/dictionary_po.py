from core import BasePage
from pages.components.trees import Tree
import allure


class DictionaryPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)

    def create_dictionary(self, parent_node, dict_name):
        with allure.step(f'Создать справочник {dict_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать справочник'))
            self.tree.modal.enter_and_save(dict_name)
        with allure.step(f'Проверить отображение справочника {dict_name} в дереве справочников выбранным'):
            assert self.tree.get_selected_node_name() == dict_name, f'В дереве не выбрана нода {dict_name}'
        with allure.step(f'Проверить переход на страницу вновь соданного справочника'):
            assert self.get_entity_page_title() == dict_name.upper(), f'Некорректный заголовок на странице справочника'
0