from pages.components.entity_page import NewEntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals, Calendar
from core import antistale
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
# import datetime
import allure
import time


class ModelPage(NewEntityPage):
    DIMENSIONS_LIST_NAME = 'Измерения'
    DATASETS_LIST_NAME = 'Наборы данных'
    TIME_PERIOD_LIST_NAME = 'Временной интервал'
    SOLVERS_LIST_NAME = 'Поиск решения'
    TAGS_LIST_NAME = 'Теги'

    LOCATOR_MODEL_PERIOD_DATEPICKER = (By.XPATH, f"//div[contains(@class, 'time-measurement')]//ks-date-picker")
    LOCATOR_MODEL_PERIOD_DROPDOWN = (By.XPATH, f"//div[contains(@class, 'time-measurement')]//ks-dropdown[@formcontrolname='timePeriod']")
    LOCATOR_MODEL_PERIOD_SAVE_BUTTON = (By.XPATH, f"//div[contains(@class, 'time-measurement-body')]//button[.//*[local-name()='svg' and @data-icon='save']]")
    LOCATOR_MODEL_PERIOD_DELETE_BUTTON = (By.XPATH, f"//div[contains(@class, 'time-measurement-body')]//button[.//*[local-name()='svg' and @data-icon='trash']]")
    LOCATOR_MODEL_PERIOD_TIME = (By.XPATH, "//ks-dropdown[@formcontrolname='timePeriod']")
    LOCATOR_MODEL_PERIOD_AMOUNT_INPUT = (By.XPATH, "//input[@formcontrolname='amount']")
    LOCATOR_MODEL_PERIOD_START_YEAR = (By.XPATH, "//ks-dropdown[@formcontrolname='year']")
    LOCATOR_MODEL_LAST_PERIOD = (By.XPATH, "//input[@formcontrolname='result']")
    LOCATOR_MODEL_SEARCH_TAG_INPUT = (By.XPATH, "//div[contains(@class, 'model-tags__search')]//input")
    LOCATOR_MODEL_TAG = (By.XPATH, "//ks-array-label-display//div[contains(@class, 'item ')]")
    LOCATOR_ADD_TAG_BUTTON = (By.XPATH, "//div[contains(@class, 'create-tag')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)
        self.calendar = Calendar(driver)

    @staticmethod
    def datasets_list_value_locator_creator(dataset_name):
        #locator = (By.XPATH, f"//div[contains(@class, 'container-table') and .//div[contains(@class, 'header__title') and .='Наборы данных']]//tr[contains(@class, 'entity__row') and .//td[contains(text(), ' {dataset_name} ')]]")
        locator = (By.XPATH, f"//tr[.//span[contains(text(), '{dataset_name}')]]")
        return locator

    @staticmethod
    def model_tag_locator_creator(tag_name):
        xpath = ModelPage.LOCATOR_MODEL_TAG[1]
        xpath = xpath + f"[.=' {tag_name} ' or .='{tag_name}']"
        locator = (By.XPATH, xpath)
        return locator

    def get_model_page_data(self) -> dict:
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
        data = self.get_page_data_by_template(template)
        return data

    def create_model(self, parent_node, model_name):
        with allure.step(f'Создать модель {model_name}'):
            self.tree.create_node(model_name, 'Создать модель', parent_node)
        api = self.api_creator.get_api_models()
        # actual_date = f'{".".join(api.get_utc_date())}'
        # actual_time = api.get_utc_time()
        with allure.step(f'Проверить отображение модели {model_name} в дереве моделей выбранной'):
            self.wait_until_text_in_element(self.tree.LOCATOR_SELECTED_NODE, model_name)
        with allure.step(f'Проверить переход на страницу вновь соданной модели'):
            self.wait_page_title(model_name)
        model_uuid = api.get_model_uuid_by_name(model_name)
        api_change_dates = api.get_model_change_dates(model_uuid)
        """
        with allure.step(f'Проверить заполнение созданной модели данными по умолчанию'):
            actual = self.get_model_page_data()
            expected = {
                'model_name': model_name,
                'changes': {
                    'created_at': api_change_dates.get('created_at'),
                    'created_by': self.driver.current_user.name,
                    'updated_at': api_change_dates.get('updated_at'),
                    'updated_by': self.driver.current_user.name
                },
                'datasets': None,
                'dimensions': None,
                'time_period': None,
                'period_amount': None,
                'last_period': None,
                'solver_values': None,
                'tags': None
            }
            self.compare_dicts(actual, expected)
        """

    def get_model_dimensions(self, sort_value=None, sort_order=None):
        if sort_value and sort_order:
            self.sort_dimensions(sort_value, sort_order)
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME)
        return elements

    @antistale
    def get_model_datasets(self, sort_value=None, sort_order=None):
        if sort_value and sort_order:
            self.sort_datasets(sort_value, sort_order)

        names_locator = (By.XPATH, f"//div[contains(@class, 'container-table') and .//div[contains(@class, 'header__title') and .='{self.DATASETS_LIST_NAME}']]//tr[contains(@class, 'entity__row')]//td[1]")
        names = [element.text for element in self.elements_generator(names_locator)]
        result = []

        if names and names != []:
            for name in names:
                if '(По умолчанию)' not in name:
                    value = {'name': name, 'is_default': False}
                else:
                    value = {'name': name.split('(По умолчанию)')[0], 'is_default': True}
                result.append(value)

        return result if result != [] else None

    def get_model_period_type(self):
        value = self.get_element_text((By.XPATH, "//ks-dropdown[@formcontrolname='periodType']//div[contains(@class, 'ks-dropdown-values')]"), ignore_error=True, time=2)
        return value if value != 'Временной период' else None

    def get_model_period_amount(self):
        value = self.get_input_value(self.LOCATOR_MODEL_PERIOD_AMOUNT_INPUT, return_empty=False, time=2)
        return value

    def get_model_last_period(self):
        value = self.get_input_value(self.LOCATOR_MODEL_LAST_PERIOD, return_empty=False, time=2)
        return value

    def get_model_start_period(self):
        try:
            value = self.get_element_text(self.LOCATOR_MODEL_PERIOD_DATEPICKER, time=3)
        except TimeoutException:
            value = self.get_element_text(self.LOCATOR_MODEL_PERIOD_DROPDOWN, time=3, ignore_error=True)
        return value

    def get_model_start_year(self):
        value = self.get_element_text(self.LOCATOR_MODEL_PERIOD_START_YEAR, ignore_error=True, time=2)
        return value

    def get_model_solvers(self):
        elements = self.get_list_elements_names(self.SOLVERS_LIST_NAME)
        return elements

    def get_model_tags(self):
        elements = [element.text for element in self.elements_generator(self.LOCATOR_MODEL_TAG, time=5)]
        return elements if elements != [] else None

    def create_dataset(self, dataset_name, is_default=None):
        if self.get_model_datasets():
            is_first_dataset = False
        else:
            is_first_dataset = True

        self.find_and_click(self.add_list_element_button_creator(self.DATASETS_LIST_NAME))
        if is_default is True and not is_first_dataset:
            self.modal.check_checkbox('Использовать по умолчанию')
        elif is_default is False and not is_first_dataset:
            self.modal.uncheck_checkbox('Использовать по умолчанию')
        self.modal.enter_and_save(dataset_name)

    def sort_datasets(self, sort_type, sort_order):
        self.find_and_click(self.list_sort_button_creator(self.DATASETS_LIST_NAME))
        self.find_and_click(self.sort_type_button_creator(sort_type))
        sort_order_icon_locator = self.sort_order_icon_creator(self.DATASETS_LIST_NAME)

        if sort_order == 'ASC':
            if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'sort-amount-down':
                self.find_and_click(sort_order_icon_locator)
                if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'sort-amount-down':
                    raise AssertionError('Не удалось установить сортировку по возрастанию')

        elif sort_order == 'DESC':
            if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'sort-amount-up':
                self.find_and_click(sort_order_icon_locator)
                if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'sort-amount-up':
                    raise AssertionError('Не удалось установить сортировку по убыванию')

    def sort_dimensions(self, sort_type, sort_order):
        self.find_and_click(self.list_sort_button_creator(self.DIMENSIONS_LIST_NAME))
        self.find_and_click(self.sort_type_button_creator(sort_type))
        sort_order_icon_locator = self.sort_order_icon_creator(sort_type)

        if sort_order == 'ASC':
            if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'arrow-down':
                self.find_and_click(self.sort_type_button_creator(sort_type))
                if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'arrow-down':
                    raise AssertionError('Не удалось установить сортировку по возрастанию')

        elif sort_order == 'DESC':
            if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'arrow-up':
                self.find_and_click(self.sort_type_button_creator(sort_type))
                if self.find_element(sort_order_icon_locator).get_attribute('data-icon') != 'arrow-up':
                    raise AssertionError('Не удалось установить сортировку по убыванию')

        self.find_and_click(self.list_sort_button_creator(self.DIMENSIONS_LIST_NAME))

    def rename_dataset(self, dataset_name, dataset_new_name):
        dataset_locator = self.datasets_list_value_locator_creator(dataset_name)
        self.hover_over_element(dataset_locator)
        rename_button_locator = (By.XPATH, f"{dataset_locator[1]}//*[local-name()='svg' and @data-icon='pencil-alt']")
        self.find_and_click(rename_button_locator)
        self.modal.enter_and_save(dataset_new_name, clear_input=True)

    def delete_dataset(self, dataset_name):
        dataset_locator = self.datasets_list_value_locator_creator(dataset_name)
        self.hover_over_element(dataset_locator)
        delete_button_locator = (By.XPATH, f"{dataset_locator[1]}//*[local-name()='svg' and @data-icon='trash']")
        self.find_and_click(delete_button_locator)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(dataset_locator, wait_display=False), f'Набор данных {dataset_name} не исчезает из списка после удаления'

    def add_dimension(self, dimension_name):
        self.find_and_click(self.add_entity_button_locator_creator(self.DIMENSIONS_LIST_NAME))
        dimensions_field = (By.XPATH, f"//div[contains(@class, 'list-header') and .='{self.DIMENSIONS_LIST_NAME}']//input")
        self.find_and_enter(dimensions_field, dimension_name)
        self.find_and_click(self.modal.dropdown_item_locator_creator(dimension_name))
        self.find_element(self.list_element_creator(f'{self.DIMENSIONS_LIST_NAME}', dimension_name))

    def delete_dimension(self, dimension_name):
        dimension_locator = self.list_element_creator(self.DIMENSIONS_LIST_NAME, dimension_name)
        self.hover_over_element(dimension_locator)
        delete_button_locator = (By.XPATH, f"{dimension_locator[1]}//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='trash']")
        self.find_and_click(delete_button_locator)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(dimension_locator, wait_display=False), f'Измерение {dimension_name} не исчезает из списка при удалении'

    def set_model_period_type(self, period_type: str):
        self.find_and_click(self.dropdown_locator_creator('periodType'))
        self.find_and_click(self.dropdown_value_locator_creator(period_type))
        assert self.get_model_period_type() == period_type, "В дропдауне периода отображается некорректное значение"

    def set_start_period_month(self, month: str):
        month_locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .='{month}']")
        self.find_and_click(self.LOCATOR_MODEL_PERIOD_TIME)
        self.find_and_click(month_locator)

    def get_model_period_data(self):
        template = {
            "period_type": [self.get_model_period_type],
            'period_start_value': [self.get_model_start_period],
            'period_start_year': [self.get_model_start_year],
            'period_amount': [self.get_model_period_amount],
            'last_period': [self.get_model_last_period]
        }
        data = self.get_page_data_by_template(template)
        return data

    def set_start_period_day(self, amount: str):
        self.find_and_click(self.LOCATOR_MODEL_PERIOD_DATEPICKER)
        self.calendar.select_day(amount)
        self.find_and_click(self.calendar.LOCATOR_ACCEPT_DATA_BUTTON)

    def set_period_amount(self, amount):
        self.find_element(self.LOCATOR_MODEL_PERIOD_AMOUNT_INPUT).send_keys(Keys.CONTROL + "a")
        self.find_element(self.LOCATOR_MODEL_PERIOD_AMOUNT_INPUT).send_keys(Keys.DELETE)
        self.find_and_enter(self.LOCATOR_MODEL_PERIOD_AMOUNT_INPUT, amount)

    def save_model_period(self):
        self.find_and_click(self.LOCATOR_MODEL_PERIOD_SAVE_BUTTON)
        time.sleep(7)

    def delete_model_period(self):
        self.find_and_click(self.LOCATOR_MODEL_PERIOD_DELETE_BUTTON)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)
        assert self.is_element_disappearing(self.LOCATOR_MODEL_PERIOD_START_YEAR, wait_display=False)

    @staticmethod
    def convert_date(date: list):
        month = {
            '01': 'января',
            '02': 'февраля',
            '03': 'марта',
            '04': 'апреля',
            '05': 'мая',
            '06': 'июня',
            '07': 'июля',
            '08': 'августа',
            '09': 'сентября',
            '10': 'октября',
            '11': 'ноября',
            '12': 'декабря'
        }
        converted_date = f'{date[0]} {month[date[1]]} {date[2]}'
        return converted_date

    def add_tag(self, tag_name: str):
        self.find_and_enter(self.LOCATOR_MODEL_SEARCH_TAG_INPUT, tag_name)
        found_value_locator = self.dropdown_value_locator_creator(tag_name)
        try:
            self.find_and_click(found_value_locator, time=3)
        except TimeoutException:
            self.find_and_click(self.LOCATOR_ADD_TAG_BUTTON)
        self.find_element(self.model_tag_locator_creator(tag_name))
        time.sleep(3)

    def open_tag(self, tag_name):
        tag_locator = self.model_tag_locator_creator(tag_name)
        self.find_and_click(tag_locator)
        title_text = self.get_element_text(self.modal.LOCATOR_MODAL_TITLE)
        assert title_text == f'Информация о теге: {tag_name}', "Некорректный заголовок окна тега"

    def delete_tag(self, tag_name):
        tag_locator = self.model_tag_locator_creator(tag_name)
        tag_xpath = tag_locator[1]
        tag_xpath = tag_xpath + "//fa-icon[@icon='faLightTimes']"
        delete_icon_locator = (By.XPATH, tag_xpath)
        self.find_and_click(delete_icon_locator)
        assert self.is_element_disappearing(tag_locator, wait_display=False), f'тег {tag_name} не исчезает из списка тегов'

    def close_tag_modal(self):
        self.find_and_click(self.modal.LOCATOR_CLOSE_MODAL_BUTTON)
