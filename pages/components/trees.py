from core import BasePage, antistale, retry
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.components.modals import Modals
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
    LOCATOR_TREE_TYPE_BLOCK = (By.XPATH, "//div[contains(@class, 'admin-sidebar__item-selected')]//div[contains(@class, 'admin-sidebar__item__name')]")
    LOCATOR_TREE_ROOT_NODE = (By.XPATH, "(//div[@class='tree-item-title'])[1]")
    LOCATOR_SELECTED_NODE = (By.XPATH, "//div[contains(@class, 'tree-item-title') and contains(@class, 'selected')]")
    DICTIONARIES_TREE_NAME = 'Справочники'

    def __init__(self, driver):
        super().__init__(driver)
        self.modal = Modals(driver)

    @staticmethod
    def folder_locator_creator(folder_name):
        #locator = (By.XPATH, f"//div[@class='tree-item' and .='{folder_name}' and .//fa-icon[@ng-reflect-icon='folder']]")
        locator = (By.XPATH, f"//div[@class='tree-item' and .='{folder_name}']//*[local-name()='svg' and @data-icon='folder' ]")
        return locator

    @staticmethod
    def node_locator_creator(node_name):
        locator = (By.XPATH, f"//div[contains(@class, 'tree-item-title') and .='{node_name}']")
        return locator

    @staticmethod
    def node_arrow_locator_creator(node_name):
        node_xpath = Tree.node_locator_creator(node_name)[1]
        locator = (By.XPATH, node_xpath + "//preceding-sibling::div[contains(@class, 'item-arrow')]//fa-icon//*[local-name() = 'svg']")
        return locator

    @staticmethod
    def context_option_locator_creator(option_name):
        locator = (By.XPATH, f"//div[contains(@class, 'context-menu-body')]//div[@class='context-menu-item-title' and .=' {option_name} ']")
        return locator

    @staticmethod
    def submenu_option_locator_creator(option_name):
        locator = (By.XPATH, f"//div[contains(@class, 'context-menu-submenu')]//div[@class='context-menu-item' and .=' {option_name} ']")
        return locator

    @staticmethod
    def children_node_locator_creator(parent_node_name, children_node_name=None):
        if children_node_name:
            locator = (By.XPATH, f"//div[@class='tree-item' and ./div[contains(@class, 'tree-item-title') and .='{parent_node_name}']]//div[contains(@class, 'tree-item-children')] //div[contains(@class, 'tree-item-title') and .='{children_node_name}']")
        else:
            locator = (By.XPATH, f"//div[@class='tree-item' and ./div[contains(@class, 'tree-item-title') and .='{parent_node_name}']]//div[contains(@class, 'tree-item-children')] //div[contains(@class, 'tree-item-title')]")
        return locator

    def open_tree(self):
        try:
            return self.find_and_click(self.LOCATOR_TREE_OPEN_BUTTON, time=5)
        except TimeoutException:
            pass

    @retry
    def switch_to_tree(self, tree_name):
        tree_value = self.get_element_text(self.LOCATOR_TREE_TYPE_BLOCK)
        if tree_value != tree_name:
            tree_type_button_locator = (By.XPATH, f"(//div[contains(@class, 'admin-sidebar') and .=' {tree_name} '])[1]")
            self.find_and_click(tree_type_button_locator)
            self.wait_until_text_in_element(self.LOCATOR_TREE_TYPE_BLOCK, tree_name)

    def is_folder_exists(self, folder_name, time=5):
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
        self.find_and_context_click(self.LOCATOR_TREE_ROOT_NODE)
        self.find_and_click(self.context_option_locator_creator('Создать папку'))
        self.modal.enter_and_save(folder_name)

    def check_test_folder(self, folder_name):
        if not self.is_folder_exists(folder_name):
            self.create_root_folder(folder_name)

    def get_selected_node_name(self):
        try:
            node = self.get_element_text(self.LOCATOR_SELECTED_NODE)
            return node
        except TimeoutException:
            return

    def delete_node(self, node_name, node_type, parent_node_name=None):
        if parent_node_name:
            self.hide_node(node_name)
            children = self.get_node_children_names(parent_node_name)
            assert node_name in children, f'Нода для удаления не в родительской ноде "{parent_node_name}"'
        node_locator = self.node_locator_creator(node_name)
        self.context_selection(node_name, 'Удалить')
        actual_deletion_modal_text = self.modal.get_deletion_confirm_modal_text()
        expected_deletion_modal_text = f'Вы действительно хотите удалить\n{node_type} {node_name} ?'
        assert actual_deletion_modal_text == expected_deletion_modal_text, 'Некорректный текст подтверждения удаления ноды'
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        # time.sleep(3)
        assert self.is_element_disappearing(node_locator, wait_display=False), f'Нода "{node_name}" не исчезает при удалении'

    def rename_node(self, node_name, new_node_name):
        time.sleep(3)
        self.context_selection(node_name, 'Переименовать')
        self.modal.clear_name_input()
        self.modal.enter_and_save(new_node_name)

    def get_node_arrow(self, node_name, timeout=5):
        try:
            arrow = self.find_element(self.node_arrow_locator_creator(node_name), time=timeout)
        except TimeoutException:
            return
        return arrow

    @antistale
    def get_node_children_names(self, parent_node_name):
        arrow = self.get_node_arrow(parent_node_name)
        if not arrow:
            return []
        if arrow.get_attribute('data-icon') == 'angle-right':
            arrow.click()
        if arrow.get_attribute('data-icon') == 'angle-down':
            child_locator = self.children_node_locator_creator(parent_node_name)
            names = [node.text for node in self.elements_generator(child_locator, wait=3)]
            return names
        return

    def expand_node(self, node_name):
        arrow = self.get_node_arrow(node_name)
        if not arrow:
            return
        if arrow.get_attribute('data-icon') == 'angle-right':
            arrow.click()

    def hide_node(self, node_name):
        arrow = self.get_node_arrow(node_name)
        if not arrow:
            return
        if arrow.get_attribute('ng-reflect-icon') == 'angle-down':
            arrow.click()

    def select_node(self, node_name):
        node_locator = self.node_locator_creator(node_name)
        self. scroll_to_element(self.find_element(node_locator))
        self.find_and_click(self.node_locator_creator(node_name), time=20)
        self.wait_selected_node_name(node_name, timeout=20)
        page_title_locator = (By.XPATH, "//div[contains(@class, 'title-value')]")
        self.wait_until_text_in_element(page_title_locator, node_name.upper())

    def wait_selected_node_name(self, name, timeout=20):
        self.scroll_to_element(self.find_element(self.LOCATOR_SELECTED_NODE, time=timeout))
        self.wait_until_text_in_element(self.LOCATOR_SELECTED_NODE, name, time=timeout)

    def wait_child_node(self, parent_node_name: str, child_node_name: str, timeout=30) -> bool:
        locator = self.children_node_locator_creator(parent_node_name, child_node_name)
        try:
            self.find_element(locator, time=timeout)
            return True
        except TimeoutException:
            return False


class NewTree(BasePage):
    LOCATOR_TREE_ARROW = (By.CLASS_NAME, "arrow-wrapper")
    LOCATOR_TREE_OPEN_BUTTON = (By.XPATH, "//div[@class='menu-open-button ng-star-inserted']")
    LOCATOR_TREE_CLASS_BUTTON = (By.XPATH, "//div[contains(@class, 'dropdown-list app-scrollbar')]//div[text()=' Классы ']")
    LOCATOR_TREE_TYPE_BLOCK = (By.XPATH, "//div[contains(@class, 'admin-tree__title')]")
    LOCATOR_TREE_ADD_ROOT_ENTITY = (By.XPATH, "//div[contains(@class, 'create-container')]//button[//*[local-name()='svg' and @data-icon='plus']]")
    #LOCATOR_SELECTED_NODE = (By.XPATH, "//div[contains(@class, 'tree-item') and contains(@class, 'selected')]//div[contains(@class, 'tree-item-title')]")
    LOCATOR_SELECTED_NODE = (By.XPATH, "//div[contains(@class, 'tree-item') and contains(@class, 'selected')]")
    DICTIONARIES_TREE_NAME = 'Справочники'
    LOCATOR_TREE_NODE = (By.XPATH, "(//pkm-tree-item[.//div[contains(@class, tree-item)]])[not(.//div[contains(@class, 'load')])]")

    def __init__(self, driver):
        super().__init__(driver)
        self.modal = Modals(driver)

    @staticmethod
    def folder_locator_creator(folder_name):
        locator = (By.XPATH, f"//div[@class='tree-item' and .='{folder_name}']//*[local-name()='svg' and @data-icon='folder' ]")
        return locator

    @staticmethod
    def node_locator_creator(node_name):
        locator = (By.XPATH, f"(//div[contains(@class, 'tree-item-title') and .='{node_name}'])[last()]")
        return locator

    @staticmethod
    def node_arrow_locator_creator(node_name):
        node_xpath = NewTree.node_locator_creator(node_name)[1]
        locator = (By.XPATH, node_xpath + "//preceding-sibling::div[contains(@class, 'item-arrow')]//fa-icon//*[local-name() = 'svg']")
        return locator

    @staticmethod
    def context_option_locator_creator(option_name):
        locator = (By.XPATH, f"(//div[contains(@class, 'context-menu-body')]//div[contains(@class, 'context-menu-item') and .//div[contains(@class, 'context-menu-item-title') and .=' {option_name} ']])[last()]")
        return locator

    @staticmethod
    def submenu_option_locator_creator(option_name):
        locator = (By.XPATH, f"//div[contains(@class, 'context-menu-submenu')]//div[@class='context-menu-item' and .=' {option_name} ']")
        return locator

    @antistale
    def children_node_locator_creator(self, parent_node_name, children_node_name=None):
        parent_locator = (By.XPATH, f"(//div[@class='tree-item' and ./div[contains(@class, 'tree-item-title') and .='{parent_node_name}']])[last()]")
        parent_node = self.find_element(parent_locator)
        parent_uuid = parent_node.get_attribute('test-uuid')
        assert parent_uuid, 'Не удалось получить uuid родительской ноды'
        if children_node_name:
            locator = (By.XPATH, f"(//div[contains(@class, 'tree-item') and @test-parent-uuid='{parent_uuid}']//div[contains(@class, 'tree-item-title')])[.='{children_node_name}']")
        else:
            locator = (By.XPATH, f"//div[contains(@class, 'tree-item') and @test-parent-uuid='{parent_uuid}']//div[contains(@class, 'tree-item-title')]")
        return locator

    def switch_to_tree(self, tree_name):
        tree_value = self.get_element_text(self.LOCATOR_TREE_TYPE_BLOCK)
        if tree_value != tree_name:
            tree_type_button_locator = (By.XPATH, f"(//div[contains(@class, 'admin-sidebar') and .=' {tree_name} '])[1]")
            self.find_and_click(tree_type_button_locator)
            self.wait_until_text_in_element(self.LOCATOR_TREE_TYPE_BLOCK, tree_name)

    def is_folder_exists(self, folder_name, time=5):
        folder_locator = self.folder_locator_creator(folder_name)
        try:
            self.find_element(folder_locator, time=time)
            return True
        except TimeoutException:
            return False

    def context_selection(self, node_name, choice_name):
        node_locator = self.node_locator_creator(node_name)
        choice_locator = self.context_option_locator_creator(choice_name)
        self.find_and_context_click(node_locator, time=20)
        self.find_and_click(choice_locator)

    def create_root_folder(self, folder_name):
        create_button_locator = (By.XPATH, "//div[contains(@class, 'menu-list')]//div[.=' Создать папку ']")
        self.find_and_click(self.LOCATOR_TREE_ADD_ROOT_ENTITY)
        self.find_and_click(create_button_locator)
        self.modal.enter_and_save(folder_name)
        self.find_element(self.folder_locator_creator(folder_name))

    def check_test_folder(self, folder_name):
        if not self.is_folder_exists(folder_name):
            self.create_root_folder(folder_name)

    def get_selected_node_name(self):
        try:
            node = self.get_element_text(self.LOCATOR_SELECTED_NODE)
            return node
        except TimeoutException:
            return

    def delete_node(self, node_name, node_type, parent_node_name=None):
        """
        if parent_node_name:
            self.expand_node(parent_node_name)
            node_locator = self.children_node_locator_creator(parent_node_name, children_node_name=node_name)
        else:
        """
        node_locator = self.node_locator_creator(node_name)

        self.context_selection(node_name, 'Удалить')
        actual_deletion_modal_text = self.modal.get_deletion_confirm_modal_text()
        expected_deletion_modal_text = f'Вы действительно хотите удалить\n{node_type} {node_name} ?'
        assert actual_deletion_modal_text == expected_deletion_modal_text, 'Некорректный текст подтверждения удаления ноды'
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(node_locator, time=20, wait_display=False), f'Нода "{node_name}" не исчезает при удалении'

    def rename_node(self, node_name, new_node_name):
        time.sleep(3)
        self.context_selection(node_name, 'Переименовать')
        self.modal.clear_name_input()
        self.modal.enter_and_save(new_node_name)

    def get_node_arrow(self, node_name, timeout=5):
        try:
            arrow = self.find_element(self.node_arrow_locator_creator(node_name), time=timeout)
            self.scroll_to_element(arrow, to_top=True)
        except TimeoutException:
            return
        return arrow

    @antistale
    def get_node_children_names(self, parent_node_name):
        arrow = self.get_node_arrow(parent_node_name)
        if not arrow:
            return []
        if arrow.get_attribute('data-icon') == 'angle-right':
            arrow.click()
        if arrow.get_attribute('data-icon') == 'angle-down':
            names = [i.text for i in self.elements_generator(self.children_node_locator_creator(parent_node_name))]
            return names
        return []

    @antistale
    def expand_node(self, node_name):
        arrow = self.get_node_arrow(node_name)
        if not arrow:
            return
        if arrow.get_attribute('data-icon') == 'angle-right':
            arrow.click()

    def hide_node(self, node_name):
        arrow = self.get_node_arrow(node_name)
        if not arrow:
            return
        if arrow.get_attribute('ng-reflect-icon') == 'angle-down':
            arrow.click()

    def select_node(self, node_name):
        self.find_and_click(self.node_locator_creator(node_name), time=20)
        self.wait_until_text_in_element(self.LOCATOR_SELECTED_NODE, node_name)
        page_title_locator = (By.XPATH, "//div[contains(@class, 'title-value')]")
        self.wait_until_text_in_element(page_title_locator, node_name.upper())
        time.sleep(2)

    @antistale
    def wait_selected_node_name(self, name, timeout=15):
        self.scroll_to_element(self.find_element(self.LOCATOR_SELECTED_NODE))
        self.wait_until_text_in_element(self.LOCATOR_SELECTED_NODE, name, time=timeout)

    def wait_child_node(self, parent_node_name: str, child_node_name: str, timeout=30) -> bool:
        locator = self.children_node_locator_creator(parent_node_name, child_node_name)
        try:
            self.find_element(locator, time=timeout)
            return True
        except TimeoutException:
            return False
