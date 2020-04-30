from core import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class Modals(BasePage):
    LOCATOR_NAME_INPUT = (By.XPATH, "//input[@placeholder='Введите имя']")
    LOCATOR_CLASS_INPUT = (By.XPATH, "//input[@placeholder='Выберите класс']")
    LOCATOR_SAVE_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Сохранить ']")
    LOCATOR_CREATE_BUTTON = (By.XPATH, "//div[@class='modal-window-footer']//button[text()=' Создать ']")
    LOCATOR_ERROR_NOTIFICATION = (By.XPATH, "//div[contains(@class,'notification-type-error') and text()='Ошибка сервера']")
    LOCATOR_MODAL_TITLE = (By.XPATH, "//div[@class='modal-window-title']//div[@class='title-text']")

    def enter_and_save(self, name):
        self.find_and_enter(self.LOCATOR_NAME_INPUT, name)
        self.find_and_click(self.LOCATOR_SAVE_BUTTON)

    def object_enter_and_save(self, object_name, class_name):
        self.find_and_enter(self.LOCATOR_NAME_INPUT, object_name)
        self.find_and_enter(self.LOCATOR_CLASS_INPUT, class_name)
        self.find_and_click((By.XPATH, f"//div[@class='overlay']//div[contains(@class, 'dropdown-item') and text()=' {class_name} ']"))
        self.find_and_click(self.LOCATOR_CREATE_BUTTON)

    def check_error_displaying(self, wait_disappear=False):
        assert self.find_element(self.LOCATOR_ERROR_NOTIFICATION), 'Окно с ошибкой не отображается'
        if wait_disappear:
            assert self.wait_element_disappearing(self.LOCATOR_ERROR_NOTIFICATION), "Окно с ошибкой не исчезает"

    def get_title(self):
        title = self.get_element_text(self.LOCATOR_MODAL_TITLE)
        return title

    def fill_name(self, field_name, text):
        action = ActionChains(self.driver)
        field_locator = (By.XPATH, f"//label[@for='title' and text()='{field_name}']//following-sibling::input[@id='title']")
        field = self.find_element(field_locator)
        if field.get_attribute('value') != '':
            action.double_click(field).perform()
            field.send_keys(Keys.DELETE)
        else:
            pass
        field.send_keys(text)

    def fill_field(self, field_name, text):
        action = ActionChains(self.driver)
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//following-sibling::input")
        field = self.find_element(field_locator)
        if field.get_attribute('value') != '':
            action.double_click(field).perform()
            field.send_keys(Keys.DELETE)
        else:
            pass
        field.send_keys(text)

    def set_field(self, field_name, option):
        field_locator = (By.XPATH, f"//div[contains(@class, 'indicator-label') and text()=' {field_name} ']//..//div[contains(@class, 'dropdown')]")
        value_locator = (By.XPATH, f"//div[@class='content' and text()=' {option} ']")
        self.find_and_click(field_locator)
        self.find_and_click(value_locator)

    def check_option(self, option_name):
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'checkbox-label ') and text()=' {option_name} ']//preceding-sibling::div")
        checkbox = self.find_element(checkbox_locator)
        if 'checkbox-selected' in checkbox.get_attribute('class'):
            pass
        else:
            self.find_and_click(checkbox_locator)

    def uncheck_option(self, option_name):
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'checkbox-label ') and text()=' {option_name} ']//preceding-sibling::div")
        checkbox = self.find_element(checkbox_locator)
        if 'checkbox-selected' in checkbox.get_attribute('class'):
            self.find_and_click(checkbox_locator)
        else:
            pass



