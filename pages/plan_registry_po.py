from core import BasePage
from api.api import ApiEu
from pages.components.eu_header import EuHeader
from selenium.webdriver.common.by import By


class PlanRegistry(EuHeader, ApiEu, BasePage):
    LOCATOR_VIEW_PLAN_BUTTON = (By.XPATH, "//button[contains(@class, 'user-button') and text()=' Посмотреть ']")
    LOCATOR_SELECTED_PLAN_ROW = (By.XPATH, "//div[@class='plans-table-container']//fa-icon[@icon='star']/../..")
    LOCATOR_STAR = (By.XPATH, "//div[@class='plans-table-container']//fa-icon[@icon='star']")

    def __init__(self, driver, login=None, password=None, token=None):
        BasePage.__init__(self, driver)
        ApiEu.__init__(self, login, password, token=token)

    def watch_plan_by_comment(self, comment):
        target = (By.XPATH, f"(//tr[contains(@class, 'plan-row')]//td)[last() and text()='{comment}']")
        self.find_and_click(target)
        self.find_and_click(self.LOCATOR_VIEW_PLAN_BUTTON)
        self.wait_until_text_in_element(self.LOCATOR_EU_PAGE_TITLE, 'ПЛАН МЕРОПРИЯТИЙ (ГЛАВНАЯ)')

    def get_selected_plan(self):
        selected_row = self.find_element(self.LOCATOR_SELECTED_PLAN_ROW)
        plan_uuid = selected_row.get_attribute('test-plan-uuid')
        assert plan_uuid is not None, 'Невозможно получить uuid выбранного плана'
        plan = self.api_get_plan_by_uuid(plan_uuid)
        return plan

    def check_selected_plan(self):
        selected_plan_name = self.get_selected_plan().get('name')
        dropdown_value = self.get_plan_dropdown_placeholder()
        assert selected_plan_name == dropdown_value, 'Название плана в дропдауне планов не совпадает с выбранным планом'


