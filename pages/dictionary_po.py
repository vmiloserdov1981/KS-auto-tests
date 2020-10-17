from core import BasePage
from pages.components.trees import Tree


class DictionaryPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)

    def create_dictionary(self, parent_node, dict_name):
        self.find_and_context_click(self.tree.node_locator_creator(parent_node))
        self.find_and_click(self.tree.context_option_locator_creator('Создать справочник'))
        self.tree.modal.enter_and_save(dict_name)

