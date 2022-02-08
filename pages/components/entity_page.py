from core import BasePage, antistale
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from pages.components.modals import Modals
import time
import allure


class EntityPage(BasePage):
    LOCATOR_ENTITY_PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'title-value')]")
    LOCATOR_PAGE_TITLE_BLOCK = (By.XPATH, "//div[@class='page-title-container']//div[@class='title-value']")
    LOCATOR_TITLE_INPUT = (By.XPATH, "(//div[@class='page-title-container']//input)[1]")
    LOCATOR_TITLE_CHECK_ICON = (By.XPATH, "//div[@class='page-title-container']//fa-icon[@icon='check']")
    LOCATOR_PAGE_CONTENT = (By.XPATH, "//div[contains(@class, 'router-outlet')]//div[contains(@class, 'page-container')]")

    @staticmethod
    def add_list_element_button_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and text()='{list_name}'] ]//fa-icon[@icon='plus']")
        return locator

    @staticmethod
    def list_sort_button_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and text()='{list_name}' or @class='title' and text()=' {list_name} '] ]//fa-icon[@icon='sort']")
        return locator

    @staticmethod
    def sort_type_button_creator(sort_type):
        locator = (By.XPATH, f"//div[contains(@class, 'overlay-item') and ./div[.='{sort_type}']]")
        return locator

    @staticmethod
    def sort_order_icon_creator(sort_type):
        element_xpath = EntityPage.sort_type_button_creator(sort_type)[1]
        locator = (By.XPATH, element_xpath + "//*[local-name()='svg' and contains(@data-icon, 'arrow-')]")
        return locator

    @staticmethod
    def list_element_creator(list_name, element_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{list_name}'] ]//div[contains(@class, 'list-item ') and .='{element_name}' or contains(@class, 'list-item ') and .=' {element_name} ']")
        return locator

    @staticmethod
    def class_relation_link_locator_creator(relation_name):
        locator = (By.XPATH,
                   f"//div[@class='list' and .//div[@class='title' and .='Связи'] ]//div[contains(@class, 'list-item')]//relation-arrow[.=' {relation_name} ']")
        return locator

    @staticmethod
    def list_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{list_name}']]")
        return locator

    @staticmethod
    def list_elements_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{list_name}'] ]//div[contains(@class, 'list-item ')]")
        return locator

    @staticmethod
    def list_element_rename_button_creator(list_name, element_name):
        element_xpath = EntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='edit']")
        return locator

    @staticmethod
    def list_element_delete_button_creator(list_name, element_name):
        element_xpath = EntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='trash']")
        return locator

    @staticmethod
    def dropdown_locator_creator(form_control_name):
        locator = (By.XPATH, f"//pkm-dropdown[@formcontrolname='{form_control_name}']//div[contains(@class, 'dropdown')]")
        return locator

    @staticmethod
    def async_dropdown_locator_creator(form_control_name):
        locator = (By.XPATH, f"//async-dropdown-search[@formcontrolname='{form_control_name}']//div[contains(@class, 'dropdown')]//input")
        return locator

    @staticmethod
    def pkm_dropdown_actual_value_locator_creator(form_control_name):
        locator = (By.XPATH, f"//pkm-dropdown[@formcontrolname='{form_control_name}']//div[contains(@class,'display-value-text')]")
        return locator

    @staticmethod
    def input_locator_creator(form_control_name):
        locator = (By.XPATH, f"//input[@formcontrolname='{form_control_name}']")
        return locator

    @staticmethod
    def add_entity_button_locator_creator(entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'list-header') and .='{entity_name}']//fa-icon[@icon='plus']")
        return locator

    @staticmethod
    def list_element_edit_button_locator_creator(list_name, element_name):
        element_xpath = EntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='pencil-alt']")
        return locator

    @staticmethod
    def dropdown_value_locator_creator(value_name):
        locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .='{value_name}' or contains(@class, 'dropdown-item') and .=' {value_name} ']")
        return locator

    def get_entity_page_title(self, return_raw=False, prev_title_html: str = None, timeout=10):
        if prev_title_html:
            self.wait_element_changing(prev_title_html, self.LOCATOR_ENTITY_PAGE_TITLE, time=5, ignore_timeout=True)
        if return_raw:
            title = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
        else:
            title = self.get_element_text(self.LOCATOR_ENTITY_PAGE_TITLE, time=timeout)
        return title

    def wait_page_title(self, page_title: str, timeout: int = 10):
        self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, page_title, time=timeout)

    def rename_title(self, title_name):
        self.find_and_click(self.LOCATOR_PAGE_TITLE_BLOCK)
        title_input = self.find_element(self.LOCATOR_TITLE_INPUT)
        title_input.send_keys(Keys.CONTROL + "a")
        title_input.send_keys(Keys.DELETE)
        title_input.send_keys(title_name)
        self.find_and_click(self.LOCATOR_TITLE_CHECK_ICON)
        actual_title_name = (self.get_element_text(self.LOCATOR_PAGE_TITLE_BLOCK))
        assert actual_title_name == title_name.upper()
        time.sleep(2)

    def get_list_elements_names(self, list_name, timeout=5):
        elements = [element.text for element in self.elements_generator(self.list_elements_creator(list_name), time=timeout)]
        return elements if elements != [] else None

    def get_change_data(self):
        create_info = self.get_element_text((By.XPATH, "//pkm-changes-entity-info//div[contains(@class, 'info__item') and ./span[.='Создано:']]//span[2]"))
        update_info = self.get_element_text((By.XPATH, "//pkm-changes-entity-info//div[contains(@class, 'info__item') and ./span[.='Изменено:']]//span[2]"))
        data = {
            'created_at': create_info.split(' / ')[0],
            'created_by': create_info.split(' / ')[1],
            'updated_at': update_info.split(' / ')[0],
            'updated_by': update_info.split(' / ')[1]
        }
        return data

    def get_page_data_by_template_old(self, template):
        '''
        template = {
            'model_name': (self.get_entity_page_title, (), {"return_raw": True}),
            'changes': [self.get_change_data],
            'datasets': [self.get_model_datasets],
            'dimensions': [self.get_model_dimensions],
            'time_period': [self.get_model_period_type],
            'period_amount': [self.get_model_period_amount],
            'last_period': [self.get_model_last_period],
            'solver_values': [self.get_model_solvers],
            'tags': [self.get_model_tags]
        }
        '''

        self.wait_stable_page()
        result = {}

        with ThreadPoolExecutor() as executor:
            for field in template:

                function = template.get(field)[0]
                try:
                    args = template.get(field)[1]
                except IndexError:
                    args = ()
                try:
                    kwargs = template.get(field)[2]
                except IndexError:
                    kwargs = {}

                result[field] = executor.submit(function, *args, **kwargs).result()

        sorted_result = {}
        for field in template:
            if field in result.keys():
                sorted_result[field] = result.get(field)
        return sorted_result

    @antistale
    def get_page_data_by_template(self, template):
        """
        template = {
            'model_name': (self.get_entity_page_title, (), {"return_raw": True}),
            'changes': [self.get_change_data],
            'datasets': [self.get_model_datasets],
            'dimensions': [self.get_model_dimensions],
            'time_period': [self.get_model_period_type],
            'period_amount': [self.get_model_period_amount],
            'last_period': [self.get_model_last_period],
            'solver_values': [self.get_model_solvers],
            'tags': [self.get_model_tags]
        }
        """

        self.wait_stable_page(timeout=2)
        futures = {}

        with allure.step('Получить данные страницы'):
            with ThreadPoolExecutor() as executor:
                for field in template:
                    function = template.get(field)[0]
                    try:
                        args = template.get(field)[1]
                    except IndexError:
                        args = ()
                    try:
                        kwargs = template.get(field)[2]
                    except IndexError:
                        kwargs = {}

                    futures[field] = executor.submit(function, *args, **kwargs)

        sorted_result = {}
        for field in template:
            sorted_result[field] = futures[field].result()
        return sorted_result

    def wait_stable_page(self, timeout=3):
        self.wait_element_stable(self.LOCATOR_PAGE_CONTENT, timeout)


class NewEntityPage(BasePage):
    LOCATOR_ENTITY_PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'entity__configuration-name')]")
    LOCATOR_RENAME_TITLE_ICON = (By.XPATH, "//div[contains(@class, 'entity__configuration-name')]//fa-icon[.//*[local-name()='svg' and @data-icon='pen']]")
    #LOCATOR_TITLE_INPUT = (By.XPATH, "(//div[@class='page-title-container']//input)[1]")
    #LOCATOR_TITLE_CHECK_ICON = (By.XPATH, "//div[@class='page-title-container']//fa-icon[@icon='check']")
    LOCATOR_PAGE_CONTENT = (By.XPATH, "//div[contains(@class, 'router-outlet')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.modal = Modals(driver)

    @staticmethod
    def add_list_element_button_creator(list_name):
        locator = (By.XPATH, f"//div[contains(@class, 'container-table__header_buttons header') and .//div[contains(@class, 'header__title') and .='{list_name}']]//ks-button[.//*[local-name()='svg' and @data-icon='plus']]")
        return locator

    @staticmethod
    def list_sort_button_creator(list_name):
        locator = (By.XPATH, f"//div[contains(@class, 'container-table__header') and .//div[contains(@class, 'header__title') and .='{list_name}']]//ks-sorting//button")
        return locator

    @staticmethod
    def sort_type_button_creator(sort_type):
        locator = (By.XPATH, f"//div[contains(@class, 'ks-sort')]//div[contains(@class, 'item') and .='{sort_type}']")
        return locator

    @staticmethod
    def sort_order_icon_creator(list_name):
        element_xpath = NewEntityPage.list_sort_button_creator(list_name)[1]
        locator = (By.XPATH, element_xpath + "//*[local-name()='svg' and contains(@data-icon, 'sort-amount-')]")
        return locator

    @staticmethod
    def list_element_creator(list_name, element_name):
        elements_xpath = NewEntityPage.list_elements_creator(list_name)[1]
        locator = (By.XPATH, f"({elements_xpath})[.='{element_name}']")
        return locator

    @staticmethod
    def class_relation_link_locator_creator(relation_name):
        locator = (By.XPATH, f"(//div[contains(@class, 'container-table') and .//div[contains(@class, 'header__title') and .='Связи']]//div[contains(@class, 'content__row') and .//div[contains(@class, 'content__row_up-relation') and .='{relation_name}']])[1]")
        return locator

    @staticmethod
    def list_creator(list_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{list_name}']]")
        return locator

    @staticmethod
    def list_elements_creator(list_name):
        locator = (By.XPATH, f"//div[contains(@class, 'container-table') and .//div[contains(@class, 'header__title') and .='{list_name}']]//*[contains(@class, 'ks-page__entity-title') or contains(@class, 'ks-page__title')]")
        return locator

    @staticmethod
    def list_element_delete_button_creator(list_name, element_name):
        element_xpath = NewEntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "/../..//fa-icon[./*[local-name()='svg'  and @data-icon='trash']]")
        return locator

    @staticmethod
    def dropdown_locator_creator(form_control_name):
        locator = (By.XPATH, f"//ks-dropdown[@formcontrolname='{form_control_name}']//div[contains(@class, 'dropdown')]")
        return locator

    @staticmethod
    def async_dropdown_locator_creator(form_control_name):
        locator = (By.XPATH, f"//async-dropdown-search[@formcontrolname='{form_control_name}']//div[contains(@class, 'dropdown')]//input")
        return locator

    @staticmethod
    def pkm_dropdown_actual_value_locator_creator(form_control_name):
        locator = (By.XPATH, f"//ks-dropdown[@formcontrolname='{form_control_name}']//div[contains(@class,'display-value-text')]")
        return locator

    @staticmethod
    def input_locator_creator(form_control_name):
        locator = (By.XPATH, f"//ks-input[@formcontrolname='{form_control_name}']//input")
        return locator

    @staticmethod
    def checkbox_locator_creator(form_control_name, label=None):
        locator = (By.XPATH, f"//ks-checkbox[@formcontrolname='{form_control_name}' or @label='{label}']//div[contains(@class, 'checkbox-container')]")
        return locator

    @staticmethod
    def add_entity_button_locator_creator(entity_name):
        locator = (By.XPATH, f"//div[contains(@class, 'header__buttons')]//ks-button[contains(@class, 'header__buttons_create') and .='{entity_name}']")
        return locator

    @staticmethod
    def list_element_edit_button_locator_creator(list_name, element_name):
        element_xpath = NewEntityPage.list_element_creator(list_name, element_name)[1]
        locator = (By.XPATH, element_xpath + "/../..//fa-icon[./*[local-name()='svg'  and @data-icon='pencil-alt']]")
        return locator

    @staticmethod
    def dropdown_value_locator_creator(value_name):
        locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .='{value_name}' or contains(@class, 'dropdown-item') and .=' {value_name} ']")
        return locator

    def get_entity_page_title(self, return_raw=False, prev_title_html: str = None, timeout=10) -> str:
        if prev_title_html:
            self.wait_element_changing(prev_title_html, self.LOCATOR_ENTITY_PAGE_TITLE, time=5, ignore_timeout=True)
        if return_raw:
            title = self.driver.execute_script("return arguments[0].textContent;", self.find_element(self.LOCATOR_ENTITY_PAGE_TITLE)).strip()
        else:
            title = self.get_element_text(self.LOCATOR_ENTITY_PAGE_TITLE, time=timeout)
        return title

    def wait_page_title(self, page_title: str, timeout: int = 30):
        self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, page_title, time=timeout)

    def rename_title(self, title_name):
        current_name = self.get_entity_page_title()
        if current_name != title_name:
            self.find_and_click(self.LOCATOR_RENAME_TITLE_ICON)
            self.modal.enter_and_save(title_name, clear_input=True)
            self.wait_page_title(title_name)

    def get_list_elements_names(self, list_name, timeout=5):
        elements = [element.text for element in self.elements_generator(self.list_elements_creator(list_name), time=timeout)]
        return elements if elements != [] else None

    def get_change_data(self):
        create_info = self.get_element_text((By.XPATH, "//pkm-changes-entity-info//div[contains(@class, 'info__item') and ./span[.='Создано:']]//span[2]"))
        update_info = self.get_element_text((By.XPATH, "//pkm-changes-entity-info//div[contains(@class, 'info__item') and ./span[.='Изменено:']]//span[2]"))
        data = {
            'created_at': create_info.split(' / ')[0],
            'created_by': create_info.split(' / ')[1],
            'updated_at': update_info.split(' / ')[0],
            'updated_by': update_info.split(' / ')[1]
        }
        return data

    def get_page_data_by_template_old(self, template):
        '''
        template = {
            'model_name': (self.get_entity_page_title, (), {"return_raw": True}),
            'changes': [self.get_change_data],
            'datasets': [self.get_model_datasets],
            'dimensions': [self.get_model_dimensions],
            'time_period': [self.get_model_period_type],
            'period_amount': [self.get_model_period_amount],
            'last_period': [self.get_model_last_period],
            'solver_values': [self.get_model_solvers],
            'tags': [self.get_model_tags]
        }
        '''

        self.wait_stable_page()
        result = {}

        with ThreadPoolExecutor() as executor:
            for field in template:

                function = template.get(field)[0]
                try:
                    args = template.get(field)[1]
                except IndexError:
                    args = ()
                try:
                    kwargs = template.get(field)[2]
                except IndexError:
                    kwargs = {}

                result[field] = executor.submit(function, *args, **kwargs).result()

        sorted_result = {}
        for field in template:
            if field in result.keys():
                sorted_result[field] = result.get(field)
        return sorted_result

    @antistale
    def get_page_data_by_template(self, template) -> dict:
        """
        template = {
            'model_name': (self.get_entity_page_title, (), {"return_raw": True}),
            'changes': [self.get_change_data],
            'datasets': [self.get_model_datasets],
            'dimensions': [self.get_model_dimensions],
            'time_period': [self.get_model_period_type],
            'period_amount': [self.get_model_period_amount],
            'last_period': [self.get_model_last_period],
            'solver_values': [self.get_model_solvers],
            'tags': [self.get_model_tags]
        }
        """

        self.wait_stable_page(timeout=2)
        futures = {}

        with allure.step('Получить данные страницы'):
            with ThreadPoolExecutor() as executor:
                for field in template:
                    function = template.get(field)[0]
                    try:
                        args = template.get(field)[1]
                    except IndexError:
                        args = ()
                    try:
                        kwargs = template.get(field)[2]
                    except IndexError:
                        kwargs = {}

                    futures[field] = executor.submit(function, *args, **kwargs)

        sorted_result = {}
        for field in template:
            sorted_result[field] = futures[field].result()
        return sorted_result

    def wait_stable_page(self, timeout=3):
        self.wait_element_stable(self.LOCATOR_PAGE_CONTENT, timeout)

    def get_active_page_tab_name(self):
        active_tab_locator = (By.XPATH, "//div[contains(@class, 'tab-title') and contains(@class, 'active')]")
        active_tab_name = self.get_element_text(active_tab_locator)
        return active_tab_name

    def switch_to_tab(self, tab_name: str):
        target_tab_locator = (By.XPATH, f"//div[contains(@class, 'tab-title') and .=' {tab_name} ']")
        if 'active' not in self.find_element(target_tab_locator).get_attribute('class'):
            self.find_and_click(target_tab_locator)

