from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
import allure


class DictionaryPage(EntityPage):

    LOCATOR_DICTIONARY_ELEMENTS = (By.XPATH, "//div[@class='list' and .//div[@class='title' and .='Элементы']]//div[contains(@class, 'list-item-name')]")

    ELEMENTS_LIST_NAME = 'Элементы'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    def create_dictionary(self, parent_node, dict_name):
        with allure.step(f'Создать справочник {dict_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать справочник'))
            self.tree.modal.enter_and_save(dict_name)
        with allure.step(f'Проверить отображение справочника {dict_name} в дереве справочников выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, dict_name)
        with allure.step(f'Проверить переход на страницу вновь соданного справочника'):
            self.wait_page_title(dict_name.upper())
        with allure.step(f'Проверить что справочник создан без элементов'):
            assert not self.get_dict_elements()

    def get_dict_elements(self):
        elements = [element.text for element in self.elements_generator(self.LOCATOR_DICTIONARY_ELEMENTS, time=5)]
        return elements if elements != [] else None

    def rename_dictionary(self, new_name):
        node = self.find_element(self.tree.LOCATOR_SELECTED_NODE)
        with allure.step(f'Переименовать справочник на странице справочника'):
            self.rename_title(new_name)
        self.wait_element_replacing(node, self.tree.LOCATOR_SELECTED_NODE)
        with allure.step(f'Проверить изменение названия справочника в дереве'):
            assert self.get_element_text(self.tree.LOCATOR_SELECTED_NODE) == new_name, 'Некорректное название ноды после переименования справочника'

    def create_dict_element(self, element_name):
        with allure.step(f'Создать новый элемент справочника "{element_name}"'):
            prev_elements = self.get_dict_elements() or []
            self.find_and_click(self.add_list_element_button_creator(self.ELEMENTS_LIST_NAME))
            self.modal.enter_and_save(element_name)
            prev_elements.append(element_name)
            new_element_locator = (By.XPATH, f"{self.LOCATOR_DICTIONARY_ELEMENTS[1]}[.='{element_name}']")
            self.find_element(new_element_locator)
            actual_elements = self.get_dict_elements()
        with allure.step(f'Проверить отображене элемента "{element_name}" внутри списка элементов справочника'):
            assert self.compare_lists(actual_elements, prev_elements), 'Некорректный список элементов справочника'

    def delete_dict_element(self, element_name):
        element_locator = self.list_element_creator(f'{self.ELEMENTS_LIST_NAME}', element_name)
        self.hover_over_element(element_locator)
        self.find_and_click(self.list_element_delete_button_creator(f'{self.ELEMENTS_LIST_NAME}', element_name))
        actual_deletion_modal_text = self.modal.get_deletion_confirm_modal_text()
        assert actual_deletion_modal_text == f'Вы действительно хотите удалить\nЭлемент {element_name} ?', 'Некорректный текст подтверждения удаления элемента справочника'
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(element_locator, wait_display=False), f'Элемент {element_name} не исчезает из списка элементов справочника'

    def rename_dict_element(self, element_name, new_element_name):
        element_locator = self.list_element_creator(f'{self.ELEMENTS_LIST_NAME}', element_name)
        self.hover_over_element(element_locator)
        self.find_and_click(self.list_element_rename_button_creator(f'{self.ELEMENTS_LIST_NAME}', element_name))
        self.modal.clear_name_input()
        self.modal.enter_and_save(new_element_name)
        assert self.is_element_disappearing(element_locator, wait_display=False)
        element_locator = self.list_element_creator(f'{self.ELEMENTS_LIST_NAME}', new_element_name)
        self.find_element(element_locator)

    def check_tree_node_children(self, parent_node_name: str):
        api = self.api_creator.get_api_dictionaries()
        tree = api.get_dicts_tree()
        api_nodes = api.get_node_children_names(parent_node_name, tree=tree)
        ui_nodes = self.tree.get_node_children_names(parent_node_name)
        assert self.compare_lists(api_nodes, ui_nodes), 'Некорректный список дочерних нод'
