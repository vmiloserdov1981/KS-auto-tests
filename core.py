from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
import json
from variables import PkmVars as Vars
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class BasePage:
    LOCATOR_PAGE_TITLE_BLOCK = (By.XPATH, "//div[@class='page-title-container']//div[@class='title-value']")
    LOCATOR_TITLE_INPUT = (By.XPATH, "(//div[@class='page-title-container']//input)[1]")
    LOCATOR_TITLE_CHECK_ICON = (By.XPATH, "//div[@class='page-title-container']//fa-icon[@icon='check']")

    def __init__(self, driver, url=None):
        self.driver = driver
        self.base_url = url

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def wait_element_disappearing(self, locator, time=10, wait_display=True):
        if wait_display:
            try:
                element = self.find_element(locator)
            except TimeoutException:
                raise AssertionError('Элемент не появился на странице')
            try:
                WebDriverWait(self.driver, time).until(ec.staleness_of(element),
                                                       message=f'Элемент "{locator}" не исчезает')
            except TimeoutException:
                return False
            return True
        elif not wait_display:
            try:
                element = self.find_element(locator, time=1)
            except TimeoutException:
                return True
            try:
                WebDriverWait(self.driver, time).until(ec.staleness_of(element),
                                                       message=f'Элемент "{locator}" не исчезает')
            except TimeoutException:
                return False
            return True

    def get_element_text(self, locator, time=5):
        element = self.find_element(locator)
        if element.text == '':
            WebDriverWait(self.driver, time).until((lambda text_present: self.find_element(locator).text.strip() != ''),
                                                message=f"Empty element {locator}")
        return element.text

    def wait_until_text_in_element(self, locator, text, time=15):
        return WebDriverWait(self.driver, time).until(ec.text_to_be_present_in_element(locator, text),
                                               message=f"No '{text}' text in element '{locator}'")

    def wait_until_text_in_element_value(self, locator, text, time=5):
        WebDriverWait(self.driver, time).until(ec.text_to_be_present_in_element_value(locator, text),
                                               message=f"No '{text}' text in element_value '{locator}'")

    def find_element_clickable(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.element_to_be_clickable(locator),
                                                      message=f"Can't find element by locator {locator}")

    def show_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.visibility_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_and_click(self, locator, time=5):
        element = self.find_element_clickable(locator, time)
        return element.click()

    def find_and_click_by_offset(self, locator, x=0, y=0):
        elem = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(elem).move_by_offset(x, y).click().perform()

    def find_and_context_click(self, locator, time=5):
        element = self.find_element_clickable(locator, time)
        action_chains = ActionChains(self.driver)
        return action_chains.context_click(element).perform()

    def find_and_enter(self, locator, text, time=5):
        element = self.find_element(locator, time)
        element.send_keys(text)
        return element

    def hover_over_element(self, locator):
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    def get_local_token(self):
        token = self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", 'token')
        if token != 'undefined':
            return token
        else:
            return None

    def get_uuid_from_url(self):
        url = self.driver.current_url
        url = url.split(Vars.PKM_MAIN_URL)[1]
        uuid = url.split('/')[-1].split("?")[0]
        return uuid

    def rename_title(self, title_name):
        action = ActionChains(self.driver)
        self.find_and_click(self.LOCATOR_PAGE_TITLE_BLOCK)
        title_input = self.find_element(self.LOCATOR_TITLE_INPUT)
        action.double_click(title_input).perform()
        title_input.send_keys(Keys.DELETE)
        title_input.send_keys(title_name)
        self.find_and_click(self.LOCATOR_TITLE_CHECK_ICON)
        actual_title_name = (self.get_element_text(self.LOCATOR_PAGE_TITLE_BLOCK))
        assert actual_title_name == title_name.upper()

    def rename_field(self, locator, field_name):
        action = ActionChains(self.driver)
        input_field = self.find_element(locator)
        action.double_click(input_field).perform()
        input_field.send_keys(Keys.DELETE)
        self.find_and_enter(locator, field_name)

    def drag_and_drop(self, element_1, element_2):
        action = ActionChains(self.driver)
        action.drag_and_drop(element_1, element_2).perform()


class BaseApi:
    def __init__(self, login, password, token=None):
        self.login = login
        self.password = password
        if token is None:
            self.token = self.api_get_token(self.login, self.password, Vars.PKM_API_URL)
        else:
            self.token = token

    @staticmethod
    def api_get_token(login, password, host):
        payload = {'login': "{}".format(login), 'password': "{}".format(password)}
        r = requests.post('{}auth/login'.format(host), data=json.dumps(payload))
        result = json.loads(r.text)
        token = result.get('token')
        return token

    @staticmethod
    def post(url, token, payload):
        headers = {'Content-Type': 'application/json', 'Authorization': str("Bearer " + token)}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return json.loads(response.text)
