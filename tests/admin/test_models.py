import allure
import pytest
from variables import PkmVars as Vars
from pages.model_po import ModelPage
from conditions.clean_factory import ModelNodeCreator


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление моделями')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление моделями'
    })])
def test_admin_models_control(parametrized_login_admin_driver, parameters):
    model_page = ModelPage(parametrized_login_admin_driver)
    api = model_page.api_creator.get_api_models()

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве моделей'):
        model_page.tree.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Определить уникальное название модели'):
        model_name = api.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME)

    with allure.step(f'Создать модель {model_name} в папке {Vars.PKM_TEST_FOLDER_NAME}'):
        model_page.create_model(Vars.PKM_TEST_FOLDER_NAME, model_name)

    new_model_name = api.create_unique_model_name(f'{model_name}_измененная')

    with allure.step(f'Переименовать модель "{model_name}" на "{new_model_name}" на странице модели'):
        model_page.rename_title(new_model_name)

    with allure.step(f'Проверить изменение названия модели в дереве'):
        #model_page.wait_until_text_in_element(model_page.tree.LOCATOR_SELECTED_NODE, new_model_name)
        pass

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени модели на странице модели'):
        assert model_page.get_entity_page_title() == new_model_name.upper()

    with allure.step('Проверить отображение обновленного имени модели в дереве'):
        assert model_page.tree.get_selected_node_name() == new_model_name

    with allure.step(f'Переименовать модель "{new_model_name}" на "{model_name}" в дереве'):
        title_html = model_page.find_element(model_page.LOCATOR_ENTITY_PAGE_TITLE).get_attribute('innerHTML')
        model_page.tree.rename_node(new_model_name, model_name)

    with allure.step(f'Проверить изменение названия модели на странице модели'):
        assert model_page.get_entity_page_title(prev_title_html=title_html) == model_name.upper()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени модели на странице модели'):
        assert model_page.get_entity_page_title() == model_name.upper()

    with allure.step('Проверить отображение обновленного имени модели в дереве'):
        assert model_page.tree.get_selected_node_name() == model_name

    with allure.step(f'Удалить модель "{model_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве моделей'):
        model_page.tree.delete_node(model_name, 'Модель', parent_node_name=Vars.PKM_TEST_FOLDER_NAME)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить отсутствие модели "{model_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}"'):
        assert model_name not in model_page.tree.get_node_children_names(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Проверить отсутствие модели "{model_name}" в дереве моделей'):
        assert model_name not in api.get_models_names()


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление наборами данных')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление моделями'
    })])
def test_admin_datasets_control(parametrized_login_admin_driver, parameters):
    model_page = ModelPage(parametrized_login_admin_driver)
    api = model_page.api_creator.get_api_models()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    dataset_1 = 'Проверенные данные'
    dataset_2 = 'Непроверенные данные'
    dataset_3 = 'Требуют согласования'

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве моделей через API'):
        test_folder_uuid = api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название модели'):
        model_name = api.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME + '_НД')

    with allure.step(f'Создать тестовую модель {model_name} в папке {test_folder_name} через API'):
        model = api.create_model_node(model_name, parent_uuid=test_folder_uuid)
        model_node_uuid = model.get('nodeUuid')
        model_uuid = model.get('referenceUuid')

    with allure.step(f'Добавить модель {model_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ModelNodeCreator(parametrized_login_admin_driver, model_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        model_page.tree.expand_node(test_folder_name)

    with allure.step(f'Перейти на страницу модели {model_name}'):
        model_page.tree.select_node(model_name)

    with allure.step(f'Создать новый набор данных "{dataset_1}"'):
        model_page.create_dataset(dataset_1)

    with allure.step(f'Создать новый набор данных "{dataset_2}" по умолчанию'):
        model_page.create_dataset(dataset_2, is_default=True)

    with allure.step(f'Проверить корректное отображение наборов данных в списке'):
        expected = [{'name': dataset_1, 'is_default': False}, {'name': dataset_2, 'is_default': True}]
        actual = model_page.get_model_datasets()
        #assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректное отображение наборов данных в списке'):
        expected = [{'name': dataset_2, 'is_default': True}, {'name': dataset_1, 'is_default': False}]
        actual = model_page.get_model_datasets()
        assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

    with allure.step(f'Создать новый набор данных "{dataset_3}" по умолчанию'):
        model_page.create_dataset(dataset_3, is_default=False)

    with allure.step(f'Проверить сортировку наборов данных по алфавиту (ASC)'):
        ui_datasets = model_page.get_model_datasets('По алфавиту', 'ASC')
        api_datasets = api.get_datasets_names(model_uuid, 'name', False)
        assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

    with allure.step(f'Проверить сортировку наборов данных по алфавиту (DESC)'):
        ui_datasets = model_page.get_model_datasets('По алфавиту', 'DESC')
        api_datasets = api.get_datasets_names(model_uuid, 'name', True)
        assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

    with allure.step(f'Проверить сортировку наборов данных по дате (ASC)'):
        ui_datasets = model_page.get_model_datasets('По дате создания', 'ASC')
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', False)
        #assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'
