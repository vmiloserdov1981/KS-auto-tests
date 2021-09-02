from selenium.webdriver.common.by import By
from core import BasePage
from pages.components.modals import ProjectModal
import allure
import time
from random import randint


class LoginPage(BasePage):
    LOCATOR_PKM_LOGIN_FIELD = (By.XPATH, "//ks-input[@formcontrolname='login']//input")
    LOCATOR_PKM_PASS_FIELD = (By.XPATH, "//ks-input[@formcontrolname='password']//input")
    LOCATOR_PKM_LOGIN_EU_BUTTON = (By.XPATH, "//ks-button[.='Войти']")
    LOCATOR_PKM_LOGIN_TITLE = (By.XPATH, "//ks-login")

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

    def check_page(self):
        login_title = self.get_element_text(self.LOCATOR_PKM_LOGIN_TITLE, time=20)
        assert login_title == 'Авторизация', 'неверный тайтл страницы'
        assert self.base_url in self.driver.current_url, 'Неверный url страницы'

    def login(self, login, password, wait_main_page=True, check_password_expiration=True):
        self.enter_login(login)
        self.enter_pass(password)
        # добавлена рандомная задержка для предотвращения одновременного логина при выполнении тестов параллельно
        time.sleep(randint(2, 5))
        with allure.step(f'Клик на кнопку логина'):
            self.find_and_click(self.LOCATOR_PKM_LOGIN_EU_BUTTON)
        if check_password_expiration:
            from conditions.preconditions_ui import PreconditionsFront
            change_password_modal = PreconditionsFront(self.driver, None)
            is_pass_changed = change_password_modal.change_expired_password(password)
            if is_pass_changed:
                self.enter_login(login)
                self.enter_pass(password)
                # добавлена рандомная задержка для предотвращения одновременного логина при выполнении тестов параллельно
                time.sleep(randint(2, 5))
                with allure.step(f'Клик на кнопку логина'):
                    self.find_and_click(self.LOCATOR_PKM_LOGIN_EU_BUTTON)

        if wait_main_page:
            with allure.step('Проверить переход на главную страницу'):
                self.find_element((By.XPATH, "//ks-home"))
