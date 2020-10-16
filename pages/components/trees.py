from core import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import TimeoutException
from pages.components.modals import Modals
from api.api import ApiClasses
from api.api import ApiModels
from variables import PkmVars as Vars
import time


class UserBlock(BasePage):
    LOCATOR_PKM_PROFILENAME_BLOCK = (By.XPATH, "//div[@class='profile-name']")
    LOCATOR_PKM_USER_ACTIONS_BUTTON = (By.CLASS_NAME, "user-avatar")
    LOCATOR_PKM_LOGOUT_BUTTON = (By.XPATH, "//fa-icon[@icon='sign-out-alt']")

    def check_username(self, username):
        assert self.get_element_text(self.LOCATOR_PKM_PROFILENAME_BLOCK, time=20) == username, 'В блоке профиля отображается ' \
                                                                                      'неправильное имя '

    def logout(self):
        self.find_and_click(self.LOCATOR_PKM_USER_ACTIONS_BUTTON)
        self.find_and_click(self.LOCATOR_PKM_LOGOUT_BUTTON)


class Tree(BasePage):
    LOCATOR_TREE_ARROW = (By.CLASS_NAME, "arrow-wrapper")
    LOCATOR_TREE_OPEN_BUTTON = (By.XPATH, "//div[@class='menu-open-button ng-star-inserted']")
    LOCATOR_TREE_CLASS_BUTTON = (By.XPATH, "//div[contains(@class, 'dropdown-list app-scrollbar')]//div[text()=' Классы ']")
    LOCATOR_TREE_TYPE_BLOCK = (By.XPATH, "//div[@class='display-value ng-star-inserted']")
    LOCATOR_DICTIONARY_TREE_ROOT_NODE = (By.XPATH, "//div[@class='tree-item-title' and .='Справочники']")
    DICTIONARIES_TREE_NAME = 'Справочники'

    def __init__(self, driver):
        super().__init__(driver)
        self.modal = Modals(driver)

    @staticmethod
    def folder_locator_creator(folder_name):
        locator = (By.XPATH, f"//div[@class='tree-item' and .='{folder_name}' and .//fa-icon[@ng-reflect-icon='folder']]")
        return locator

    @staticmethod
    def node_locator_creator(node_name):
        locator = (By.XPATH, f"//div[@class='tree-item' and .='{node_name}']")
        return locator

    @staticmethod
    def context_option_locator_creator(option_name):
        locator = (By.XPATH, f"//div[contains(@class, 'context-menu-body')]//div[@class='context-menu-item' and .=' {option_name} ']")
        return locator

    def open_tree(self):
        try:
            return self.find_and_click(self.LOCATOR_TREE_OPEN_BUTTON, time=5)
        except TimeoutException:
            pass

    def switch_to_tree(self, tree_name):
        tree_value = self.get_element_text(self.LOCATOR_TREE_TYPE_BLOCK)
        if tree_value != tree_name:
            tree_button_locator = (By.XPATH, f"//div[contains(@class, 'dropdown-list app-scrollbar')]//div[text()=' {tree_name} ']")
            try:
                self.find_and_click(self.LOCATOR_TREE_ARROW)
            except TimeoutException:
                self.open_tree()
                self.find_and_click(self.LOCATOR_TREE_ARROW)
            self.find_and_click(tree_button_locator)
            tree_value = self.get_element_text(self.LOCATOR_TREE_TYPE_BLOCK)
            assert tree_value == tree_name, 'Неправильное название в переключателе типа дерева'

    def is_folder_exists(self, folder_name, time=2):
        folder_locator = self.folder_locator_creator(folder_name)
        try:
            self.find_element(folder_locator, time=time)
            return True
        except TimeoutException:
            return False

    def context_selection(self, node_name, choice_name):
        node_locator = self.node_locator_creator(node_name)
        choice_locator = self.context_option_locator_creator(choice_name)
        self.find_and_context_click(node_locator)
        self.find_and_click(choice_locator)

    def create_root_folder(self, folder_name):
        self.find_and_context_click(self.LOCATOR_DICTIONARY_TREE_ROOT_NODE)
        self.find_and_click(self.context_option_locator_creator('Создать папку'))
        self.modal.enter_and_save(folder_name)
        time.sleep(3)

    def check_test_folder(self, folder_name):
        if not self.is_folder_exists(folder_name):
            self.create_root_folder(folder_name)

class TreeOld(ApiClasses, ApiModels, Modals, BasePage):
    LOCATOR_ROOT_FOLDER = (By.XPATH, "(//div[@class='tree-item-title']//div[@class='item-name'])[1]")
    LOCATOR_CREATE_FOLDER_BUTTON = (By.XPATH, "//div[@class='context-menu-item']//div[text()=' Создать папку ']")
    LOCATOR_CREATE_CLASS_BUTTON = (By.XPATH, "//div[@class='context-menu-item']//div[text()=' Создать класс ']")
    LOCATOR_CREATE_MODEL_BUTTON = (By.XPATH, "//div[@class='context-menu-item']//div[text()=' Создать модель ']")
    LOCATOR_TREE_TARGET_BUTTON = (By.XPATH, "//div[contains(@class,'menu-buttons')]//fa-icon[@ng-reflect-icon='far,dot-circle']")
    LOCATOR_DELETE_CLASS_BUTTON = (By.XPATH, "//div[@class='context-menu-item']//div[text()=' Удалить ']")
    LOCATOR_TREE_ELEMENTS = (By.XPATH, "//div[@class='tree-item-children ng-star-inserted']//div["
                                       "@class='tree-item']//div[@class='item-name']//span")
    LOCATOR_LAST_TREE_ELEMENT = (By.XPATH, "(//div[@class='tree-item-children ng-star-inserted']//div["
                                           "@class='tree-item' ]//span)[last()]")
    LOCATOR_TREE_ARROW = (By.CLASS_NAME, "arrow-wrapper")
    LOCATOR_TREE_CLASS_BUTTON = (By.XPATH, "//div[contains(@class, 'dropdown-list app-scrollbar')]//div[text()=' Классы ']")
    LOCATOR_TREE_MODEL_BUTTON = (By.XPATH, "//div[contains(@class, 'dropdown-list app-scrollbar')]//div[text()=' Модели ']")
    LOCATOR_TREE_ACTUAL_TYPE_INPUT = (By.XPATH, "//input[@placeholder='Сущность']")
    LOCATOR_TREE_TYPE_BLOCK = (By.XPATH, "//div[@class='display-value ng-star-inserted']")
    LOCATOR_TREE_ACTIVE_NODE = (By.XPATH, "//div [@class='tree-item-title selected']//span")
    LOCATOR_TREE_OPEN_BUTTON = (By.XPATH, "//div[@class='menu-open-button ng-star-inserted']")
    LOCATOR_TREE_CONTEXT_CREATE_BUTTON = (By.XPATH, "//div[@class='submenu-icon' and contains(text(), 'Создать')]")
    LOCATOR_TREE_CONTEXT_CREATE_INDICATOR_BUTTON = (By.XPATH, "//div[@class='context-menu-item-title']//div[text()=' Показатель ']")
    LOCATOR_TREE_CONTEXT_CREATE_OBJECT_BUTTON = (By.XPATH, "//div[@class='context-menu-item-title']//div[text()=' Объект ']")
    LOCATOR_TREE_CONTEXT_CREATE_DATASET_BUTTON = (By.XPATH, "//div[@class='context-menu-item-title']//div[text()=' Набор данных ']")
    LOCATOR_TREE_CONTEXT_CREATE_TABLE_BUTTON = (By.XPATH, "//div[@class='context-menu-item-title']//div[text()=' Таблица данных ']")


    def __init__(self, driver, login, password, token=None):
        BasePage.__init__(self, driver)
        ApiClasses.__init__(self, login, password, token=token)
        ApiModels.__init__(self, login, password, token=token)

    def create_folder_in_root(self, folder_name):
        self.find_and_context_click(self.LOCATOR_ROOT_FOLDER)
        self.find_and_click(self.LOCATOR_CREATE_FOLDER_BUTTON)
        Modals.enter_and_save(self, folder_name)

    def create_root_class(self, class_name):
        self.find_and_context_click(self.LOCATOR_ROOT_FOLDER)
        self.find_and_click(self.LOCATOR_CREATE_CLASS_BUTTON)
        Modals.enter_and_save(self, class_name)

    def create_class_in_folder(self, folder_name, class_name):
        folder_locator = (By.XPATH, f"//span[text()='{folder_name}']//..//..//..//div[@class='tree-item-title']")
        self.find_and_context_click(folder_locator)
        self.find_and_click(self.LOCATOR_CREATE_CLASS_BUTTON)
        Modals.enter_and_save(self, class_name)

    def create_model_in_folder(self, folder_name, model_name):
        folder_locator = (By.XPATH, f"//span[text()='{folder_name}']//..//..//..//div[@class='tree-item-title']")
        self.find_and_context_click(folder_locator)
        self.find_and_click(self.LOCATOR_CREATE_MODEL_BUTTON)
        Modals.enter_and_save(self, model_name)
        time.sleep(Vars.PKM_USER_WAIT_TIME)

    def get_root_elements(self):
        names = []
        elements = self.driver.find_elements(By.XPATH, "//div[@class='tree-item-children ng-star-inserted']//div["
                                                       "@class='tree-item']//div[@class='item-name']//span")
        for object_name in elements:
            names.append(object_name.text)
        return names

    def find_tree_node(self, node_name):
        node = (By.XPATH, f"(//div[@class='tree-item-children ng-star-inserted']//div[@class='tree-item']//div[@class='item-name']//span)[text()='{node_name}']")
        self.find_element(node)

    def switch_to_classes_tree(self):
        try:
            self.find_and_click(self.LOCATOR_TREE_ARROW)
        except TimeoutException:
            self.open_tree()
            self.find_and_click(self.LOCATOR_TREE_ARROW)
        self.find_and_click(self.LOCATOR_TREE_CLASS_BUTTON)
        tree_value = self.get_element_text(self.LOCATOR_TREE_TYPE_BLOCK)
        assert tree_value == 'Классы', 'Неправильное название в переключателе типа дерева'

    def switch_to_models_tree(self):
        try:
            self.find_and_click(self.LOCATOR_TREE_ARROW)
        except TimeoutException:
            self.open_tree()
            self.find_and_click(self.LOCATOR_TREE_ARROW)
        self.find_and_click(self.LOCATOR_TREE_MODEL_BUTTON)
        tree_value = self.get_element_text(self.LOCATOR_TREE_TYPE_BLOCK)
        assert tree_value == 'Модели', 'Неправильное название в переключателе типа дерева'

    def check_node_in_tree(self, node_name, active=True, last=True):
        nodes = self.get_root_elements()
        assert nodes.count(node_name) == 1, f'В корне дерева созданно несколько нод с именем "{node_name}"'
        if last:
            last_tree_element_name = self.get_element_text(self.LOCATOR_LAST_TREE_ELEMENT)
            assert last_tree_element_name == node_name, f'Созданная нода "{node_name}" не последняя в дереве'
        if active:
            active_node_title = self.get_element_text(self.LOCATOR_TREE_ACTIVE_NODE)
            assert active_node_title == node_name, 'Созданная нода не активная в дереве'

    def check_test_folder(self, folder_name, tree_type='classes'):
        if tree_type == 'classes':
            if folder_name not in self.get_root_elements():
                assert not ApiClasses.folder_name_is_exists(self, folder_name)
                self.create_folder_in_root(folder_name)
                self.find_tree_node(folder_name)
        elif tree_type == 'models':
            if folder_name not in self.get_root_elements():
                assert not ApiModels.folder_name_is_exists(self, folder_name)
                self.create_folder_in_root(folder_name)
                self.find_tree_node(folder_name)

    def check_indicator_in_tree(self, ind_name, class_name, active=True):
        locator = (By.XPATH, f"//span[text()='{class_name}']//..//../following-sibling::div[contains(@class, 'tree-item-children')]//span[text()='{ind_name}']")
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(locator))
        if active:
            active_node_title = self.get_element_text(self.LOCATOR_TREE_ACTIVE_NODE)
            assert active_node_title == ind_name, 'Созданная нода не активная в дереве'

    def check_child_node_absense(self, parent_node_name, child_node_name):
        element = (By.XPATH, f"//span[text()='{parent_node_name}']//..//../following-sibling::div[contains(@class, 'tree-item-children')]//span[text()='{child_node_name}']")
        try:
            self.find_element(element, time=0.5)
        except TimeoutException:
            return True
        assert self.is_element_disappearing(element, time=5, wait_display=False), f'элемент "{child_node_name}" не исчез из ноды "{parent_node_name}" в дереве'

    def get_node_childrens(self, node_name):
        list_elements = []
        elements = self.driver.find_elements(By.XPATH, f"//span[text()='{node_name}']//..//../following-sibling::div[contains("
                                                       "@class, 'tree-item-children')]//span")
        for element in elements:
            list_elements.append(element.text)
        return list_elements

    def delete_node(self, node_name):
        element = (By.XPATH, f"(//div[@class='tree-item-children ng-star-inserted']//div[@class='tree-item' ]//span)["
                             f"text()='{node_name}']")
        self.find_and_context_click(element)
        self.find_and_click(self.LOCATOR_DELETE_CLASS_BUTTON)
        self.check_node_absence(node_name)

    def check_node_absence(self, node_name):
        element = (By.XPATH, f"(//div[@class='tree-item-children ng-star-inserted']//div[@class='tree-item' ]//span)["
                             f"text()='{node_name}']")
        try:
            self.driver.find_element(element)
        except InvalidArgumentException:
            return True
        self.is_element_disappearing(element)

    def open_tree(self):
        try:
            return self.find_and_click(self.LOCATOR_TREE_OPEN_BUTTON, time=5)
        except TimeoutException:
            pass

    def open_node(self, node_name):
        node_locator = (By.XPATH, f"//span[text()='{node_name}']//..//..//..//div[contains(@class, 'tree-item-title')]")
        self.find_and_click(node_locator)
        self.wait_until_text_in_element(self.LOCATOR_PAGE_TITLE_BLOCK, node_name.upper())

    def expand_node(self, node_name):

        el = (By.XPATH, f"//span[text()='{node_name}']//..//..//..//div[contains(@class, 'item-arrow')]//fa-icon[contains(@ng-reflect-icon, 'angle-right')]")
        try:
            # фикс для обновления дерева:
            self.find_and_click(self.LOCATOR_TREE_TARGET_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(el))
            self.find_and_click(el)
        except TimeoutException:
            pass
        try:
            self.find_and_click(el, time=1)
        except TimeoutException:
            pass

    def create_indicator(self, class_name, ind_name):
        class_icon_locator = (By.XPATH, f"//span[text()='{class_name}']//..//..//div[@class='item-icon']")
        self.find_and_context_click(class_icon_locator)
        self.hover_over_element(self.LOCATOR_TREE_CONTEXT_CREATE_BUTTON)
        self.find_and_click(self.LOCATOR_TREE_CONTEXT_CREATE_INDICATOR_BUTTON)
        Modals.enter_and_save(self, ind_name)
        # фикс для обновления дерева:
        self.find_and_click(self.LOCATOR_TREE_TARGET_BUTTON)

    def create_model_object(self, model_name, class_name, object_name):
        model_icon_locator = (By.XPATH, f"//span[text()='{model_name}']//..//..//div[@class='item-icon']")
        self.find_and_context_click(model_icon_locator)
        self.hover_over_element(self.LOCATOR_TREE_CONTEXT_CREATE_BUTTON)
        self.find_and_click(self.LOCATOR_TREE_CONTEXT_CREATE_OBJECT_BUTTON)
        Modals.object_enter_and_save(self, object_name, class_name)
        time.sleep(Vars.PKM_API_WAIT_TIME)
        self.expand_node(model_name)
        assert self.find_element((By.XPATH, f"//span[text()='{model_name}']//..//../following-sibling::div[contains(@class, 'tree-item-children')]//span[text()='{object_name}']")), f'Объект "{object_name}" не отображается в дереве в модели "{model_name}"'

    def create_model_dataset(self, model_name, dataset_name):
        model_icon_locator = (By.XPATH, f"//span[text()='{model_name}']//..//..//div[@class='item-icon']")
        self.find_and_context_click(model_icon_locator)
        time.sleep(Vars.PKM_USER_WAIT_TIME)
        self.hover_over_element(self.LOCATOR_TREE_CONTEXT_CREATE_BUTTON)
        time.sleep(Vars.PKM_USER_WAIT_TIME)
        self.find_and_click(self.LOCATOR_TREE_CONTEXT_CREATE_DATASET_BUTTON)
        Modals.enter_and_save(self, dataset_name)

    def create_model_table(self, model_name, table_name):
        model_icon_locator = (By.XPATH, f"//span[text()='{model_name}']//..//..//div[@class='item-icon']")
        self.find_and_context_click(model_icon_locator)
        self.hover_over_element(self.LOCATOR_TREE_CONTEXT_CREATE_BUTTON)
        self.find_and_click(self.LOCATOR_TREE_CONTEXT_CREATE_TABLE_BUTTON)
        Modals.enter_and_save(self, table_name)
        time.sleep(Vars.PKM_API_WAIT_TIME)

    @staticmethod
    def check_nodes_order(prev_order, node_name, new_order):
        assert new_order == prev_order.remove(node_name), 'Порядок нод изменился неправильно после удаления'
