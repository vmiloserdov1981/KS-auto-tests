import allure
import pytest
from variables import PkmVars as Vars
from pages.model_po import ModelPage
from conditions.clean_factory import ModelNodeCreator
from pages.components.modals import TagModal


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
        'name': 'Управление наборами данных модели'
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
        #PKM-4552
        #assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректное отображение наборов данных в списке'):
        expected = [{'name': dataset_2, 'is_default': True}, {'name': dataset_1, 'is_default': False}]
        actual = model_page.get_model_datasets()
        assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

    with allure.step(f'Создать новый набор данных "{dataset_3}"'):
        model_page.create_dataset(dataset_3, is_default=False)

    with allure.step(f'Проверить сортировку наборов данных по дате (DESC) по умолчанию'):
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', True)
        ui_datasets = model_page.get_model_datasets()
        # PKM-4554
        # assert api_datasets == ui_datasets, 'Некорректная сортировка по умолчанию'

    with allure.step(f'Проверить сортировку наборов данных по дате (ASC)'):
        ui_datasets = model_page.get_model_datasets('По дате создания', 'ASC')
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', False)
        # PKM-4554
        #assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

    with allure.step(f'Проверить сортировку наборов данных по дате (DESC)'):
        ui_datasets = model_page.get_model_datasets('По дате создания', 'DESC')
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', True)
        # PKM-4554
        #assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'


    with allure.step(f'Проверить сортировку наборов данных по алфавиту (ASC)'):
        ui_datasets = model_page.get_model_datasets('По алфавиту', 'ASC')
        api_datasets = api.get_datasets_names(model_uuid, 'name', False)
        assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

    with allure.step(f'Проверить сортировку наборов данных по алфавиту (DESC)'):
        ui_datasets = model_page.get_model_datasets('По алфавиту', 'DESC')
        api_datasets = api.get_datasets_names(model_uuid, 'name', True)
        assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

    with allure.step(f'Переименовать набор данных {dataset_1}'):
        dataset_1_new = f'{dataset_1}_(переименовано)'
        model_page.rename_dataset(dataset_1, dataset_1_new)
        for dataset in api_datasets:
            if dataset.get('name') == dataset_1:
                dataset['name'] = dataset_1_new
                break

    with allure.step(f'Удалить набор данных {dataset_2}'):
        model_page.delete_dataset(dataset_2)
        for dataset in api_datasets:
            if dataset.get('name') == dataset_2:
                api_datasets.remove(dataset)
                break

    with allure.step(f'Проверить корректное отображение наборов данных в списке'):
        expected = api_datasets
        actual = model_page.get_model_datasets()
        assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить сортировку наборов данных по дате (DESC) по умолчанию'):
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', True)
        ui_datasets = model_page.get_model_datasets()
        assert api_datasets == ui_datasets, 'Некорректная сортировка по умолчанию'
        

@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление измерениями модели')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление измерениями модели'
    })])
def test_admin_dimensions_control(parametrized_login_admin_driver, parameters):
    model_page = ModelPage(parametrized_login_admin_driver)
    model_api = model_page.api_creator.get_api_models()
    dictionary_api = model_page.api_creator.get_api_dictionaries()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    dimension_1 = {'name': 'Типы данных (автотест)', 'elements': ['Числовые', 'Текстовые']}
    dimension_2 = {'name': 'Функциональность данных (автотест)', 'elements': ['Базовая', 'Расширенная']}
    dimension_3 = {'name': 'Виды данных (автотест)', 'elements': ['Статистические', 'Эмпирические']}

    with allure.step(f'Проверить наличие тестовых справочников'):
        dictionary_api.check_test_dictionaries([dimension_1, dimension_2, dimension_3], parent_node_name=test_folder_name)

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве моделей через API'):
        test_folder_uuid = model_api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название модели'):
        model_name = model_api.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME + '_измерения')

    with allure.step(f'Создать тестовую модель {model_name} в папке {test_folder_name} через API'):
        model = model_api.create_model_node(model_name, parent_uuid=test_folder_uuid)
        model_node_uuid = model.get('nodeUuid')
        model_uuid = model.get('referenceUuid')

    with allure.step(f'Добавить модель {model_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ModelNodeCreator(parametrized_login_admin_driver, model_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        model_page.tree.expand_node(test_folder_name)

    with allure.step(f'Перейти на страницу модели {model_name}'):
        model_page.tree.select_node(model_name)

    with allure.step(f'Добавить измерение {dimension_1.get("name")} в модель'):
        model_page.add_dimension(dimension_1.get("name"))

    with allure.step(f'Добавить измерение {dimension_2.get("name")} в модель'):
        model_page.add_dimension(dimension_2.get("name"))

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Добавить измерение {dimension_3.get("name")} в модель'):
        model_page.add_dimension(dimension_3.get("name"))

    with allure.step(f'Проверить отображение всех добавленных измерений в списке измерений'):
        ui_dimensions = model_page.get_model_dimensions()
        added_dimensions = [dimension_1.get('name'), dimension_2.get('name'), dimension_3.get('name')]
        assert model_page.compare_lists(ui_dimensions, added_dimensions), 'Измерения в списке не совпадают из созданными'

    with allure.step(f'Проверить сортировку измерений по дате (DESC) по умолчанию'):
        ui_dimensions = model_page.get_model_dimensions()
        api_dimensions = model_api.get_model_dictionaries_names(model_uuid, group_value='createdAt', reverse=True)
        assert api_dimensions == ui_dimensions, 'Некорректная сортировка по умолчанию'

    with allure.step(f'Проверить сортировку измерений по дате (ASC)'):
        ui_dimensions = model_page.get_model_dimensions('По дате создания', 'ASC')
        api_dimensions = model_api.get_model_dictionaries_names(model_uuid, 'createdAt', False)
        assert ui_dimensions == api_dimensions

    with allure.step(f'Проверить сортировку измерений по дате (DESC)'):
        ui_dimensions = model_page.get_model_dimensions('По дате создания', 'DESC')
        api_dimensions = model_api.get_model_dictionaries_names(model_uuid, 'createdAt', True)
        assert ui_dimensions == api_dimensions

    with allure.step(f'Проверить сортировку измерений по алфавиту (ASC)'):
        ui_dimensions = model_page.get_model_dimensions('По алфавиту', 'ASC')
        api_dimensions = model_api.get_model_dictionaries_names(model_uuid, 'name', False)
        assert ui_dimensions == api_dimensions

    with allure.step(f'Проверить сортировку измерений по алфавиту (DESC)'):
        ui_dimensions = model_page.get_model_dimensions('По алфавиту', 'DESC')
        api_dimensions = model_api.get_model_dictionaries_names(model_uuid, 'name', True)
        assert ui_dimensions == api_dimensions

    with allure.step(f'Удалить измерение {dimension_2.get("name")}'):
        model_page.delete_dimension(dimension_2.get("name"))
        api_dimensions.remove(dimension_2.get("name"))

    with allure.step(f'Проверить корректное отображение измерений в списке'):
        expected = api_dimensions
        actual = model_page.get_model_dimensions()
        assert model_page.compare_lists(actual, expected)
        #Раскоментировать следующую строчку и удалить предыдущую после PKM-4693
        #assert actual == expected, 'Актуальные измерения не совпадают с ожидаемыми'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить сортировку измерений по дате (DESC) по умолчанию'):
        api_dimensions = model_api.get_model_dictionaries_names(model_uuid, group_value='createdAt', reverse=True)
        ui_dimensions = model_page.get_model_dimensions()
        assert api_dimensions == ui_dimensions, 'Некорректная сортировка по умолчанию'


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление временными интервалами модели')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление временными интервалами модели'
    })])
def test_admin_model_period_control(parametrized_login_admin_driver, parameters):
    model_page = ModelPage(parametrized_login_admin_driver)
    model_api = model_page.api_creator.get_api_models()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    today = model_api.get_utc_date()
    expected_date = model_api.get_utc_date()
    days_amount_period = '14'
    mounth_amount_period = '2'
    years_amount_period = '3'

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве моделей через API'):
        test_folder_uuid = model_api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название модели'):
        model_name = model_api.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME + '_временные_интервалы')

    with allure.step(f'Создать тестовую модель {model_name} в папке {test_folder_name} через API'):
        model = model_api.create_model_node(model_name, parent_uuid=test_folder_uuid)
        model_node_uuid = model.get('nodeUuid')

    with allure.step(f'Добавить модель {model_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ModelNodeCreator(parametrized_login_admin_driver, model_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        model_page.tree.expand_node(test_folder_name)

    with allure.step(f'Перейти на страницу модели {model_name}'):
        model_page.tree.select_node(model_name)

    with allure.step(f'Задать тип временного интервала "День"'):
        model_page.set_model_period_type('День')

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == {
            "period_type": 'День',
            'period_start_value': '.'.join(expected_date),
            'period_start_year': None,
            'period_amount': None,
            'last_period': '.'.join(expected_date)
        }

    with allure.step(f'Указать количество периодов {days_amount_period}'):
        model_page.set_period_amount(days_amount_period)

    with allure.step(f'Проверить что временной интервал пересчитан правильно'):
        expected_period_data = {
            "period_type": 'День',
            'period_start_value': '.'.join(expected_date),
            'period_start_year': None,
            'period_amount': days_amount_period,
            'last_period': '.'.join(model_api.get_feature_date(expected_date, int(days_amount_period) - 1))
        }
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Сохранить временной интервал'):
        model_page.save_model_period()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Изменить дату начала интервала на 25-е число текущего месяца'):
        model_page.set_start_period_day('25')

    with allure.step(f'Проверить что временной интервал пересчитан правильно'):
        expected_date[0] = '25'
        expected_period_data = {
            "period_type": 'День',
            'period_start_value': '.'.join(expected_date),
            'period_start_year': None,
            'period_amount': days_amount_period,
            'last_period': '.'.join(model_api.get_feature_date(expected_date, int(days_amount_period) - 1))
        }
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Сохранить временной интервал'):
        model_page.save_model_period()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data

    current_mounth = model_api.get_mounth_name_by_number(today[1])
    current_year = today[2]

    with allure.step(f'Задать тип временного интервала "Месяц"'):
        model_page.set_model_period_type('Месяц')

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        expected_period_data = {
            "period_type": 'Месяц',
            'period_start_value': current_mounth,
            'period_start_year': current_year,
            'period_amount': None,
            'last_period': f'{current_mounth} {current_year}'.lower()
        }
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Указать количество периодов {mounth_amount_period}'):
        model_page.set_period_amount(mounth_amount_period)

    expected_period_data['period_amount'] = mounth_amount_period
    feature_month = model_api.get_feature_month([today[1], today[2]], int(mounth_amount_period))
    expected_period_data['last_period'] = f'{model_api.get_mounth_name_by_number(feature_month[0])} {feature_month[1]}'.lower()

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Сохранить временной интервал'):
        model_page.save_model_period()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Задать тип временного интервала "Год"'):
        model_page.set_model_period_type('Год')

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        expected_period_data = {
            "period_type": 'Год',
            'period_start_value': None,
            'period_start_year': current_year,
            'period_amount': None,
            'last_period': current_year
        }
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Указать количество периодов {years_amount_period}'):
        model_page.set_period_amount(years_amount_period)

    expected_period_data['period_amount'] = years_amount_period
    expected_period_data['last_period'] = str(int(current_year) + int(years_amount_period) - 1)

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Сохранить временной интервал'):
        model_page.save_model_period()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Удалить временной интервал модели'):
        model_page.delete_model_period()

    with allure.step(f'Проверить очистку полей временного интервала'):
        expected_period_data = {
            "period_type": None,
            'period_start_value': None,
            'period_start_year': None,
            'period_amount': None,
            'last_period': None
        }
        assert model_page.get_model_period_data() == expected_period_data, 'Временной интервал модели не очищен'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить очистку полей временного интервала'):
        assert model_page.get_model_period_data() == expected_period_data


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление тегами модели')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление тегами модели'
    })])
def test_admin_model_tags_control(parametrized_login_admin_driver, parameters):
    model_page = ModelPage(parametrized_login_admin_driver)
    tag_modal = TagModal(parametrized_login_admin_driver)
    model_api = model_page.api_creator.get_api_models()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    tag_1 = 'Тестовый тег'
    tag_2 = 'Базовый тег'

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве моделей через API'):
        test_folder_uuid = model_api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название модели'):
        model_name = model_api.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME + '_теги')

    with allure.step(f'Создать тестовую модель {model_name} в папке {test_folder_name} через API'):
        model = model_api.create_model_node(model_name, parent_uuid=test_folder_uuid)
        model_node_uuid = model.get('nodeUuid')

    with allure.step(f'Добавить модель {model_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ModelNodeCreator(parametrized_login_admin_driver, model_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        model_page.tree.expand_node(test_folder_name)

    with allure.step(f'Перейти на страницу модели {model_name}'):
        model_page.tree.select_node(model_name)

    with allure.step(f'Добавить тег {tag_1}'):
        model_page.add_tag(tag_1)

    with allure.step(f'Открыть тег {tag_1}'):
        model_page.open_tag(tag_1)

    with allure.step(f'Проверить что в окне связанных моделей тега отображаются все связанные модели включая текущую'):
        api_tag_models = model_api.get_models_names_by_tag(tag_1)
        ui_tag_models = tag_modal.get_linked_models()
        assert model_name in ui_tag_models, f'Модель {model_name} отсутствует в списке моделей тега'
        assert model_page.compare_lists(api_tag_models, ui_tag_models), "Некорректный список моделей"

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить отображение корректного списка тегов модели'):
        assert model_page.compare_lists([tag_1], model_page.get_model_tags()), 'Некорректный список тегов'

    with allure.step(f'Добавить тег {tag_2}'):
        model_page.add_tag(tag_2)
