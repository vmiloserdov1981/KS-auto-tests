from core import BasePage
from pages.login_po import LoginPage
from variables import PkmVars as Vars
from pages.main_po import MainPage
import allure
from selenium.webdriver.common.by import By
from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry


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
            main_page.find_element((By.XPATH, "//fa-icon[@icon='bars']"), time=20)
            self.driver.token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')

    @allure.title('Посмотреть последний созданный через k6 план мероприятий')
    def view_last_k6_plan(self):
        header = EuHeader(self.driver)
        k6_plan_comment = self.driver.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
        plan_registry_page = PlanRegistry(self.driver)
        with allure.step('Перейти на страницу "Реестр ИП"'):
            header.navigate_to_page('Реестр интегрированных планов')
        with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
            plan_registry_page.watch_plan_by_comment(k6_plan_comment)
