from selenium.webdriver.common.by import By
from core import BasePage


class LoginPage(BasePage):
    LOCATOR_PKM_LOGIN_FIELD = (By.NAME, "login")
    LOCATOR_PKM_PASS_FIELD = (By.NAME, "password")
    LOCATOR_PKM_LOGIN_ADMIN_BUTTON = (By.XPATH, "//button [@class='user-button user-view-clear user-form-default "
                                                "user-size-s']")
    LOCATOR_PKM_LOGIN_TITLE = (By.XPATH, "//div[@class='login-container']//div[@class='login-title']")

    def go_to_site(self):
        self.driver.get(self.base_url)
        self.check_page()

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
        return self.find_and_click(self.LOCATOR_PKM_LOGIN_ADMIN_BUTTON)

    def check_page(self):
        login_title = self.get_element_text(self.LOCATOR_PKM_LOGIN_TITLE)
        assert login_title == 'Авторизация', 'неверный тайтл страницы'
        assert self.base_url in self.driver.current_url, 'Неверный url страницы'
