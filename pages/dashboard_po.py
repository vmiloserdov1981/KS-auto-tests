from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from core import antistale
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
import time


class DashboardPage(EntityPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    def wait_page_title(self, title, timeout=15):
        expected_title_locator = (By.XPATH, f"//div[contains(@class, 'header__title' ) and .=' {title} ']")
        try:
            self.find_element(expected_title_locator, time=timeout)
        except TimeoutException:
            raise AssertionError('Переход на страницу дашборда не осуществлен')

    def create_dashboard(self, parent_node, dashboard_name):
        with allure.step(f'Создать дашборд {dashboard_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать интерфейс'))
            self.tree.modal.enter_and_save(dashboard_name)
        with allure.step(f'Проверить отображение дашборда {dashboard_name} в дереве выбранным'):
            self.tree.wait_selected_node_name(dashboard_name)
        with allure.step(f'Проверить переход на страницу вновь соданного дашборда'):
            self.wait_page_title(dashboard_name)
