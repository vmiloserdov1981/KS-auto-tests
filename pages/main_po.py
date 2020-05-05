from core import BasePage
from selenium.webdriver.common.by import By
from variables import PkmVars as Vars


class MainPage(BasePage):
    LOCATOR_PKM_PROFILENAME_BLOCK = (By.XPATH, "//div[@class='profile-name']")

    def check_url(self, driver):
        assert self.base_url is not None, 'Для главной страницы не указан url'
        target_url = '{0}?treeType={1}'.format(self.base_url, Vars.PKM_DEFAULT_TREE_TYPE)
        assert driver.current_url == target_url, 'Неверный url страницы'

    def go_to_default_page(self):
        assert self.base_url is not None, 'Для главной страницы не указан url'
        self.driver.get(f'{self.base_url}?treeType={Vars.PKM_DEFAULT_TREE_TYPE}')
        self.find_element(self.LOCATOR_PKM_PROFILENAME_BLOCK)
