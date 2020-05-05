from core import BasePage
from pages.components.eu_header import EuHeader
from selenium.webdriver.common.by import By


class PlanRegistry(EuHeader, BasePage):
    LOCATOR_VIEW_PLAN_BUTTON = (By.XPATH, "//button[contains(@class, 'user-button') and text()=' Посмотреть ']")

    def watch_plan_by_comment(self, comment):
        target = (By.XPATH, f"(//tr[contains(@class, 'plan-row')]//td)[last() and text()='{comment}']")
        self.find_and_click(target)
        self.find_and_click(self.LOCATOR_VIEW_PLAN_BUTTON)
        self.wait_until_text_in_element(self.LOCATOR_EU_PAGE_TITLE, 'ПЛАН МЕРОПРИЯТИЙ (ГЛАВНАЯ)')

