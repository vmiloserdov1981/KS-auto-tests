from pages.components.entity_page import NewEntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
import allure
import time
import random


class BpmsPage(NewEntityPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    def create_bpms(self, parent_node, bpms_name):
        with allure.step(f'Создать бизнес процесс {bpms_name}'):
            time.sleep(random.randint(1, 6))
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.context_option_locator_creator('Бизнес процесс'))
            self.tree.modal.enter_and_save(bpms_name)
        with allure.step(f'Проверить отображение бизнес процесса {bpms_name} в дереве бизнес процессов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, bpms_name)
        with allure.step(f'Проверить переход на страницу вновь соданной модели'):
            self.wait_page_title(bpms_name)


class BpmsEventPage(NewEntityPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    def create_bpms_event(self, parent_node, bpms_event_name):
        with allure.step(f'Создать событие {bpms_event_name}'):
            self.tree.tree_chain_actions(parent_node, ['Создать', 'Событие'])
            self.tree.modal.enter_and_save(bpms_event_name)
        with allure.step(f'Проверить отображение события {bpms_event_name} в дереве бизнес процессов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, bpms_event_name)
        with allure.step(f'Проверить переход на страницу вновь созданного события'):
            self.wait_page_title(bpms_event_name)

    def set_event(self, event_data: dict):
        """
        event_data = {
            'event_type': 'Начальное',
            'system_event_type': 'Ручное/внешнее',
            'next_element_type': 'Задача',
            'next_element_name': 'Название задачи'
        }
        """

        for field in event_data:
            value = event_data[field]
            if value:

                if field == 'event_type':
                    self.set_event_type(value)

                elif field == 'system_event_type':
                    self.set_system_event_type(value)

                elif field == 'next_element_type':
                    self.set_next_element_type(value)

                elif field == 'next_element_name':
                    self.set_next_element(value)

                time.sleep(1)

    def set_event_type(self, event_type: str):
        selected_type_locator = (By.XPATH, "//div[contains(@class, 'event__bpmType')]//ks-radio-item[contains(@class, 'selected')]")
        selected_type = self.get_element_text(selected_type_locator)
        if selected_type != event_type:
            target_button_locator = (By.XPATH, f"//div[contains(@class, 'event__bpmType')]//ks-radio-item[.=' {event_type} ']")
            self.find_and_click(target_button_locator)

    def set_system_event_type(self, event_type: str):
        event_type_dropdown_locator = self.dropdown_locator_creator('type')
        current_type = self.get_element_text(event_type_dropdown_locator)
        if current_type != event_type:
            self.find_and_click(event_type_dropdown_locator)
            self.find_and_click(self.dropdown_value_locator_creator(event_type))
            self.wait_until_text_in_element(event_type_dropdown_locator, event_type)

    def set_next_element_type(self, type_name: str):
        selected_type_locator = (By.XPATH, "//ks-radio[@formcontrolname='nextElementType']//ks-radio-item[.//div[contains(@class, 'selected')]]")
        selected_type = self.get_element_text(selected_type_locator)
        if selected_type != type_name:
            target_button_locator = (By.XPATH, f"//ks-radio[@formcontrolname='nextElementType']//ks-radio-item[.=' {type_name} ']")
            self.find_and_click(target_button_locator)

    def set_next_element(self, element_name: str):
        element_field_locator = self.async_dropdown_locator_creator('nextElementUuid')
        self.find_and_enter(element_field_locator, element_name)
        self.find_and_click(self.dropdown_value_locator_creator(element_name))


class BpmsTaskPage(NewEntityPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    def create_bpms_task(self, parent_node, bpms_task_name):
        with allure.step(f'Создать задачу {bpms_task_name}'):
            self.tree.tree_chain_actions(parent_node, ['Создать', 'Задачу'])
            self.tree.modal.enter_and_save(bpms_task_name)
        with allure.step(f'Проверить отображение события {bpms_task_name} в дереве бизнес процессов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, bpms_task_name)
        with allure.step(f'Проверить переход на страницу вновь созданного события'):
            self.wait_page_title(bpms_task_name)


class BpmsGatePage(NewEntityPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    def create_bpms_gate(self, parent_node, bpms_gate_name):
        with allure.step(f'Создать шлюз {bpms_gate_name}'):
            self.tree.tree_chain_actions(parent_node, ['Создать', 'Шлюз'])
            self.tree.modal.enter_and_save(bpms_gate_name)
        with allure.step(f'Проверить отображение шлюза {bpms_gate_name} в дереве бизнес процессов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, bpms_gate_name)
        with allure.step(f'Проверить переход на страницу вновь созданного шлюза'):
            self.wait_page_title(bpms_gate_name)

    def wait_page_title(self, page_title: str, timeout: int = 30, gate_type='ПАРАЛЛЕЛЬНЫЙ'):
        self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, f"{gate_type}.\n{page_title}", time=timeout)
