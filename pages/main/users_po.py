import time

from pages.main.new_po import NewPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class UsersPage(NewPage):
    LOCATOR_USERS_PAGE = (By.XPATH, "//ks-users")
    LOCATOR_PAGINATION_NEXT_PAGE_BUTTON = (By.XPATH, "(//ks-pagination//li[.//*[local-name()='svg' and contains(@data-icon, 'chevron-right')]])[not (contains(@class, 'disabled'))]")

    def __init__(self, driver):
        super().__init__(driver),
        self.profile_page = UserProfilePage(driver)

    def switch_to_page(self):
        self.sidebar.select_page('Пользователи')
        self.wait_element_stable(self.LOCATOR_USERS_PAGE, 3)


    def select_user(self, login: str):
        self.sidebar.search_user()
        target_locator = (By.XPATH, f"//tr[(.//td[2])[.='{login}']]")
        target_row = self.find_element(target_locator, time=4)
        time.sleep(1)
        target_row.click()
'''
    def select_user(self, login: str):
         target_locator = (By.XPATH, f"//tr[(.//td[2])[.='{login}']]")
         target_row = None
         while not target_row:
             try:
                 target_row = self.find_element(target_locator, time=3)
             except TimeoutException:
                 self.find_and_click(self.LOCATOR_PAGINATION_NEXT_PAGE_BUTTON)
         target_row.click()
'''

class UserProfilePage(NewPage):
    LOCATOR_EDIT_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'edit-password')]")
    LOCATOR_GENERATE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'generate-password')]")
    LOCATOR_SHOW_PASSWORD_BUTTON = (By.XPATH, "//fa-icon[contains(@class, 'eye-password-icon')]")
    LOCATOR_PASSWORD_FIELD = (By.XPATH, "//ks-input[@type='password']//input[@placeholder='Создайте пароль']")
    LOCATOR_CHANGE_PASSWORD_BUTTON = (By.XPATH, "//ks-button[.=' Изменить пароль ']")
    LOCATOR_EDIT_USER_PROFILE_BUTTON = (By.XPATH, "//div[contains(@class,'user-details-form')]//button[.='Редактировать']")

    def change_password(self, new_password: str = None):
        try:
            self.find_and_click(self.LOCATOR_EDIT_PASSWORD_BUTTON)
        except TimeoutException:
            self.find_and_click(self.LOCATOR_EDIT_USER_PROFILE_BUTTON)
            self.find_and_click(self.LOCATOR_EDIT_PASSWORD_BUTTON)
        if new_password:
            pass
        else:
            self.find_and_click(self.LOCATOR_GENERATE_PASSWORD_BUTTON)
            self.find_and_click(self.LOCATOR_SHOW_PASSWORD_BUTTON)
            time.sleep(3)
            actual_password = self.get_input_value(self.LOCATOR_PASSWORD_FIELD)
            assert actual_password
            self.find_and_click(self.LOCATOR_CHANGE_PASSWORD_BUTTON)
            self.modal.accept_modal()
            self.is_element_disappearing(self.LOCATOR_CHANGE_PASSWORD_BUTTON, wait_display=False)
            return actual_password


