from core import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.projects_page = ProjectsPage(driver)

    def wait_main_page(self, timeout=10):
        self.find_element(NavigationSidebar.LOCATOR_SIDEBAR, time=timeout)

    def switch_to_publication(self, project_name, publication_name):
        self.projects_page.switch_to_page()
        self.projects_page.select_project(project_name)
        self.projects_page.switch_to_publication(publication_name)


class ProjectsPage(BasePage):
    LOCATOR_PROJECTS_PAGE = (By.XPATH, "//ks-projects")
    LOCATOR_PROJECT_NAME_INPUT = (By.XPATH, "//div[contains(@class,'project-details__row') and ./div[.='Название проекта']]//input")

    def __init__(self, driver):
        super().__init__(driver)
        self.sidebar = NavigationSidebar(driver)

    def switch_to_page(self):
        self.sidebar.select_page('Проекты')
        self.wait_element_stable(self.LOCATOR_PROJECTS_PAGE, 3)

    def select_project(self, project_name):
        project_locator = (By.XPATH, f"//div[@routerlink='project-details' and .//div[@class='project__info-name' and .=' {project_name} ']]")
        self.find_and_click(project_locator)
        self.wait_until_text_in_element_value(self.LOCATOR_PROJECT_NAME_INPUT, project_name)

    def switch_to_publication(self, publication_name):
        pub_locator = (By.XPATH, f"//div[contains(@class, 'publication-view__name-container') and .//span[.='{publication_name}']]")
        self.find_and_click(pub_locator)


class NavigationSidebar(BasePage):
    LOCATOR_SIDEBAR = (By.XPATH, "//ks-sidebar[.//div[contains(@class, 'sidebar__logo')]]")

    def select_page(self, page_name):
        page_locator = (By.XPATH, f"//div[contains(@class, 'sidebar__nav-item') and .//span[.='{page_name}']]")
        if 'selected' not in self.find_element(page_locator).get_attribute('class'):
            self.find_and_click(page_locator)
