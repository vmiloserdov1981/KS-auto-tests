from pages.components.entity_page import EntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
import allure
import time


class DictionaryPage(EntityPage):
    LOCATOR_DICTIONARY_ELEMENTS = (By.XPATH, "//table//tbody//tr")
    LOCATOR_ADD_DICTIONARY_ELEMENT_BUTTON = (By.XPATH, "//ks-button[.//button[.='Элемент']]")
    LOCATOR_DICTIONARY_PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'dictionaries-header')]//div[contains(@class, 'title')]")
    LOCATOR_CHANGE_TITLE_BUTTON = (By.XPATH, "//div[contains(@class, 'dictionaries-header')]//fa-icon[*[local-name() = 'svg' and @data-icon='pen']]")
    ELEMENTS_LIST_NAME = 'Элементы'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    def create_dictionary(self, parent_node: str, dict_name: str):
        with allure.step(f'Создать справочник {dict_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать справочник'))
            self.tree.modal.enter_and_save(dict_name)
        with allure.step(f'Проверить отображение справочника {dict_name} в дереве справочников выбранным'):
            self.tree.wait_selected_node_name(dict_name, timeout=20)
        with allure.step(f'Проверить переход на страницу вновь соданного справочника'):
            self.wait_page_title(dict_name)

    def rename_title(self, title_name):
        self.find_and_click(self.LOCATOR_CHANGE_TITLE_BUTTON)
        self.modal.enter_and_save(title_name, clear_input=True)
        self.wait_page_title(title_name)
        time.sleep(2)

    def wait_page_title(self, page_title: str, timeout: int = 10):
        self.wait_until_text_in_element(self.LOCATOR_DICTIONARY_PAGE_TITLE, page_title, time=timeout)

    def get_dict_elements(self):
        elements = [element.text for element in self.elements_generator(self.LOCATOR_DICTIONARY_ELEMENTS, time=5)]
        return elements if elements != [] else None

    def get_dictionary_page_data(self) -> dict:
        template = {
            'dictionary_name': (self.get_entity_page_title, (), {"return_raw": True}),
            'elements': [self.get_dict_elements]
        }
        data = self.get_page_data_by_template(template)
        return data

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
            self.find_and_click(self.LOCATOR_ADD_DICTIONARY_ELEMENT_BUTTON)
            self.modal.enter_and_save(element_name)
            prev_elements.append(element_name)
            new_element_locator = (By.XPATH, f"{self.LOCATOR_DICTIONARY_ELEMENTS[1]}[.=' {element_name} ']")
            self.find_element(new_element_locator)
            actual_elements = self.get_dict_elements()
        with allure.step(f'Проверить отображене элемента "{element_name}" внутри списка элементов справочника'):
            assert self.compare_lists(actual_elements, prev_elements), 'Некорректный список элементов справочника'

    def delete_dict_element(self, element_name):
        element_locator = (By.XPATH, f"{self.LOCATOR_DICTIONARY_ELEMENTS[1]}[.=' {element_name} ']")
        delete_button_locator = (By.XPATH, f"{element_locator[1]}//fa-icon//*[local-name() = 'svg' and @data-icon='trash']")
        self.hover_over_element(element_locator)
        self.find_and_click(delete_button_locator)
        confirm_text_locator = (By.XPATH, "//div[contains(@class, 'modal-window-content')]//div[contains(@class, 'confirm-message')]")
        actual_deletion_modal_text = self.get_element_text(confirm_text_locator)
        assert actual_deletion_modal_text == f'Вы действительно хотите удалить элемент справочника?', 'Некорректный текст подтверждения удаления элемента справочника'
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(element_locator, wait_display=False), f'Элемент {element_name} не исчезает из списка элементов справочника'

    def rename_dict_element(self, element_name, new_element_name):
        element_locator = (By.XPATH, f"{self.LOCATOR_DICTIONARY_ELEMENTS[1]}[.=' {element_name} ']")
        rename_button_locator = (By.XPATH, f"{element_locator[1]}//fa-icon//*[local-name() = 'svg' and @data-icon='pen']")
        self.hover_over_element(element_locator)
        self.find_and_click(rename_button_locator)
        self.modal.clear_name_input()
        self.modal.enter_and_save(new_element_name)
        assert self.is_element_disappearing(element_locator, wait_display=False)
        element_locator = (By.XPATH, f"{self.LOCATOR_DICTIONARY_ELEMENTS[1]}[.=' {new_element_name} ']")
        self.find_element(element_locator)

    def check_tree_node_children(self, parent_node_name: str):
        api = self.api_creator.get_api_dictionaries()
        tree = api.get_dicts_tree()
        api_nodes = api.get_node_children_names(parent_node_name, tree=tree)
        ui_nodes = self.tree.get_node_children_names(parent_node_name)
        assert self.compare_lists(api_nodes, ui_nodes), 'Некорректный список дочерних нод'
