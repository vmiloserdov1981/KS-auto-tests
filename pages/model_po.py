from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
from core import antistale
from selenium.webdriver.common.by import By
import datetime
import allure


class ModelPage(EntityPage):
    DIMENSIONS_LIST_NAME = ' Измерения '
    DATASETS_LIST_NAME = 'Наборы данных'
    SOLVERS_LIST_NAME = 'Поиск решения'
    TAGS_LIST_NAME = 'Теги'

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = Tree(driver)
        self.modal = Modals(driver)

    @staticmethod
    def datasets_list_value_locator_creator(dataset_name):
        locator = (By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{ModelPage.DATASETS_LIST_NAME}'] ]//div[contains(@class, 'list-item ') and ./div[.='{dataset_name}']]")
        return locator

    def get_model_page_data(self) -> dict:
        '''
        data = {
            'model_name': self.get_entity_page_title(return_raw=True),
            'changes': self.get_change_data(),
            'datasets': self.get_model_datasets(),
            'dimensions': self.get_model_dimensions(),
            'time_period': self.get_model_period_type(),
            'period_amount': self.get_model_period_amount(),
            'last_period': self.get_model_last_period(),
            'solver_values': self.get_model_solvers(),
            'tags': self.get_model_tags()
        }
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
        data = self.get_page_data_by_template(template)
        return data

    def create_model(self, parent_node, model_name):
        with allure.step(f'Создать модель {model_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_node))
            self.find_and_click(self.tree.context_option_locator_creator('Создать модель'))
            self.tree.modal.enter_and_save(model_name)
        api = self.api_creator.get_api_models()
        actual_date = f'{".".join(api.get_utc_date())}'
        actual_time = api.get_utc_time()
        with allure.step(f'Проверить отображение модели {model_name} в дереве моделей выбранной'):
            #assert self.tree.get_selected_node_name() == model_name, f'В дереве не выбрана нода {model_name}'
            pass
        with allure.step(f'Проверить переход на страницу вновь соданной модели'):
            assert self.get_entity_page_title() == model_name.upper(), f'Некорректный заголовок на странице модели'
        with allure.step(f'Проверить заполнение созданной модели данными по умолчанию'):
            actual = self.get_model_page_data()
            expected = {
                'model_name': model_name,
                'changes': {
                    'created_at': f'{actual_date} {actual_time}',
                    'created_by': self.driver.current_user.name,
                    'updated_at': f'{actual_date} {actual_time}',
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
            try:
                self.compare_dicts(actual, expected)
            except AssertionError:
                actual_datetime = datetime.datetime(int(actual_date.split('.')[2]), int(actual_date.split('.')[1]), int(actual_date.split('.')[0]), int(actual_time.split(':')[0]), int(actual_time.split(':')[1]))
                interval = datetime.timedelta(minutes=1)
                actual_datetime = str(actual_datetime + interval)
                actual_date = '.'.join(actual_datetime.split(' ')[0].split('-')[::-1])
                actual_time = actual_datetime.split(' ')[1][:-3]
                expected['changes'] = {
                    'created_at': f'{actual_date} {actual_time}',
                    'created_by': self.driver.current_user.name,
                    'updated_at': f'{actual_date} {actual_time}',
                    'updated_by': self.driver.current_user.name
                }
                self.compare_dicts(actual, expected)

    def get_model_dimensions(self, sort_value=None, sort_order=None):
        if sort_value and sort_order:
            self.sort_dimensions(sort_value, sort_order)
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME)
        return elements

    @antistale
    def get_model_datasets(self, sort_value=None, sort_order=None):
        if sort_value and sort_order:
            self.sort_datasets(sort_value, sort_order)

        names = self.get_list_elements_names(self.DATASETS_LIST_NAME)
        result = []

        if names:
            for name in names:
                if '\n(По умолчанию)' not in name:
                    value = {'name': name, 'is_default': False}
                else:
                    value = {'name': name.split('\n')[0], 'is_default': True}
                result.append(value)

        return result if result != [] else None

    def get_model_period_type(self):
        value = self.get_element_text((By.XPATH, "//pkm-dropdown[@formcontrolname='periodType']//div[contains(@class, 'display-value-text')]"), ignore_error=True, time=2)
        return value

    def get_model_period_amount(self):
        value = self.get_input_value(self.input_locator_creator('amount'), return_empty=False)
        return value

    def get_model_last_period(self):
        value = self.get_input_value(self.input_locator_creator('result'), return_empty=False)
        return value

    def get_model_solvers(self):
        elements = self.get_list_elements_names(self.SOLVERS_LIST_NAME)
        return elements

    def get_model_tags(self):
        elements = [element.text for element in self.elements_generator((By.XPATH, f"//div[@class='list' and .//div[@class='title' and .='{self.TAGS_LIST_NAME}'] ]//div[contains(@class, 'tag-item')]"), time=1)]
        return elements if elements != [] else None

    def create_dataset(self, dataset_name, is_default=None):
        self.find_and_click(self.add_list_element_button_creator(self.DATASETS_LIST_NAME, without_spaces=True))
        if is_default is None:
            assert self.is_element_disappearing(self.modal.checkbox_locator_creator('По умолчанию'), wait_display=False), 'Отображается чекбокс выбора по умолчанию'
        elif is_default is True:
            self.modal.check_checkbox('По умолчанию')
        elif is_default is False:
            self.modal.uncheck_checkbox('По умолчанию')
        self.modal.enter_and_save(dataset_name)
        value_locator = self.datasets_list_value_locator_creator(dataset_name)
        row = self.find_element(value_locator)
        if is_default is True or is_default is None:
            assert row.text == f'{dataset_name}\n(По умолчанию)'
        elif is_default is False:
            assert row.text == dataset_name

    def sort_datasets(self, sort_type, sort_order):
        self.find_and_click(self.list_sort_button_creator(self.DATASETS_LIST_NAME, without_spaces=True))
        self.find_and_click(self.sort_type_button_creator(sort_type))
        sort_order_icon_locator = self.sort_order_icon_creator(sort_type)

        if sort_order == 'ASC':
            if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-down':
                self.find_and_click(self.sort_type_button_creator(sort_type))
                if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-down':
                    raise AssertionError('Не удалось установить сортировку по возрастанию')

        elif sort_order == 'DESC':
            if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-up':
                self.find_and_click(self.sort_type_button_creator(sort_type))
                if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-up':
                    raise AssertionError('Не удалось установить сортировку по убыванию')

        self.find_and_click(self.list_sort_button_creator(self.DATASETS_LIST_NAME, without_spaces=True))

    def sort_dimensions(self, sort_type, sort_order):
        self.find_and_click(self.list_sort_button_creator(self.DIMENSIONS_LIST_NAME, without_spaces=True))
        self.find_and_click(self.sort_type_button_creator(sort_type))
        sort_order_icon_locator = self.sort_order_icon_creator(sort_type)

        if sort_order == 'ASC':
            if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-down':
                self.find_and_click(self.sort_type_button_creator(sort_type))
                if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-down':
                    raise AssertionError('Не удалось установить сортировку по возрастанию')

        elif sort_order == 'DESC':
            if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-up':
                self.find_and_click(self.sort_type_button_creator(sort_type))
                if self.find_element(sort_order_icon_locator).get_attribute('ng-reflect-icon') != 'arrow-up':
                    raise AssertionError('Не удалось установить сортировку по убыванию')

        self.find_and_click(self.list_sort_button_creator(self.DIMENSIONS_LIST_NAME, without_spaces=True))

    def rename_dataset(self, dataset_name, dataset_new_name, is_default=None):
        dataset_locator = self.datasets_list_value_locator_creator(dataset_name)
        name = self.get_element_text(dataset_locator)
        if '\n(По умолчанию)' in name:
            actual_default = True
        else:
            actual_default = False

        self.hover_over_element(dataset_locator)
        rename_button_locator = (By.XPATH, f"{self.datasets_list_value_locator_creator(dataset_name)[1]}//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='pencil-alt']")
        self.find_and_click(rename_button_locator)
        assert self.modal.is_input_checked(self.modal.checkbox_locator_creator('По умолчанию')) == actual_default, 'Состояние чекбокса по умолчанию не соответствыует названию набора данных'

        if is_default is True:
            self.modal.check_checkbox('По умолчанию')
        elif is_default is False:
            self.modal.uncheck_checkbox('По умолчанию')

        self.modal.enter_and_save(dataset_new_name, clear_input=True)

    def delete_dataset(self, dataset_name):
        dataset_locator = self.datasets_list_value_locator_creator(dataset_name)
        self.hover_over_element(dataset_locator)
        delete_button_locator = (By.XPATH, f"{self.datasets_list_value_locator_creator(dataset_name)[1]}//div[contains(@class, 'list-item-buttons')]//fa-icon[@icon='trash']")
        self.find_and_click(delete_button_locator)
        self.find_and_click(self.modal.LOCATOR_DELETE_BUTTON)

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

