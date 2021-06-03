from core import BasePage
from selenium.webdriver.common.by import By
from variables import PkmVars as Vars
from pages.components.modals import ProjectModal


class AdminPage(BasePage):
    LOCATOR_PKM_PROFILENAME_BLOCK = (By.XPATH, "//div[contains(@class, 'header__user-info')]")
    LOCATOR_SELECT_PROJECT_BUTTON = (By.XPATH, "//div[@class='title-content']//div[.='Выбрать проект']")

    def __init__(self, driver):
        super().__init__(driver)
        self.project_modal = ProjectModal(driver)

    def wait_admin_page(self):
        self.find_element(self.LOCATOR_PKM_PROFILENAME_BLOCK)

    def check_url(self, driver):
        assert self.base_url is not None, 'Для главной страницы не указан url'
        target_url = '{0}?treeType={1}'.format(self.base_url, Vars.PKM_DEFAULT_TREE_TYPE)
        assert driver.current_url == target_url, 'Неверный url страницы'

    def go_to_default_page(self):
        assert self.base_url is not None, 'Для главной страницы не указан url'
        self.driver.get(f'{self.base_url}?treeType={Vars.PKM_DEFAULT_TREE_TYPE}')
        self.find_element(self.LOCATOR_PKM_PROFILENAME_BLOCK)

    def open_project_modal(self):
        self.find_and_click(self.LOCATOR_SELECT_PROJECT_BUTTON)
        self.find_element(self.project_modal.LOCATOR_SELECT_PROJECT_MODAL)

    def check_project(self, expected_project_name):
        self.open_project_modal()
        actual_project_name = self.project_modal.get_selected_project_name()
        if actual_project_name != expected_project_name:
            self.project_modal.select_project(expected_project_name)
        else:
            self.project_modal.close_project_modal()

