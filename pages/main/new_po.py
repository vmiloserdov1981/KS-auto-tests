from core import BasePage
from selenium.webdriver.common.by import By
from pages.login_po import LoginPage


class NewPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.sidebar = NavigationSidebar(driver)
        self.modal = NewModal(driver)
        self.header = Header(driver)

    def wait_main_page(self, timeout=10):
        self.find_element(self.sidebar.LOCATOR_SIDEBAR, time=timeout)


class NavigationSidebar(BasePage):
    LOCATOR_SIDEBAR = (By.XPATH, "//ks-sidebar[.//div[contains(@class, 'sidebar__logo')]]")
    USER_SEARCH_FIELD = (By.XPATH, "//ks-filter-input/div/input")

    def select_page(self, page_name):
        page_locator = (By.XPATH, f"//div[contains(@class, 'sidebar__nav-item') and .//span[.='{page_name}']]")
        if 'selected' not in self.find_element(page_locator).get_attribute('class'):
            self.find_and_click(page_locator)

    def search_user(self, User):
        self.find_and_click(self.USER_SEARCH_FIELD)
        self.find_element(self.USER_SEARCH_FIELD).send_keys(User)

class Header(BasePage):
    LOCATOR_USER_INFO_BLOCK = (By.XPATH, "(//div[contains(@class, 'header__user-info')])[1]")
    LOCATOR_EXIT_BUTTON = (By.XPATH, "//div[contains(@class, 'menu-item') and .=' Выйти ']")

    def logout(self):
        self.find_and_click(self.LOCATOR_USER_INFO_BLOCK)
        self.find_and_click(self.LOCATOR_EXIT_BUTTON)
        self.find_element(LoginPage.LOCATOR_PKM_LOGIN_TITLE)



class NewModal(BasePage):
    LOCATOR_ACCEPT_BUTTON = (By.XPATH, "//ks-button[.=' Принять ']")

    def accept_modal(self):
        self.find_and_click(self.LOCATOR_ACCEPT_BUTTON)

