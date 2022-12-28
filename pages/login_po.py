from selenium.webdriver.common.by import By
from core import BasePage, Keys
from pages.components.modals import ProjectModal
import allure
import time
from random import randint


class LoginPage(BasePage):
    LOCATOR_PKM_LOGIN_FIELD = (By.XPATH, "//ks-input[@formcontrolname='login']//input")
    LOCATOR_PKM_PASS_FIELD = (By.XPATH, "//ks-input[@formcontrolname='password']//input")
    LOCATOR_PKM_LOGIN_EU_BUTTON = (By.XPATH, "//ks-button[.=' Войти ']")
    LOCATOR_PKM_LOGIN_TITLE = (By.XPATH, "//ks-login")
    REGISTRATION_BUTTON = (By.XPATH, "//pkm-app-root//*[text()='Регистрация']")
    FIRST_NAME_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите имя')]")
    LAST_NAME_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите фамилию')]")
    LOGIN_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите логин')]")
    EMAIL_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите e-mail')]")
    PASSWORD_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Придумайте пароль')]")
    PASSWORD_FIELD2 = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите пароль')]")
    PASSWORD_CONFIRM_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите пароль повторно')]")
    REGISTRATION_BUTTON_CONFIRM = (By.XPATH, "//pkm-app-root//*[text()='Зарегистрироваться']")

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

    def registering(self):
        self.find_and_click(self.REGISTRATION_BUTTON)

    def filling_regirstration_data_new_user(self, First_name, Last_name, Login, Email, Password_user):
        self.find_element(self.FIRST_NAME_FIELD).send_keys(First_name)
        self.find_element(self.LAST_NAME_FIELD).send_keys(Last_name)
        self.find_element(self.LOGIN_FIELD).send_keys(Login)
        self.find_element(self.EMAIL_FIELD).send_keys(Email)
        self.find_element(self.PASSWORD_FIELD).send_keys(Password_user)
        self.find_element(self.PASSWORD_CONFIRM_FIELD).send_keys(Password_user)
        time.sleep(2)
        self.find_and_click(self.REGISTRATION_BUTTON_CONFIRM)
        time.sleep(4)

    def registered_user_login(self, Login, Password_user):
        self.find_element(self.LOGIN_FIELD).send_keys(Login)
        self.find_element(self.PASSWORD_FIELD2).send_keys(Password_user)
        self.find_and_click(self.LOCATOR_PKM_LOGIN_EU_BUTTON)
        time.sleep(2)

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
