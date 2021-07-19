from pages.main.new_po import NewPage
from selenium.webdriver.common.by import By
from core import retry


class ProjectsPage(NewPage):
    LOCATOR_PROJECTS_PAGE = (By.XPATH, "//ks-projects")
    LOCATOR_PROJECT_NAME_INPUT = (By.XPATH, "//div[contains(@class,'project-details__row') and ./div[.='Название проекта']]//input")

    @retry
    def switch_to_publication(self, project_name, publication_name):
        self.select_project(project_name)
        self.select_publication(publication_name)

    def switch_to_page(self):
        self.sidebar.select_page('Проекты')
        self.wait_element_stable(self.LOCATOR_PROJECTS_PAGE, 3)

    def select_project(self, project_name):
        project_locator = (By.XPATH, f"//div[@routerlink='project-details' and .//div[@class='project__info-name' and .=' {project_name} ']]")
        self.find_and_click(project_locator)
        self.wait_until_text_in_element_value(self.LOCATOR_PROJECT_NAME_INPUT, project_name)

    def select_publication(self, publication_name):
        pub_locator = (By.XPATH, f"//div[contains(@class, 'publication-view__name-container') and .//span[.='{publication_name}']]")
        self.find_and_click(pub_locator)