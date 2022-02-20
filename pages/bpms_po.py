from core import TimeoutException
from pages.components.entity_page import NewEntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from selenium.webdriver.common.by import By
from copy import deepcopy
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
            self.tree.tree_chain_actions(parent_node, ["Создать", "Бизнес процесс"])
            self.tree.modal.enter_and_save(bpms_name)
        with allure.step(f'Проверить отображение бизнес процесса {bpms_name} в дереве бизнес процессов выбранным'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, bpms_name)
        with allure.step(f'Проверить переход на страницу вновь соданной модели'):
            self.wait_page_title(bpms_name)

    def switch_on_bpms(self):
        self.switch_on_toggle('enabled')

    def create_bpms_diagram(self):
        create_button_locator = (By.XPATH, "//pkm-process-mx-diagram//ks-button[.='Создать диаграмму']")
        diagram_locator = (By.XPATH, "//div[contains(@class, 'geBackgroundPage')]")
        self.find_and_click(create_button_locator)
        self.find_element(diagram_locator)

    def consider_adding_process_elements(self):
        self.switch_on_toggle('considerAddingProcessElements')

    def consider_deleting_process_elements(self):
        toggle_block_locator = (By.XPATH, "//ks-switch[@formcontrolname='considerDeletingProcessElements']")
        toggle_locator = (By.XPATH, "//ks-switch[@formcontrolname='considerDeletingProcessElements']//div[contains(@class, 'slide')]//div[contains(@class, 'thumb')]")
        if 'slide-selected' not in self.get_element_html(toggle_block_locator):
            self.find_and_click(toggle_locator)

    def check_diagram_elements(self, elements: dict):
        """
        elements = {'events': 2, 'tasks': 3, 'arrows': 5}
        """

        self.wait_element_stable((By.XPATH, "//pkm-chart-diagram"), 5)

        for element in elements:
            if element == 'events':
                xpath = "//div[contains(@class, 'diagram-container')]//*[local-name()='ellipse']"

            elif element == 'tasks':
                xpath = "//div[contains(@class, 'diagram-container')]//*[local-name()='rect']"

            elif element == 'arrows':
                xpath = "(//div[contains(@class, 'diagram-container')]//*[local-name()='path'])[not(@visibility) and @pointer-events='stroke']"

            else:
                xpath = None

            if xpath:
                for i in range(elements[element]):
                    self.find_element((By.XPATH, f"({xpath})[{i+1}]"))


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
            'name': 'Название'
            'event_type': 'Начальное',
            'system_event_type': 'Ручное/внешнее',
            'next_element_type': 'Задача',
            'next_element_name': 'Название задачи'
        }
        """

        for field in event_data:
            value = event_data[field]
            if value:

                if field == 'name':
                    self.rename_title(value)

                if field == 'event_type':
                    self.set_event_type(value)

                elif field == 'system_event_type':
                    self.set_system_event_type(value)

                elif field == 'next_element_type':
                    self.set_next_element_type(value)

                elif field == 'next_element_name':
                    self.set_next_element(value)

                time.sleep(1)

    def get_event_type(self):
        selected_type_locator = (By.XPATH, "//div[contains(@class, 'event__bpmType')]//ks-radio-item[contains(@class, 'selected')]")
        selected_type = self.get_element_text(selected_type_locator)
        return selected_type

    def set_event_type(self, event_type: str):
        selected_type = self.get_event_type()
        if selected_type != event_type:
            target_button_locator = (By.XPATH, f"//div[contains(@class, 'event__bpmType')]//ks-radio-item[.=' {event_type} ']")
            self.find_and_click(target_button_locator)

    def get_system_event_type(self):
        event_type_dropdown_locator = self.dropdown_locator_creator('type')
        current_type = self.get_element_text(event_type_dropdown_locator, ignore_error=True)
        return current_type

    def set_system_event_type(self, event_type: str):
        current_type = self.get_system_event_type()
        if current_type != event_type:
            event_type_dropdown_locator = self.dropdown_locator_creator('type')
            self.find_and_click(event_type_dropdown_locator)
            self.find_and_click(self.dropdown_value_locator_creator(event_type))
            self.wait_until_text_in_element(event_type_dropdown_locator, event_type)

    def get_next_element_type(self):
        selected_type_locator = (By.XPATH, "//ks-radio[@formcontrolname='nextElementType']//ks-radio-item[.//div[contains(@class, 'selected')]]")
        selected_type = self.get_element_text(selected_type_locator, ignore_error=True)
        return selected_type

    def set_next_element_type(self, type_name: str):
        selected_type = self.get_next_element_type()
        if selected_type != type_name:
            target_button_locator = (By.XPATH, f"//ks-radio[@formcontrolname='nextElementType']//ks-radio-item[.=' {type_name} ']")
            self.find_and_click(target_button_locator)

    def get_next_element_name(self):
        try:
            element_field_locator = self.async_dropdown_locator_creator('nextElementUuid')
            value = self.get_input_value(element_field_locator)
            return value
        except TimeoutException:
            return


    def set_next_element(self, element_name: str):
        current_next_element = self.get_next_element_name()
        if current_next_element != element_name:
            element_field_locator = self.async_dropdown_locator_creator('nextElementUuid')
            self.find_and_enter(element_field_locator, element_name)
            self.find_and_click(self.dropdown_value_locator_creator(element_name))

    def get_event_page_data(self):
        template = {
            'name': (self.get_entity_page_title, (), {"return_raw": True}),
            'event_type': [self.get_event_type],
            'system_event_type': [self.get_system_event_type],
            'next_element_type': [self.get_next_element_type],
            'next_element_name': [self.get_next_element_name]
        }
        page_data = self.get_page_data_by_template(template)
        result = deepcopy(page_data)
        for i in page_data:
            if page_data[i] is None:
                del result[i]
        return result


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

    def set_task(self, task_data):
        """
                task_data = {
                    'name': 'Название'
                    'execution_type': 'Один исполнитель',
                    'task_executors': ['Иванов Андрей'],
                    'next_element_type': 'Задача',
                    'next_element_name': 'Название задачи'
                    'completion_criteria': 'Ручное завершение'
                }
                """

        for field in task_data:
            value = task_data[field]
            if value:

                if field == 'name':
                    self.rename_title(value)

                if field == 'execution_type':
                    self.set_execution_type(value)

                elif field == 'task_executors':
                    self.set_task_executors(value)

                elif field == 'next_element_type':
                    self.set_next_element_type(value)

                elif field == 'next_element_name':
                    self.set_next_element(value)

                elif field == 'completion_criteria':
                    self.set_completion_criteria(value)

                time.sleep(1)

    def get_execution_type(self):
        selected_type_locator = (By.XPATH, "//ks-radio[@formcontrolname='executionType']//ks-radio-item[contains(@class, 'selected')]")
        selected_type = self.get_element_text(selected_type_locator, ignore_error=True)
        return selected_type

    def set_execution_type(self, type_name: str):
        selected_type = self.get_execution_type()
        if selected_type != type_name:
            target_type_locator = (By.XPATH, f"//ks-radio[@formcontrolname='executionType']//ks-radio-item[.=' {type_name} ']")
            self.find_and_click(target_type_locator)

    def get_task_executors_list(self):
        executors_locator = (By.XPATH, "//div[contains(@class, 'task-settings__container') and .//div[contains(@class, 'task-settings__performers')]]//tbody//tr//td[1]")
        executors_list = []
        for row in self.elements_generator(executors_locator):
            executors_list.append(row.text)
        return executors_list

    def set_task_executors(self, executors_list: list):
        add_executor_button_locator = (By.XPATH, "//div[contains(@class, 'task-settings__container') and .//div[contains(@class, 'task-settings__performers')]]//ks-button[.='Добавить']")
        filter_input_locator = (By.XPATH, "//pkm-modal-window//div[contains(@class, 'filter-input')]//input")
        add_user_button_locator = (By.XPATH, "//pkm-modal-window//ks-button[.=' Добавить ']")

        current_executors_list = self.get_task_executors_list()

        for executor in executors_list:
            if executor not in current_executors_list:
                self.find_and_click(add_executor_button_locator)
                self.find_and_click(filter_input_locator)
                self.find_and_enter(filter_input_locator, executor, double_click=True)
                target_user_locator = (By.XPATH, f"(//div[contains(@class, 'users')]//div[.='{executor}'])[1]")
                self.find_and_click(target_user_locator)
                self.find_and_click(add_user_button_locator)

    def get_next_element_type(self):
        selected_type_locator = (By.XPATH, "//ks-radio[@formcontrolname='nextElementType']//ks-radio-item[.//div[contains(@class, 'selected')]]")
        selected_type = self.get_element_text(selected_type_locator)
        return selected_type

    def set_next_element_type(self, type_name: str):
        selected_type = self.get_next_element_type()
        if selected_type != type_name:
            target_button_locator = (By.XPATH, f"//ks-radio[@formcontrolname='nextElementType']//ks-radio-item[.=' {type_name} ']")
            self.find_and_click(target_button_locator)

    def get_next_element(self):
        element_field_locator = self.async_dropdown_locator_creator('nextElementUuid')
        value = self.get_input_value(element_field_locator)
        return value

    def set_next_element(self, element_name: str):
        element_field_locator = self.async_dropdown_locator_creator('nextElementUuid')
        self.find_and_enter(element_field_locator, element_name)
        self.find_and_click(self.dropdown_value_locator_creator(element_name))

    def get_completion_criteria(self):
        completion_criteria_dropdown_locator = (By.XPATH, "//ks-dropdown[@formcontrolname='completionCriteria']")
        current_completion_criteria = self.get_element_text(completion_criteria_dropdown_locator)
        return current_completion_criteria

    def set_completion_criteria(self, criteria_name: str):
        current_completion_criteria = self.get_completion_criteria()
        if current_completion_criteria != criteria_name:
            completion_criteria_dropdown_locator = (By.XPATH, "//ks-dropdown[@formcontrolname='completionCriteria']")
            self.find_and_click(completion_criteria_dropdown_locator)
            self.find_and_click(self.dropdown_value_locator_creator(criteria_name))

    def get_task_page_data(self):
        template = {
            'name': (self.get_entity_page_title, (), {"return_raw": True}),
            'execution_type': [self.get_execution_type],
            'task_executors': [self.get_task_executors_list],
            'next_element_type': [self.get_next_element_type],
            'next_element_name': [self.get_next_element],
            'completion_criteria': [self.get_completion_criteria]
        }
        page_data = self.get_page_data_by_template(template)
        return page_data


class BpmsGatePage(NewEntityPage):

    LOCATOR_TYPE_TYPE_DROPDOWN = (By.XPATH, "//ks-dropdown[@formcontrolname='type']")

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

    '''
    def get_entity_page_title(self, gate_type='ПАРАЛЛЕЛЬНЫЙ', without_type=False):
        raw_title = super().get_entity_page_title()
        if not without_type:
            return raw_title
        else:
            title = raw_title.split('\n')[1]
            return title

    def wait_page_title(self, page_title: str, timeout: int = 30, gate_type='ПАРАЛЛЕЛЬНЫЙ'):
        self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, f"{gate_type}.\n{page_title}", time=timeout)

    def rename_title(self, title_name, gate_type='ПАРАЛЛЕЛЬНЫЙ'):
        current_name = self.get_entity_page_title()
        expected_name = f'{gate_type}.\n{title_name}'
        if current_name != expected_name:
            self.find_and_click(self.LOCATOR_RENAME_TITLE_ICON)
            self.modal.enter_and_save(title_name, clear_input=True)
            self.wait_page_title(title_name)
    '''

    def set_gate(self, gate_data):
        """
        gate_data = {
            'name': 'Название',
            'gate_type': 'Параллельный',
            'next_elements': [
                {
                    'type': 'Задача',
                    'name': 'Задача 1'
                },
                {
                    'type': 'Задача',
                    'name': 'Задача 2'
                }
            ]
        }
        """
        for field in gate_data:
            value = gate_data[field]
            if value:

                if field == 'name':
                    self.rename_title(value)

                elif field == 'gate_type':
                    self.set_gate_type(value)

                elif field == 'next_elements':
                    self.set_next_elements(value)

                time.sleep(1)

    def get_gate_type(self):
        dropdown_type = self.get_element_text(self.LOCATOR_TYPE_TYPE_DROPDOWN)
        return dropdown_type

    def set_gate_type(self, gate_type: str):
        current_type = self.get_gate_type()
        if current_type != gate_type:
            self.find_and_click(self.LOCATOR_TYPE_TYPE_DROPDOWN)
            self.find_and_click(self.dropdown_value_locator_creator(gate_type))

    def get_next_elements(self):
        result = []
        elements_rows_locator = (By.XPATH, "//tbody[@formarrayname='nextElements']//tr")
        row_count = 0
        for element_row in self.elements_generator(elements_rows_locator):
            row_count += 1
            try:
                entity_type = self.get_element_text((By.XPATH, f"(//tbody[@formarrayname='nextElements']//tr)[{row_count}]/td[2]"))
                entity_name = self.get_element_text((By.XPATH, f"(//tbody[@formarrayname='nextElements']//tr)[{row_count}]/td[3]"))
            except TimeoutException:
                return result
            result.append({'type': entity_type, 'name': entity_name})
        return result

    def set_next_elements(self, elements: list):
        """
        elements = [
                {
                    'type': 'Задача',
                    'name': 'Задача 1'
                },
                {
                    'type': 'Задача',
                    'name': 'Задача 2'
                }
            ]
        """
        current_elements = self.get_next_elements()

        for element in elements:
            if element not in current_elements:
                self.find_and_click((By.XPATH, "//div[contains(@class, 'gate__title')]//ks-button[.='Добавить']"))
                self.find_and_click(self.dropdown_locator_creator('nextElementType'))
                self.find_and_click(self.dropdown_value_locator_creator(element['type']))

                self.find_and_enter(self.async_dropdown_locator_creator('nextElementUuid'), element['name'])
                self.find_and_click(self.dropdown_value_locator_creator(element['name']))

                self.find_and_click(self.modal.LOCATOR_SAVE_BUTTON)

    def get_gate_page_data(self):
        template = {
            'name': [self.get_entity_page_title],
            'gate_type': [self.get_gate_type],
            'next_elements': [self.get_next_elements]
        }
        page_data = self.get_page_data_by_template(template)
        return page_data

