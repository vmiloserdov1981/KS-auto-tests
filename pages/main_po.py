from core import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.projects_page = ProjectsPage(driver)
        self.users_page = UsersPage(driver)
        self.sidebar = NavigationSidebar(driver)

    def wait_main_page(self, timeout=10):
        self.find_element(NavigationSidebar.LOCATOR_SIDEBAR, time=timeout)

    def switch_to_publication(self, project_name, publication_name):
        self.switch_to_projects_page()
        self.projects_page.select_project(project_name)
        self.projects_page.switch_to_publication(publication_name)

    def switch_to_projects_page(self):
        self.sidebar.select_page('Проекты')
        self.wait_element_stable(self.projects_page.LOCATOR_PROJECTS_PAGE, 3)

    def switch_to_users_page(self):
        self.sidebar.select_page('Пользователи')
        self.wait_element_stable(self.users_page.LOCATOR_USERS_PAGE, 3)


class ProjectsPage(BasePage):
    LOCATOR_PROJECTS_PAGE = (By.XPATH, "//ks-projects")
    LOCATOR_PROJECT_NAME_INPUT = (By.XPATH, "//div[contains(@class,'project-details__row') and ./div[.='Название проекта']]//input")

    def select_project(self, project_name):
        project_locator = (By.XPATH, f"//div[@routerlink='project-details' and .//div[@class='project__info-name' and .=' {project_name} ']]")
        self.find_and_click(project_locator)
        self.wait_until_text_in_element_value(self.LOCATOR_PROJECT_NAME_INPUT, project_name)

    def switch_to_publication(self, publication_name):
        pub_locator = (By.XPATH, f"//div[contains(@class, 'publication-view__name-container') and .//span[.='{publication_name}']]")
        self.find_and_click(pub_locator)


class UsersPage(BasePage):
    LOCATOR_USERS_PAGE = (By.XPATH, "//ks-users")
    LOCATOR_PAGINATION_NEXT_PAGE_BUTTON = (By.XPATH, "(//ks-pagination//li[.//*[local-name()='svg' and contains(@data-icon, 'chevron-right')]])[not (contains(@class, 'disabled'))]")

    def __init__(self, driver):
        super().__init__(driver),
        self.profile_page = UserProfilePage(driver)

    def select_user(self, login: str):
        target_locator = (By.XPATH, f"//tr[(.//td[2])[.='{login}']]")
        target_row = None
        while not target_row:
            try:
                target_row = self.find_element(target_locator, time=5)
            except TimeoutException:
                self.find_and_click(self.LOCATOR_PAGINATION_NEXT_PAGE_BUTTON)
        target_row.click()


class UserProfilePage(BasePage):
    LOCATOR_EDIT_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'edit-password')]")
    LOCATOR_GENERATE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'generate-password')]")
    LOCATOR_SHOW_PASSWORD_BUTTON = (By.XPATH, "//fa-icon[contains(@class, 'eye-password-icon')]")
    LOCATOR_PASSWORD_FIELD = (By.XPATH, "//ks-input[@type='password']//input[@placeholder='Создайте пароль']")
    LOCATOR_CHANGE_PASSWORD_BUTTON = (By.XPATH, "//ks-button[.='Изменить пароль']")
    LOCATOR_ACCEPT_BUTTON = (By.XPATH, "//ks-button[.=' Принять ']")

    def change_password(self, new_password: str = None):
        self.find_and_click(self.LOCATOR_EDIT_PASSWORD_BUTTON)
        if new_password:
            pass
        else:
            self.find_and_click(self.LOCATOR_GENERATE_PASSWORD_BUTTON)
            self.find_and_click(self.LOCATOR_SHOW_PASSWORD_BUTTON)
            actual_password = self.get_input_value(self.LOCATOR_PASSWORD_FIELD)
            self.find_and_click(self.LOCATOR_CHANGE_PASSWORD_BUTTON)
            self.find_and_click(self.LOCATOR_ACCEPT_BUTTON)
            return actual_password






class NavigationSidebar(BasePage):
    LOCATOR_SIDEBAR = (By.XPATH, "//ks-sidebar[.//div[contains(@class, 'sidebar__logo')]]")

    def select_page(self, page_name):
        page_locator = (By.XPATH, f"//div[contains(@class, 'sidebar__nav-item') and .//span[.='{page_name}']]")
        if 'selected' not in self.find_element(page_locator).get_attribute('class'):
            self.find_and_click(page_locator)
