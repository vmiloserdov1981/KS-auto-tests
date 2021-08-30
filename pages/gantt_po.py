import time

from pages.components.entity_page import EntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from pages.events_plan_po import EventsPlan
from selenium.webdriver.common.by import By
import allure


class GanttPage(EntityPage):
    LOCATOR_CONSTRUCTOR_CLASS_INPUT = (By.XPATH, "//async-dropdown-search[@formcontrolname='classUuid']//input")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)
        self.events_plan_page = EventsPlan(driver)

    def create_gantt(self, model_name, gantt_name):
        with allure.step(f'Создать диаграмму Ганта {gantt_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(model_name), time=20)
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Диаграмма Ганта'))
        with allure.step(f'Укзать название диаграммы Ганта {gantt_name} и создать ее'):
            self.modal.enter_and_save(gantt_name)
        with allure.step(f'Проверить отображение диаграммы Ганта {gantt_name} в дереве выбранной'):
            self.tree.wait_selected_node_name(gantt_name)
        with allure.step(f'Проверить переход на страницу диаграммы Ганта'):
            self.wait_page_title(gantt_name.upper())

    def set_gantt_class(self, class_name: str):
        self.find_and_enter(self.LOCATOR_CONSTRUCTOR_CLASS_INPUT, class_name)
        item_locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .=' {class_name} ']")
        self.find_and_click(item_locator)
        actual_value = self.find_element(self.LOCATOR_CONSTRUCTOR_CLASS_INPUT).get_attribute('value')
        assert actual_value == class_name

    def set_gantt(self, gantt_data):
        """
                gantt_data = {
                "name": 'План мероприятий',
                "class": 'hi',
                "start_indicator": 'hi',
                "end_indicator": 'hi',
                "duration_indicator": 'hi',
                "anchor_indicator": 'hi',
                "additional_indicators": ['hi'],
                "relations": {
                    0: {
                        "name": "Персонал мероприятия",
                        "class": 'hi',
                        "search_indicators": [],
                        "input_indicators": ['hi']
                    },
                    1: {
                        "name": "МТР мероприятия",
                        "class": 'hi',
                        "search_indicators": ['hi'],
                        "input_indicators": ['hi']
                    }
                }
            }
        """
        class_name = gantt_data.get("class")
        start_indicator = gantt_data.get("start_indicator")
        end_indicator = gantt_data.get("end_indicator")
        duration_indicator = gantt_data.get("duration_indicator")
        anchor_indicator = gantt_data.get("anchor_indicator")
        additional_indicators = gantt_data.get("additional_indicators")
        assert class_name
        assert start_indicator
        assert end_indicator
        assert duration_indicator
        assert anchor_indicator

        with allure.step("Указать класс"):
            self.set_gantt_class(class_name)

        with allure.step("Настроить показатель старта мероприятий"):
            self.set_gantt_required_indicator('Дата начала*', start_indicator)

        with allure.step("Настроить показатель окончания мероприятий"):
            self.set_gantt_required_indicator('Дата окончания*', end_indicator)

        with allure.step("Настроить показатель длительности мероприятий"):
            self.set_gantt_required_indicator('Длительность*', duration_indicator)

        with allure.step("Настроить якорный показатель"):
            self.set_gantt_required_indicator('Якорное мероприятие*', anchor_indicator)

        if additional_indicators:
            with allure.step("Настроить дополнительные показатели"):
                self.set_additional_indicators(additional_indicators)



    def set_gantt_required_indicator(self, indicator_name: str, indicator_value: str):
        input_locator = (By.XPATH, f"//pkm-gant-settings//div[contains(@class, 'form-col') and .//*[.='{indicator_name}']]//input")
        actual_input_value = (By.XPATH, f"//pkm-gant-settings//div[contains(@class, 'form-col') and .//*[.='{indicator_name}']]//div[contains(@class, 'display-value-text')]")
        value_locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .=' {indicator_value} ']")
        self.find_and_click(input_locator)
        self.find_and_click(value_locator)
        time.sleep(2)
        self.wait_until_text_in_element(actual_input_value, indicator_value)

    def set_additional_indicators(self, indicators: list):
        plus_button_locator = self.add_entity_button_locator_creator("Дополнительные показатели")
        indicator_input_locator = (By.XPATH, "//div[@class='list-header' and .//div[contains(@class, 'title') and .='Дополнительные показатели']]//input")
        for indicator in indicators:
            self.find_and_click(plus_button_locator)
            self.find_and_click(indicator_input_locator)
            indicator_locator = self.dropdown_value_locator_creator(indicator)
            self.find_and_click(indicator_locator)
            time.sleep(1)
        actual_indicators_locator = self.list_elements_creator('Дополнительные показатели')
        actual_indicators = [i.text for i in self.elements_generator(actual_indicators_locator)]
        assert self.compare_lists(actual_indicators, indicators)

    def build_gantt(self):
        active_build_button_locator = (By.XPATH, "//gant//button[.=' Построить диаграмму ' and not(contains(@class, 'disabled'))]")
        self.find_and_click(active_build_button_locator)
        self.wait_stable_page()





