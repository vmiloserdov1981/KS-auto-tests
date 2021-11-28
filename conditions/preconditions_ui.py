from core import BasePage
from pages.login_po import LoginPage
from variables import PkmVars as Vars
from pages.admin_po import AdminPage
from pages.main.projects_po import ProjectsPage
import allure
from selenium.webdriver.common.by import By
from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from api.api import ApiEu
from pages.components.trees import Tree
from pages.components.modals import ProjectModal
from pages.main.new_po import NewPage
from pages.components.modals import ChangePasswordModal
from core import TimeoutException


class PreconditionsFront(BasePage, ApiEu):

    ADMIN_PUBLICATION_NAME = 'Администрирование'
    EU_PUBLICATION_NAME = 'Приразломная'

    def __init__(self, driver, project_uuid, login=None, password=None, token=None):
        BasePage.__init__(self, driver)
        ApiEu.__init__(self, login, password, project_uuid, token=token)

    def change_expired_password(self, password, timeout=5):
        change_modal = ChangePasswordModal(self.driver)
        try:
            self.find_element(change_modal.LOCATOR_CHANGE_PASS_BUTTON, time=timeout)
        except TimeoutException:
            return False
        self.find_and_click(change_modal.LOCATOR_CHANGE_PASS_BUTTON)
        change_modal.change_password(password, password)
        return True

    @allure.title('Перейти к интерфейсу администратора')
    def login_as_admin(self, login, password, project, publication=Vars.PKM_ADMIN_PUBLICATION_NAME):
        login_page = LoginPage(self.driver, url=Vars.PKM_MAIN_URL)
        admin_page = AdminPage(self.driver)
        projects_page = ProjectsPage(self.driver)
        main_page = NewPage(self.driver)
        with allure.step('Перейти на сайт по адресу {}'.format(Vars.PKM_MAIN_URL)):
            login_page.go_to_site()
        with allure.step('Включиить логирование истории запросов'):
            self.driver.execute_script("window.requestHistoryEnabled = true")
        with allure.step('Войти в систему'):
            login_page.login(login, password)
        if publication:
            with allure.step('Перейти на вкладку "Проекты"'):
                projects_page.switch_to_page()
            with allure.step(f'Перейти к публикации {publication}'):
                projects_page.switch_to_publication(project, publication)
            with allure.step('Подождать отображение интерфейса администратора'):
                admin_page.wait_admin_page()
        else:
            with allure.step('Подождать отображение главной страницы'):
                main_page.wait_main_page()

        with allure.step('Сохранить токен приложения в драйвере'):
            self.driver.token = self.api_get_token(login, password, Vars.PKM_API_URL)

    @allure.title('Перейти к интерфейсу конечного пользователя')
    def login_as_eu(self, login, password, project):
        login_page = LoginPage(self.driver, url=Vars.PKM_MAIN_URL)
        plan_registry = PlanRegistry(self.driver)
        projects_page = ProjectsPage(self.driver)
        with allure.step('Перейти на сайт по адресу {}'.format(Vars.PKM_MAIN_URL)):
            login_page.go_to_site()
        with allure.step('Войти в систему'):
            login_page.login(login, password)
        with allure.step('Перейти на вкладку "Проекты"'):
            projects_page.switch_to_page()
        with allure.step(f'Перейти к публикации {self.EU_PUBLICATION_NAME}'):
            projects_page.switch_to_publication(project, self.EU_PUBLICATION_NAME)
        with allure.step(f'Закрыть модальое окно необходимости выбора плана при его отображении'):
            plan_registry.close_modal()
        with allure.step('Проверить наличие иконки меню'):
            plan_registry.find_element((By.XPATH, "//fa-icon[@icon='bars']"), time=10)
        with allure.step('Сохранить токен приложения в драйвере'):
            # self.driver.token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')
            self.driver.token = self.api_get_token(login, password, Vars.PKM_API_URL)

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
