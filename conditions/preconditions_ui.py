from core import BasePage
from pages.login_po import LoginPage
from variables import PkmVars as Vars
from pages.main_po import MainPage
import allure
from selenium.webdriver.common.by import By


class PreconditionsFront(BasePage):
    @allure.title('Перейти к интерфейсу администратора')
    def login_as_admin(self, login, password):
        login_page = LoginPage(self.driver, url=Vars.PKM_MAIN_URL)
        main_page = MainPage(self.driver)
        with allure.step('Перейти на сайт по адресу {}'.format(Vars.PKM_MAIN_URL)):
            login_page.go_to_site()
        with allure.step('Ввести логин "{}"'.format(login)):
            login_page.enter_login(login)
        with allure.step('Ввести пароль "{}"'.format(password)):
            login_page.enter_pass(password)
        with allure.step('Войти в режим администратора'):
            login_page.login_as_admin()
            main_page.find_element(main_page.LOCATOR_PKM_PROFILENAME_BLOCK)
            self.driver.token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')

    @allure.title('Перейти к интерфейсу конечного пользователя')
    def login_as_eu(self, login, password):
        login_page = LoginPage(self.driver, url=Vars.PKM_MAIN_URL)
        main_page = MainPage(self.driver)
        with allure.step('Перейти на сайт по адресу {}'.format(Vars.PKM_MAIN_URL)):
            login_page.go_to_site()
        with allure.step('Ввести логин "{}"'.format(login)):
            login_page.enter_login(login)
        with allure.step('Ввести пароль "{}"'.format(password)):
            login_page.enter_pass(password)
        with allure.step('Войти в режим конечного пользователя'):
            login_page.login_as_eu()
            main_page.find_element((By.XPATH, "//fa-icon[@icon='bars']"))
            self.driver.token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')
