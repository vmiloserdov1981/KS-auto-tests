from core import BasePage
from pages.components.trees import Tree


class DictionaryPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)

    def check_test_foldedr(self):
        pass