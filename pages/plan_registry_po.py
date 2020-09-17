from core import BasePage
from core import antistale
from pages.components.eu_header import EuHeader
from selenium.webdriver.common.by import By
from api.api import ApiEu
from selenium.common.exceptions import TimeoutException
import time


class PlanRegistry(EuHeader, BasePage):
    LOCATOR_VIEW_PLAN_BUTTON = (By.XPATH, "//button[contains(@class, 'user-button') and text()=' Посмотреть ']")
    LOCATOR_SELECTED_PLAN_ROW = (By.XPATH, "//div[@class='plans-table-container']//fa-icon[@icon='star']/../..")
    LOCATOR_STAR = (By.XPATH, "//div[@class='plans-table-container']//fa-icon[@icon='star']")
    LOCATOR_VERSIONS_NAMES = (By.XPATH, "//div[contains(@class, 'version-element')]/div[2]")
    LOCATOR_VERSIONS_ROWS = (By.XPATH, "//div[contains(@class, 'version-element')]")
    LOCATOR_PLAN_CONTROL_BUTTONS = (By.XPATH, "//div[contains(@class, 'version-buttons')]/pkm-button")
    LOCATOR_ADD_VERSION_BUTTON = (By.XPATH, "//div[contains(@class, 'version-buttons')]/pkm-button[@ng-reflect-tooltip='Добавить']")
    LOCATOR_ADD_BASED_VERSION_BUTTON = (By.XPATH, "//div[contains(@class, 'version-buttons')]/pkm-button[@ng-reflect-tooltip='Создать на основе']")
    LOCATOR_DELETE_VERSION_BUTTON = (By.XPATH, "//div[contains(@class, 'version-buttons')]/pkm-button[@ng-reflect-tooltip='Удалить']")
    LOCATOR_SELECT_VERSION_BUTTON = (By.XPATH, "//div[contains(@class, 'version-buttons')]/pkm-button[@ng-reflect-tooltip='Выбрать']")
    LOCATOR_DEFAULT_VERSION_ROW = (By.XPATH, "//div[@class='versions']//fa-icon[@ng-reflect-icon='star']/../..")

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def watch_plan_by_comment(self, comment):
        target = (By.XPATH, f"(//tr[contains(@class, 'plan-row')]//td)[last() and text()='{comment}']")
        self.find_and_click(target)
        self.find_and_click(self.LOCATOR_VIEW_PLAN_BUTTON)
        self.wait_until_text_in_element(self.LOCATOR_EU_PAGE_TITLE, 'ПЛАН МЕРОПРИЯТИЙ (ГЛАВНАЯ)')

    def get_selected_plan(self):
        selected_row = self.find_element(self.LOCATOR_SELECTED_PLAN_ROW)
        plan_uuid = selected_row.get_attribute('test-plan-uuid')
        assert plan_uuid is not None, 'Невозможно получить uuid выбранного плана'
        plan = self.api_creator.get_api_eu().api.api_get_plan_by_uuid(plan_uuid)
        return plan

    def check_selected_plan(self):
        selected_plan_name = self.get_selected_plan().get('name')
        dropdown_value = self.get_plan_dropdown_placeholder()
        assert selected_plan_name == dropdown_value, 'Название плана в дропдауне планов не совпадает с выбранным планом'

    def select_plan_by_uuid(self, uuid):
        target = (By.XPATH, f"//tr[contains(@class, 'plan-row') and @test-plan-uuid='{uuid}']")
        self.find_and_click(target)

    def check_plan_versions(self, k6_plan_copy_uuid, expected_ui_versions=None):
        api = self.api_creator.get_api_eu()
        ui_versions = self.get_versions_names(with_dates=False)
        api_versions = [version.get('name') for version in api.plan_versions_generator(k6_plan_copy_uuid)]
        assert self.compare_lists(ui_versions, api_versions), f'версии в UI и API не совпадают, api = {api_versions}, ui = {ui_versions}'
        if expected_ui_versions:
            assert self.compare_lists(ui_versions, expected_ui_versions), f'Список версий не соответствует ожидаемому, actual_ui = {ui_versions}, expected_ui = {expected_ui_versions} '

    def cut_version_date(self, version):
        version = version.split(' ')
        version = version[:len(version) - 1]
        version = ' '.join(version)
        return version

    @antistale
    def get_versions_names(self, with_dates=True):
        element = self.find_element(self.LOCATOR_VERSIONS_NAMES)
        try:
            self.wait_element_replacing(element, self.LOCATOR_VERSIONS_NAMES, time=3)
        except TimeoutException:
            pass
        if with_dates:
            names = [ApiEu.anti_doublespacing(name.text) for name in self.elements_generator(self.LOCATOR_VERSIONS_NAMES)]
        else:
            names = [self.cut_version_date(name.text) for name in self.elements_generator(self.LOCATOR_VERSIONS_NAMES)]
        return names

    def get_selected_version(self):
        for row in self.elements_generator(self.LOCATOR_VERSIONS_ROWS):
            if 'selected-version' in row.get_attribute('class'):
                version = row.text.split('\n')[0]
                return version

    def get_control_buttons(self, enabled_only=False, disabled_only=False):
        buttons = []
        for button in self.elements_generator(self.LOCATOR_PLAN_CONTROL_BUTTONS):
            if enabled_only:
                if not button.get_attribute('ng-reflect-disabled'):
                    buttons.append(button.get_attribute('tooltip'))
            elif disabled_only:
                if button.get_attribute('ng-reflect-disabled') == 'true':
                    buttons.append(button.get_attribute('tooltip'))
        return buttons

    def select_version(self, name, with_dates=False):
        for version in self.elements_generator(self.LOCATOR_VERSIONS_NAMES):
            if not with_dates:
                if self.cut_version_date(version.text) == name:
                    return version.click()
            else:
                if version.text == name:
                    return version.click()

    def add_version(self, plan_uuid, based_on=None):
        expected_versions = self.get_versions_names(with_dates=True)
        api = self.api_creator.get_api_eu()
        last_number = api.get_last_plan_version_number(plan_uuid)
        last_number += 1
        today = api.get_utc_date()
        expected_name = f'Проект плана №{last_number} ({".".join(today)})'
        expected_versions.append(expected_name)
        if based_on:
            self.select_version(based_on, with_dates=False)
            self.find_and_click(self.LOCATOR_ADD_BASED_VERSION_BUTTON)
        else:
            self.find_and_click(self.LOCATOR_ADD_VERSION_BUTTON)
        actual_versions = self.get_versions_names(with_dates=True)
        assert self.compare_lists(expected_versions, actual_versions), 'Добавленная версия отображается некорректно'
        return (expected_name, api.get_plan_version_uuid_by_name(plan_uuid, self.cut_version_date(expected_name)))

    def get_version_state(self, name):
        for row in self.elements_generator(self.LOCATOR_VERSIONS_ROWS):
            if row.text.split('\n')[0] == name:
                return row.text.split('\n')[1]

    def get_default_version(self):
        row = self.find_element(self.LOCATOR_DEFAULT_VERSION_ROW)
        name = row.text.split('\n')[0]
        return name

    def delete_version(self, name):
        self.select_version(name, with_dates=True)
        self.find_and_click(self.LOCATOR_DELETE_VERSION_BUTTON)
        row_locator = (By.XPATH, f"//div[text()=' {name} ']/..")
        self.is_element_disappearing(row_locator)

    def set_default_version(self, name, with_dates=True):
        self.select_version(name, with_dates=with_dates)
        self.find_and_click(self.LOCATOR_SELECT_VERSION_BUTTON)
        time.sleep(5)
        actual_default_version = self.get_default_version()
        assert actual_default_version == name






