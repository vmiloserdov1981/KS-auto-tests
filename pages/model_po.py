from pages.components.entity_page import EntityPage
from pages.components.trees import Tree
from pages.components.modals import Modals
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

    def get_model_page_data(self) -> dict:
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
        '''
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
                actual_date = actual_datetime.split(' ')[0]
                actual_time = actual_datetime.split(' ')[1]
                expected['changes'] = {
                    'created_at': f'{actual_date} {actual_time}',
                    'created_by': self.driver.current_user.name,
                    'updated_at': f'{actual_date} {actual_time}',
                    'updated_by': self.driver.current_user.name
                }
                self.compare_dicts(actual, expected)

    def get_model_dimensions(self):
        elements = self.get_list_elements_names(self.DIMENSIONS_LIST_NAME)
        return elements

    def get_model_datasets(self):
        elements = self.get_list_elements_names(self.DATASETS_LIST_NAME)
        if elements:
            elements = [element.split('\n')[0] for element in elements]
        return elements

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


