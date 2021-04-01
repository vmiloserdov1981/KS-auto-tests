from selenium.webdriver.common.by import By
from core import BasePage
import users
from variables import PkmVars as Vars
from pages.components.modals import ProjectModal
import allure
import time
from random import randint


class LoginPage(BasePage):
    LOCATOR_PKM_LOGIN_FIELD = (By.XPATH, "//ks-input[@formcontrolname='login']//input")
    LOCATOR_PKM_PASS_FIELD = (By.XPATH, "//ks-input[@formcontrolname='password']//input")
    LOCATOR_PKM_LOGIN_EU_BUTTON = (By.XPATH, "//ks-button[@ng-reflect-title='Вход']")
    LOCATOR_PKM_LOGIN_TITLE = (By.XPATH, "//h1[.='Knowledge Space']")

    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.project_modal = ProjectModal(driver)

    def go_to_site(self):
        self.driver.get(self.base_url)

    def enter_login(self, login):
        login_input = self.find_element(self.LOCATOR_PKM_LOGIN_FIELD)
        if login_input.get_attribute('value') is not None:
            login_input.clear()
        return self.find_and_enter(self.LOCATOR_PKM_LOGIN_FIELD, login)

    def enter_pass(self, password):
        pass_input = self.find_element(self.LOCATOR_PKM_PASS_FIELD)
        if pass_input.get_attribute('value') is not None:
            pass_input.clear()
        return self.find_and_enter(self.LOCATOR_PKM_PASS_FIELD, password)

    def login_as_admin(self):
        with allure.step('Кликнуть на кнопку входа'):
            # добавлена рандомная задержка для предотвращения одновременного логина при выполнении тестов параллельно
            time.sleep(randint(2, 11))
            self.find_and_click(self.LOCATOR_PKM_LOGIN_EU_BUTTON)
        with allure.step('Проверить наличие иконки меню'):
            time.sleep(5)
            # self.find_element((By.XPATH, "//fa-icon[@icon='bars']"), time=10)
        with allure.step('Перейти в интерфейс администратора'):
            self.driver.get(f"{Vars.PKM_MAIN_URL}#/main")

    def login_as_eu(self):
        # добавлена рандомная задержка для предотвращения одновременного логина при выполнении тестов параллельно
        time.sleep(randint(2, 11))
        self.find_and_click(self.LOCATOR_PKM_LOGIN_EU_BUTTON)

    def check_page(self):
        login_title = self.get_element_text(self.LOCATOR_PKM_LOGIN_TITLE, time=20)
        assert login_title == 'Авторизация', 'неверный тайтл страницы'
        assert self.base_url in self.driver.current_url, 'Неверный url страницы'

    def eu_login(self, login, project_name=Vars.PKM_PROJECT_NAME):
        login = users.test_users.get(login).login
        password = users.test_users.get(login).password
        self.enter_login(login)
        self.enter_pass(password)
        self.login_as_eu()
        if self.project_modal.is_project_modal_displaying():
            self.project_modal.select_project(project_name, remember_choice=True)
