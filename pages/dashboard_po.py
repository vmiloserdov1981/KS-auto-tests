from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from core import antistale
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
import time


class DashboardPage(EntityPage):
    LOCATOR_DASHBOARD_SETTINGS_BUTTON = (By.XPATH, "//ks-button[.//*[local-name()='svg' and @data-icon='cog']]")
    LOCATOR_DASHBOARD_ADD_INPUT_EVENT_BUTTON = (By.XPATH, "//pkm-dashboard-settings-group[.//div[.='Входящие события']]//fa-icon[.//*[local-name()='svg' and @data-icon='plus']]")
    LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON = (By.XPATH, "//pkm-dashboard-side-panel//button[.=' Сохранить ' or .='Сохранить']")
    LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR = (By.XPATH, "//pkm-dashboard-settings-group[.//div[.='Связанная сущность']]")

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

    def set_single_input_event_dropdown(self, dropdown_name, dropdown_value):
        dropdown_locator = (By.XPATH, f"//div[contains(@class, 'form-col') and .//div[.='{dropdown_name}']]//ks-dropdown")
        option_locator = (By.XPATH, f"//div[@class='single-dropdown-item' and .=' {dropdown_value} ']")
        self.find_and_click(dropdown_locator)
        self.find_and_click(option_locator)

    def set_multiple_input_event_dropdown(self, dropdown_name, dropdown_values):
        dropdown_locator = (By.XPATH, f"//div[@class='form-col' and .//div[.='{dropdown_name}']]//ks-dropdown")
        self.find_and_click(dropdown_locator)
        for dropdown_value in dropdown_values:
            option_locator = (By.XPATH, f"//div[@class='multiple-dropdown-item' and .=' {dropdown_value} ']")
            self.find_and_click(option_locator)
        self.find_and_click(dropdown_locator)

    def set_menu_dashboard(self, menu_diagram_name):
        self.find_and_click(self.LOCATOR_DASHBOARD_SETTINGS_BUTTON)
        self.find_and_click(self.LOCATOR_DASHBOARD_ADD_INPUT_EVENT_BUTTON)
        self.set_single_input_event_dropdown('Тип события', 'Получение интерфейса')
        self.set_single_input_event_dropdown('Действие', 'Получить')
        self.set_multiple_input_event_dropdown('Источник', ['Ячейка 0'])
        self.find_and_click(self.modal.LOCATOR_SAVE_BUTTON)
        self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)
        self.find_and_click((By.XPATH, "//pkm-dashboard-cell"))
        self.find_and_click(self.LOCATOR_DASHBOARD_RELATED_ENTITY_DROPDOWN_LOCATOR)
        self.set_single_input_event_dropdown('Тип сущности', 'Диаграмма')
        self.find_and_enter((By.XPATH, "//async-dropdown-search//input[@placeholder='Диаграмма']"), menu_diagram_name)
        self.find_and_click(self.dropdown_value_locator_creator(menu_diagram_name))
        self.find_and_click(self.LOCATOR_SAVE_DASHBOARD_SETTINGS_BUTTON)



