from core import BasePage
from pages.login_po import LoginPage
from variables import PkmVars as Vars
from pages.main_po import MainPage
import allure
from selenium.webdriver.common.by import By
from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from api.api import ApiEu
from pages.components.trees import Tree
from pages.components.modals import ProjectModal, PublicationsModal


class PreconditionsFront(BasePage, ApiEu):

    def __init__(self, driver, project_uuid, login=None, password=None, token=None):
        BasePage.__init__(self, driver)
        ApiEu.__init__(self, login, password, project_uuid, token=token)

    @allure.title('Перейти к интерфейсу администратора')
    def login_as_admin(self, login, password, project):
        login_page = LoginPage(self.driver, url=Vars.PKM_MAIN_URL)
        main_page = MainPage(self.driver)
        project_modal = ProjectModal(self.driver)
        with allure.step('Перейти на сайт по адресу {}'.format(Vars.PKM_MAIN_URL)):
            login_page.go_to_site()
        with allure.step('Ввести логин "{}"'.format(login)):
            login_page.enter_login(login)
        with allure.step('Ввести пароль "{}"'.format(password)):
            login_page.enter_pass(password)
        with allure.step('Войти в режим администратора'):
            login_page.login_as_admin()
        if project_modal.is_project_modal_displaying():
            with allure.step(f'Выбрать проект {project}'):
                project_modal.select_project(project)
        with allure.step('Проверить отображение блока профиля пользователя'):
            main_page.find_element(main_page.LOCATOR_PKM_PROFILENAME_BLOCK)
        with allure.step('Сохранить токен приложения в драйвере'):
            self.driver.token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')

    @allure.title('Перейти к интерфейсу конечного пользователя')
    def login_as_eu(self, login, password, project, publication=Vars.PKM_PUBLICATION_NAME):
        login_page = LoginPage(self.driver, url=Vars.PKM_MAIN_URL)
        main_page = MainPage(self.driver)
        project_modal = ProjectModal(self.driver)
        publication_modal = PublicationsModal(self.driver)
        plan_registry = PlanRegistry(self.driver)
        with allure.step('Перейти на сайт по адресу {}'.format(Vars.PKM_MAIN_URL)):
            login_page.go_to_site()
        with allure.step('Ввести логин "{}"'.format(login)):
            login_page.enter_login(login)
        with allure.step('Ввести пароль "{}"'.format(password)):
            login_page.enter_pass(password)
        with allure.step('Войти в режим конечного пользователя'):
            login_page.login_as_eu()
        if project_modal.is_project_modal_displaying():
            with allure.step(f'Выбрать проект {project}'):
                project_modal.select_project(project)
        if publication_modal.is_publications_bar_displaying():
            with allure.step(f'Выбрать представление {publication}'):
                publication_modal.select_publication(publication)
        plan_registry.close_modal()

        with allure.step('Проверить наличие иконки меню'):
            main_page.find_element((By.XPATH, "//fa-icon[@icon='bars']"), time=10)

        with allure.step('Сохранить токен приложения в драйвере'):
            self.driver.token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')

    @allure.title('Посмотреть последний созданный через k6 план мероприятий')
    def view_last_k6_plan(self):
        header = EuHeader(self.driver)
        k6_plan_comment = self.driver.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
        plan_registry_page = PlanRegistry(self.driver)

        with allure.step('Закрыть модальное окно необходимости выбора плана при его появлении'):
            plan_registry_page.close_modal()

        with allure.step('Перейти на страницу "Реестр ИП"'):
            header.navigate_to_page('Реестр интегрированных планов')
        with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
            plan_registry_page.watch_plan_by_comment(k6_plan_comment)

    @allure.title('Посмотреть копию последнего созданного через k6 плана мероприятий')
    def view_last_k6_plan_copy(self):
        header = EuHeader(self.driver)
        k6_plan_comment = self.driver.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
        plans_registry = PlanRegistry(self.driver)
        k6_plan = self.driver.test_data.get('last_k6_plan')
        k6_plan_uuid = k6_plan.get('uuid')
        k6_plan_name = k6_plan.get('name')
        with allure.step(f'Проверить наличие плана - копии ИП "{k6_plan_name}"'):
            self.driver.test_data['copy_last_k6_plan'] = self.check_k6_plan_copy(k6_plan_comment, k6_plan_uuid)
            if self.driver.test_data['copy_last_k6_plan'].get('is_new_created'):
                self.driver.refresh()

        with allure.step('Закрыть модальное окно необходимости выбора плана при его появлении'):
            plans_registry.close_modal()

        with allure.step('Перейти на страницу "Реестр ИП"'):
            header.navigate_to_page('Реестр интегрированных планов')

        with allure.step(f'Посмотреть на диаграмме Ганта план - копию ИП "{k6_plan_name}"'):
            plans_registry.watch_plan_by_comment(
                self.driver.test_data['copy_last_k6_plan'].get('settings').get('plan').get('comment'))

    @allure.title('Выбрать тип дерева')
    def set_tree(self, tree_type):
        tree = Tree(self.driver)
        with allure.step(f'Выбрать тип дерева "{tree_type}"'):
            tree.switch_to_tree(tree_type)

    @allure.title('Выбрать проект')
    def set_project(self, project_name):
        project_modal = ProjectModal(self.driver)
        if project_modal.is_project_modal_displaying():
            with allure.step(f'Выбрать проект "{project_name}"'):
                project_modal.select_project(project_name, remember_choice=True)
