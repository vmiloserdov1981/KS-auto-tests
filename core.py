from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
import json
from variables import PkmVars as Vars
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from datetime import datetime
from datetime import date
from datetime import timedelta
from time import sleep
import collections
import os


class BasePage:
    LOCATOR_DROPDOWN_VALUE = (By.XPATH, "//pkm-dropdown-item")

    def __init__(self, driver, url=None):
        self.driver = driver
        self.base_url = url
        from api.api import ApiCreator
        self.api_creator = ApiCreator(None, None, driver.project_uuid, token=driver.token)

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def wait_dom_changing(self, time=10):
        dom = self.driver.execute_script('return document.body')
        return WebDriverWait(self.driver, time).until(DomChanged(dom),
                                                      message=f"DOM hasn`t been changed")

    def wait_element_replacing(self, element, locator, time=10, ignore_timeout=False):
        if ignore_timeout:
            try:
                WebDriverWait(self.driver, time).until(ElementReplaced(element, locator),
                                                       message=f"Element hasn`t been replaced")
            except TimeoutException:
                pass
        else:
            return WebDriverWait(self.driver, time).until(ElementReplaced(element, locator),
                                                          message=f"Element hasn`t been replaced")

    def wait_element_changing(self, html, locator, time=10, ignore_timeout=False):
        if ignore_timeout:
            try:
                WebDriverWait(self.driver, time).until(ElementChanged(html, locator), message=f"Element hasn`t been changed")
            except TimeoutException:
                return
        else:
            WebDriverWait(self.driver, time).until(ElementChanged(html, locator), message=f"Element hasn`t been changed")

    def is_element_disappearing(self, locator, time=10, wait_display=True):
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

    def get_element_text(self, locator, time=5, ignore_error=False):
        if ignore_error:
            try:
                element = self.find_element(locator, time=time)
            except TimeoutException:
                return
        else:
            element = self.find_element(locator, time=time)
        if element.text == '':
            WebDriverWait(self.driver, time).until((lambda text_present: self.find_element(locator).text.strip() != ''),
                                                   message=f"Empty element {locator}")
        return element.text

    def wait_until_text_in_element(self, locator, text, time=10):
        return WebDriverWait(self.driver, time).until(ec.text_to_be_present_in_element(locator, text),
                                                      message=f"No '{text}' text in element '{locator}'")

    def wait_until_text_in_element_value(self, locator, text, time=5):
        WebDriverWait(self.driver, time).until(ec.text_to_be_present_in_element_value(locator, text),
                                               message=f"No '{text}' text in element_value '{locator}'")

    def find_element_clickable(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.element_to_be_clickable(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_element_disabled(self, locator, time=10):
        return WebDriverWait(self.driver, time).until_not(ec.element_to_be_clickable(locator),
                                                          message=f"Can't find element by locator {locator}")

    def show_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.visibility_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def scroll_to_element(self, webelement):
        self.driver.execute_script("arguments[0].scrollIntoView(alignToTop=false);", webelement)

    def find_and_click(self, locator, time=5, scroll_to_element=True):
        element = self.find_element(locator, time=time)
        if scroll_to_element:
            self.scroll_to_element(element)
        element.click()

    def find_and_click_by_offset(self, locator, x=0, y=0):
        elem = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(elem).move_by_offset(x, y).click().perform()

    def find_and_context_click(self, locator, time=5):
        element = self.find_element(locator, time)
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

    def rename_field(self, locator, field_name):
        action = ActionChains(self.driver)
        input_field = self.find_element(locator)
        action.double_click(input_field).perform()
        input_field.send_keys(Keys.DELETE)
        self.find_and_enter(locator, field_name)

    def drag_and_drop(self, element_1, element_2):
        action = ActionChains(self.driver)
        action.drag_and_drop(element_1, element_2).perform()

    def get_input_value(self, input_locator, return_empty=True, webelement=None, time=2):
        if not webelement:
            input_element = self.find_element(input_locator, time=time)
        else:
            input_element = webelement
        value = input_element.get_attribute('value')
        if return_empty:
            return value
        else:
            return value if value != '' else None

    @staticmethod
    def compare_lists(list_a: list, list_b: list):
        return collections.Counter(list_a) == collections.Counter(list_b)

    def compare_dicts(self, dict_a, dict_b):
        assert self.compare_lists(dict_a.keys(), dict_b.keys())
        for key in dict_a:
            if type(dict_a.get(key)) is list:
                assert self.compare_lists(dict_a.get(key), dict_b.get(key))
            elif type(dict_a.get(key)) is dict:
                self.compare_dicts(dict_a.get(key), dict_b.get(key))
            else:
                assert dict_a.get(key) == dict_b.get(key), f'{dict_a} не равно f{dict_b}'

    @staticmethod
    def compare_dicts_static(dict_a, dict_b):
        if not BasePage.compare_lists(dict_a.keys(), dict_b.keys()):
            return False
        for key in dict_a:
            if type(dict_a.get(key)) is list:
                if not BasePage.compare_lists(dict_a.get(key), dict_b.get(key)):
                    return False
            elif type(dict_a.get(key)) is dict:
                if not BasePage.compare_dicts_static(dict_a.get(key), dict_b.get(key)):
                    return False
            else:
                if dict_a.get(key) != dict_b.get(key):
                    return False
        return True

    @staticmethod
    def add_in_group(item, dictionary, group_value):
        if ' . ' in group_value:
            group_values = group_value.split(' . ')
            for value in group_values:
                if value in dictionary.keys():
                    dictionary[value].append(item)
                else:
                    dictionary[value] = [item]
        else:
            if group_value in dictionary.keys():
                dictionary[group_value].append(item)
            else:
                dictionary[group_value] = [item]
        return dictionary

    def elements_generator(self, locator, time=5, wait=None):
        if wait:
            sleep(wait)
        try:
            self.find_element(locator, time=time)
        except TimeoutException:
            return None
        elements = self.driver.find_elements(*locator)
        for element in elements:
            yield element

    def is_element_clickable(self, locator):
        try:
            WebDriverWait(self.driver, 1).until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            return False
        return True

    def get_dropdown_values(self, dropdown_locator, time=5):
        self.find_and_click(dropdown_locator, time=time)
        values = [value.text for value in self.elements_generator(self.LOCATOR_DROPDOWN_VALUE, time=time)]
        self.find_and_click(dropdown_locator)
        return values

    def is_input_checked(self, input_locator: tuple):
        input = self.find_element(input_locator)
        is_checked = self.driver.execute_script("return arguments[0].checked;", input)
        return is_checked


class DomChanged(object):
    def __init__(self, dom):
        self.dom = dom

    def __call__(self, driver):
        new_dom = driver.execute_script("return document.documentElement.outerHTML")
        if self.dom != new_dom:
            return True
        else:
            return False


class ElementReplaced(object):
    def __init__(self, element, locator):
        self.element = element
        self.locator = locator

    def __call__(self, driver):
        new_element = driver.find_element(*self.locator)
        if self.element != new_element:
            return True
        else:
            return False


class ElementChanged(object):
    def __init__(self, html, locator):
        self.html = html
        self.locator = locator

    def __call__(self, driver):
        old_html = self.html
        new_html = driver.find_element(*self.locator).get_attribute('innerHTML')
        if old_html != new_html:
            return True
        else:
            return False


class BaseApi:
    def __init__(self, login, password, project_uuid, token=None, api_url=Vars.PKM_API_URL):
        self.login = login
        self.password = password
        self.project_uuid = project_uuid
        if token is None and login and password:
            self.token = self.api_get_token(self.login, self.password, api_url)
        else:
            self.token = token

    @staticmethod
    def api_get_token(login, password, host):
        payload = {'login': "{}".format(login), 'password': "{}".format(password)}
        response = requests.post('{}auth/login'.format(host), data=json.dumps(payload))
        if response.status_code in range(200, 300):
            result = json.loads(response.text)
            token = result.get('token')
            return token
        else:
            raise AssertionError(f'Ошибка при получении ответа сервера: {response.status_code}, {response.text}')

    def post(self, url, token, payload, without_project=False):
        project_uuid = self.project_uuid
        if not project_uuid:
            project_uuid = os.getenv('PROJECT_UUID')
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = str("Bearer " + token)
        if project_uuid and not without_project:
            headers['x-project-uuid'] = project_uuid
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code in range(200, 300):
            return json.loads(response.text)
        else:
            raise AssertionError(f'Ошибка при получении ответа сервера:\n запрос: {url} \n payload: {payload} \n headers: {headers} \n Ответ: {response.status_code}, {response.text}')

    @staticmethod
    def get(url, params=None):
        if params is None:
            params = {}
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, params=json.dumps(params), headers=headers)
        return json.loads(response.text)

    @staticmethod
    def get_utc_date():
        raw_date = datetime.utcnow()
        date_value = str(raw_date).split(' ')[0].split('-')[::-1]
        return date_value

    @staticmethod
    def get_utc_time():
        raw_date = datetime.utcnow()
        time_value = str(raw_date).split(' ')[1].split(':')
        value = f'{time_value[0]}:{time_value[1]}'
        return value

    @staticmethod
    def get_feature_date(start, offset):
        raw_date = list(map(int, start[::-1]))
        start_date = date(*raw_date)
        day = timedelta(days=1)
        end_date = start_date + day * offset
        day = end_date.day
        month = end_date.month
        year = end_date.year
        if day < 10:
            day = f'0{day}'
        else:
            day = str(day)
        if month < 10:
            month = f'0{month}'
        else:
            month = str(month)
        year = str(year)
        feature_date = [day, month, year]
        return feature_date

    @staticmethod
    def get_feature_month(start: list, offset: int):
        '''
        start = ['01', '2012']
        '''
        start_month = int(start[0])
        start_year = int(start[1])
        end_month = start_month + offset
        if end_month > 12:
            year_add = end_month // 12
            month_add = (end_month % 12) - 1
            start_month += month_add
            start_year += year_add
        else:
            start_month += offset - 1

        if start_month < 10:
            start_month = f'0{start_month}'
        else:
            start_month = str(start_month)

        start_year = str(start_year)

        result = [start_month, start_year]
        return result

    @staticmethod
    def get_mounth_name_by_number(mounth_number: str):
        mounth = {
            '01': 'Январь',
            '02': 'Февраль',
            '03': 'Март',
            '04': 'Апрель',
            '05': 'Май',
            '06': 'Июнь',
            '07': 'Июль',
            '08': 'Август',
            '09': 'Сентябрь',
            '10': 'Октябрь',
            '11': 'Ноябрь',
            '12': 'Декабрь'
        }
        return mounth.get(mounth_number)

    def api_get_user_by_login(self, login):
        payload = {"login": login}
        response = self.post(f'{Vars.PKM_API_URL}users/get-user-by-login', self.token, payload)
        assert not response.get('error'), f'Ошибка при получении данных пользователя'
        return response.get('user')

    @staticmethod
    def anti_doublespacing(string):
        if string:
            if '  ' in string:
                string_list = string.split(' ')
                new_string_list = [elem for elem in string_list if elem != '']
                string = ' '.join(new_string_list)

            if string[0] == ' ':
                string = string[1:]

            if string[len(string) - 1] == ' ':
                string = string[:len(string) - 1]

            return string

    def get_project_uuid_by_name(self, project_name):
        payload = {"term": "", "limit": 0}
        projects = self.post(f'{Vars.PKM_API_URL}projects/get-list', self.token, payload).get('data')
        for project in projects:
            if project.get('name') == project_name:
                return project.get('uuid')

    @staticmethod
    def get_project_uuid_by_name_static(project_name, token):
        payload = {"term": "", "limit": 0}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': str("Bearer " + token)}
        r = requests.post(f'{Vars.PKM_API_URL}projects/get-list', data=json.dumps(payload), headers=headers)
        projects = json.loads(r.text).get('data')
        for project in projects:
            if project.get('name') == project_name:
                return project.get('uuid')

    @staticmethod
    def add_in_group(item, dictionary, group_value):
        if type(group_value) is str:
            if group_value in dictionary.keys():
                dictionary[group_value].append(item)
            else:
                dictionary[group_value] = [item]
        elif type(group_value) is list:
            for i in group_value:
                if i in dictionary.keys():
                    dictionary[i].append(item)
                else:
                    dictionary[i] = [item]
        return dictionary


def antistale(func):
    def wrap(*args, **kwargs):
        stale = True
        count = 0
        while stale:
            if count > 10:
                raise AssertionError('Превышено количество повторных перезапусков метода')
            try:
                return func(*args, **kwargs)
            except StaleElementReferenceException:
                stale = True
                count += 1
    return wrap
