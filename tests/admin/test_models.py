import allure
import pytest
import time
from variables import PkmVars as Vars
from pages.model_po import ModelPage
from pages.table_po import TablePage
from pages.object_po import ObjectPage
from conditions.clean_factory import ModelNodeCreator, ClassNodeCreator, FormulaEntityCreator, DatasetCreator
from pages.components.modals import TagModal


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление моделями')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user3',
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
        model_page.tree.wait_selected_node_name(new_model_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени модели на странице модели'):
        model_page.wait_page_title(new_model_name)

    with allure.step('Проверить отображение обновленного имени модели в дереве'):
        assert model_page.tree.get_selected_node_name() == new_model_name

    with allure.step(f'Переименовать модель "{new_model_name}" на "{model_name}" в дереве'):
        model_page.tree.rename_node(new_model_name, model_name)

    with allure.step(f'Проверить изменение названия модели на странице модели'):
        model_page.wait_page_title(model_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени модели на странице модели'):
        model_page.wait_page_title(model_name)

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
        expected = [{'name': dataset_2, 'is_default': True}, {'name': dataset_1, 'is_default': False}]
        actual = model_page.get_model_datasets()
        assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

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
        assert api_datasets == ui_datasets, 'Некорректная сортировка по умолчанию'

    with allure.step(f'Проверить сортировку наборов данных по дате (ASC)'):
        ui_datasets = model_page.get_model_datasets('По дате создания', 'ASC')
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', False)
        assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

    with allure.step(f'Проверить сортировку наборов данных по дате (DESC)'):
        ui_datasets = model_page.get_model_datasets('По дате создания', 'DESC')
        api_datasets = api.get_datasets_names(model_uuid, 'createdAt', True)
        assert api_datasets == ui_datasets, 'Отсортированные наборы данных UI и API не совпадают'

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
            if dataset.get('name') == dataset_3:
                dataset['is_default'] = True

    with allure.step(f'Проверить корректное отображение наборов данных в списке'):
        expected = api_datasets
        actual = model_page.get_model_datasets()
        assert actual == expected, 'Актуальные наборы данных не совпадают с ожидаемыми'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить сортировку наборов данных по дате (DESC) по умолчанию'):
        api_datasets = api.get_datasets_names(model_uuid, group_value='createdAt', reverse=True)
        ui_datasets = model_page.get_model_datasets()
        assert api_datasets == ui_datasets, 'Некорректная сортировка по умолчанию'


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление временными интервалами модели')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user3',
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
        actual_period_data = model_page.get_model_period_data()
        expected_period_data = {
            "period_type": 'День',
            'period_start_value': '.'.join(expected_date),
            'period_start_year': None,
            'period_amount': '1',
            'last_period': model_page.convert_date(expected_date)
        }
        assert actual_period_data == expected_period_data

    with allure.step(f'Указать количество периодов {days_amount_period}'):
        model_page.set_period_amount(days_amount_period)

    with allure.step(f'Проверить что временной интервал пересчитан правильно'):
        expected_period_data = {
            "period_type": 'День',
            'period_start_value': '.'.join(expected_date),
            'period_start_year': None,
            'period_amount': days_amount_period,
            'last_period': model_page.convert_date(model_api.get_feature_date(expected_date, int(days_amount_period) - 1))
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
            'last_period': model_page.convert_date(model_api.get_feature_date(expected_date, int(days_amount_period) - 1))
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
            'period_amount': '1',
            'last_period': f'{current_mounth} {current_year}'.lower()
        }
        assert model_page.get_model_period_data() == expected_period_data

    with allure.step(f'Указать количество периодов {mounth_amount_period}'):
        model_page.set_period_amount(mounth_amount_period)

    expected_period_data['period_amount'] = mounth_amount_period
    feature_month = model_api.get_feature_month([today[1], today[2]], int(mounth_amount_period))
    expected_period_data['last_period'] = f'{model_api.get_mounth_name_by_number(feature_month[0])} {feature_month[1]}'.lower()

    with allure.step(f'Проверить корректное заполнение полей временного интервала'):
        actual_period_data = model_page.get_model_period_data()
        assert actual_period_data == expected_period_data

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
            'period_amount': '1',
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

    with allure.step(f'Удалить тег {tag_1}'):
        model_page.delete_tag(tag_1)

    with allure.step(f'Проверить, что в списке тегов модели отображается только тег {tag_2}'):
        assert model_page.get_model_tags() == [tag_2]

    with allure.step(f'Открыть тег {tag_2}'):
        model_page.open_tag(tag_2)

    with allure.step(f'Проверить что в окне связанных моделей тега отображаются все связанные модели включая текущую'):
        api_tag_models = model_api.get_models_names_by_tag(tag_2)
        ui_tag_models = tag_modal.get_linked_models()
        assert model_name in ui_tag_models, f'Модель {model_name} отсутствует в списке моделей тега'
        assert model_page.compare_lists(api_tag_models, ui_tag_models), "Некорректный список моделей"

    with allure.step(f'Закрыть модальное окно тега'):
        model_page.close_tag_modal()

    with allure.step(f'Удалить тег {tag_2}'):
        model_page.delete_tag(tag_2)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение пустого списка тегов модели'):
        assert model_page.get_model_tags() is None, 'Некорректный список тегов'


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление объектами модели')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user2',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление объектами модели'
    })])


def test_admin_model_objects_control(parametrized_login_admin_driver, parameters):
    object_page = ObjectPage(parametrized_login_admin_driver)
    model_api = object_page.api_creator.get_api_models()
    classes_api = object_page.api_creator.get_api_classes()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    src_class_name = 'Для связи объектов (источник)'
    dst_class_name = 'Для связи объектов (приемник)'
    indicator_name = 'Показатель_1'
    relation_name = 'Связь классов'
    object_1_name = original_object_1_name = 'Объект_1'
    object_2_name = 'Объект_2'

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве моделей через API'):
        models_test_folder_uuid = model_api.check_test_folder(test_folder_name)

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве классов через API'):
        classes_test_folder_uuid = classes_api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название класса_источника'):
        src_class_name = classes_api.create_unique_class_name(src_class_name)

    with allure.step(f'Создать класс источник через API'):
        src_class_data = classes_api.create_class_node(src_class_name, parent_uuid=classes_test_folder_uuid)

    with allure.step(f'Создать показатель класса источника через API'):
        classes_api.create_indicator_node(indicator_name, src_class_data.get('referenceUuid'), src_class_data.get('nodeUuid'), 'number')

    with allure.step(f'Определить уникальное название класса_приемника'):
        dst_class_name = classes_api.create_unique_class_name(dst_class_name)

    with allure.step(f'Создать класс приемник через API'):
        dst_class_data = classes_api.create_class_node(dst_class_name, parent_uuid=classes_test_folder_uuid)

    with allure.step(f'Создать показатель класса приемника через API'):
        classes_api.create_indicator_node(indicator_name, dst_class_data.get('referenceUuid'), dst_class_data.get('nodeUuid'), 'number')

    with allure.step(f'Определить уникальное название связи классов'):
        relation_name = classes_api.create_unique_class_name(relation_name)

    with allure.step(f'Создать связь классов {src_class_name} и {dst_class_name} через API'):
        classes_api.create_classes_relation_node(relation_name, src_class_data.get('nodeUuid'), src_class_data.get('referenceUuid'), dst_class_data.get('referenceUuid'))

    with allure.step(f'Определить уникальное название модели'):
        model_name = model_api.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME + '_объекты')

    with allure.step(f'Создать тестовую модель {model_name} в папке {test_folder_name} через API'):
        model = model_api.create_model_node(model_name, parent_uuid=models_test_folder_uuid)
        model_node_uuid = model.get('nodeUuid')

    with allure.step(f'Добавить модель {model_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ModelNodeCreator(parametrized_login_admin_driver, model_node_uuid, delete_anyway=True))

    with allure.step(f'Добавить класс {src_class_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ClassNodeCreator(parametrized_login_admin_driver, src_class_data.get('nodeUuid'), delete_anyway=True))

    with allure.step(f'Добавить класс {dst_class_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ClassNodeCreator(parametrized_login_admin_driver, dst_class_data.get('nodeUuid'), delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        object_page.tree.expand_node(test_folder_name)

    with allure.step(f'Создать объект {object_1_name} класса {src_class_name} в модели {model_name}'):
        object_1_data = object_page.create_object(object_1_name, model_name, src_class_name)

    with allure.step(f'Проверить заполнение созданного объекта данными по умолчанию'):
        expected_data = {
            'object_name': object_1_name,
            'description': None,
            'object_class': src_class_name,
            'relations': [[src_class_name, relation_name, dst_class_name]]
        }
        assert object_1_data == expected_data, 'Объект заполнен некорректными данными'

    with allure.step(f'Создать объект {object_2_name} класса {dst_class_name} в модели {model_name}'):
        object_2_data = object_page.create_object(object_2_name, model_name, dst_class_name)

    with allure.step(f'Проверить заполнение созданного объекта данными по умолчанию'):
        expected_data = {
            'object_name': object_2_name,
            'description': None,
            'object_class': dst_class_name,
            'relations': [[src_class_name, relation_name, dst_class_name]]
        }
        assert object_2_data == expected_data, 'Объект заполнен некорректными данными'

    with allure.step(f'Создать связь объектов {object_1_name} и {object_2_name}'):
        object_relation = object_page.create_object_relation(src_class_name, relation_name, dst_class_name, object_1_name)
        print('1')
        time.sleep(1)


    with allure.step(f'Открыть объект {object_1_name} через дерево'):
        object_page.tree.select_node(object_1_name)
        print('2')
        time.sleep(1)


    with allure.step(f'Проверить отображение коректных связей на странице объекта'):
        actual_relations = object_page.get_object_relations()
        expected_relations = [[src_class_name, relation_name, dst_class_name], object_relation]
        print('3')
        time.sleep(1)


        assert actual_relations == expected_relations, "актуальные связи не совпадают с ожидаемыми"
        print('4')
        time.sleep(1)

    with allure.step(f'Переименовать объект {object_1_name} на странице объекта'):
        object_1_name += '_ред'
        object_page.rename_title(object_1_name)
        print('5')
        time.sleep(1)

    with allure.step(f'Проверить изменение названия объекта в дереве'):
        object_page.wait_until_text_in_element(object_page.tree.LOCATOR_SELECTED_NODE, object_1_name)
        print('6')
        time.sleep(1)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()
        print('7')


    with allure.step(f'Проверить отображение актуального названия объекта на странице объекта'):
        object_page.wait_page_title(object_1_name)
        print('8')


    with allure.step(f'Проверить отображение актуального названия объекта в дереве'):
        object_page.wait_until_text_in_element(object_page.tree.LOCATOR_SELECTED_NODE, object_1_name)
        print('9')


    with allure.step(f'Переименовать объект {object_1_name} в дереве'):
        object_page.tree.rename_node(object_1_name, f'{object_1_name}_2')
        object_1_name += '_2'
        print('10')


    with allure.step(f'Проверить отображение актуального названия объекта на странице объекта'):
        object_page.wait_page_title(object_1_name)
        print('11')


    with allure.step(f'Открыть объект {object_2_name} через дерево'):
        object_page.tree.select_node(object_2_name)
        print('12')


    with allure.step(f'Проверить отображение коректных связей на странице объекта'):
        actual_relations = object_page.get_object_relations()
        object_relation[0] = object_1_name
        expected_relations = [[src_class_name, relation_name, dst_class_name], object_relation]

        assert actual_relations == expected_relations, "актуальные связи не совпадают с ожидаемыми"

        print('13')


    with allure.step(f'Удалить связь объектов {object_1_name} и {object_2_name}'):
        object_page.delete_relation(object_1_name, relation_name, object_2_name)
        print('14')


    with allure.step(f'Открыть объект {object_1_name} через дерево'):
        object_page.tree.select_node(object_1_name)
        print('15')
        time.sleep(1)

    with allure.step(f'Проверить отображение коректных связей на странице объекта'):
        actual_relations = object_page.get_object_relations()
        expected_relations = [[src_class_name, relation_name, dst_class_name]]
        assert actual_relations == expected_relations, "Некорректный список связей"
        print('16')
        time.sleep(1)

    with allure.step(f'Удалить объект {object_1_name}'):
        object_page.tree.delete_node(object_1_name, 'Объект', parent_node_name=model_name)
        print('17')


    with allure.step(f'Удалить объект {object_2_name}'):
        object_page.tree.delete_node(object_2_name, 'Объект', parent_node_name=model_name)
        print('18')


    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()
        print('19')


    with allure.step(f'Развернуть папку {test_folder_name}'):
        object_page.tree.expand_node(test_folder_name)
        print('20')


    with allure.step(f'Проверить отсутствие удаленных объектов модели {model_name} в дереве'):
        actual_objects = object_page.tree.get_node_children_names(model_name)
        assert actual_objects == []
        print('21')



@allure.feature('Интерфейс Администратора')
@allure.story('Дерево моделей')
@allure.title('Управление таблицами данных модели')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Модели',
        'name': 'Управление таблицами данных модели'
    })])
def test_admin_data_tables_control(parametrized_login_admin_driver, parameters):
    table_page = TablePage(parametrized_login_admin_driver)
    template_creator = table_page.api_creator.get_template_creator_api()
    model_api = table_page.api_creator.get_api_models()
    classes_api = table_page.api_creator.get_api_classes()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    table_name = 'Тестовая таблица'
    cells_fill_data = [
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_1', 'value': '200'},
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_2', 'value': '33'},
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_текстовый', 'value': 'Тест_тест'},   #Тестовое_значение
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_1', 'value': '500'},
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_2', 'value': '-150'},
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_текстовый', 'value': 'Тест123'},  #Тестовое_значение_2
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_1', 'value': '3000'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_2', 'value': '4500'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_текстовый', 'value': 'Test'},   #Привет
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_1', 'value': '-300'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_2', 'value': '-122'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_текстовый', 'value': 'Что-то'}    #Что-то
    ]
    cells_calc_data = [
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_3', 'value': '167.00'},
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_3', 'value': '650.00'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_3', 'value': '-1 500.00'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_3', 'value': '-178.00'}
    ]

    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве моделей через API'):
        models_test_folder_uuid = model_api.check_test_folder(test_folder_name)
        print('1')


    with allure.step(f'Проверить наличие тестовой папки "{test_folder_name}" в дереве классов через API'):
        classes_test_folder_uuid = classes_api.check_test_folder(test_folder_name)
        print('2')


    with allure.step(f'Создать шаблон для тестирования таблиц через API'):
        template_data = template_creator.create_table_template(classes_folder_uuid=classes_test_folder_uuid, models_folder_uuid=models_test_folder_uuid)
        print('3')


    class_name = template_data.get('class_data').get('name')
    class_node_uuid = template_data.get('class_data').get('nodeUuid')
    model_name = template_data.get('model_data').get('data')[0].get('name')
    model_node_uuid = template_data.get('model_data').get('nodeUuid')
    model_uuid = template_data.get('model_data').get('referenceUuid')
    dataset_1_name = template_data.get('dataset_1_data').get('name')
    dataset_1_uuid = template_data.get('dataset_1_data').get('uuid')
    dataset_2_name = template_data.get('dataset_2_data').get('name')
    dataset_2_uuid = template_data.get('dataset_2_data').get('uuid')
    formula_name = template_data.get('formula_data').get('name')
    formula_uuid = template_data.get('formula_data').get('uuid')

    with allure.step(f'Добавить набор данных {dataset_1_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(DatasetCreator(parametrized_login_admin_driver, dataset_1_uuid, delete_anyway=True))
        print('4')


    with allure.step(f'Добавить набор данных {dataset_2_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(DatasetCreator(parametrized_login_admin_driver, dataset_2_uuid, delete_anyway=True))
        print('5')


    with allure.step(f'Добавить модель {model_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ModelNodeCreator(parametrized_login_admin_driver, model_node_uuid, delete_anyway=True))
        print('6')


    with allure.step(f'Добавить формулу {formula_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(FormulaEntityCreator(parametrized_login_admin_driver, formula_uuid, delete_anyway=True))
        print('7')


    with allure.step(f'Добавить класс {class_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(ClassNodeCreator(parametrized_login_admin_driver, class_node_uuid, delete_anyway=True, force=[16, 17]))
        print('8')


    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        table_page.tree.expand_node(test_folder_name)
        print('9')


    with allure.step(f'Создать таблицу данных {table_name}'):
        table_page.create_data_table(model_name, table_name)
        print('10')


    with allure.step(f'Задать базовую структуру таблицы'):
        table_page.set_base_structure()
        print('11')


    # Удалить принудительное указание сущностей после исправления PKM-8966 и PKM-9767
#    table_page.set_entity_values('Столбцы', 'Наборы данных', [dataset_1_name, dataset_2_name])
#    table_page.set_entity_values('Столбцы', 'Показатели', ['Показатель_1', 'Показатель_2', 'Показатель_3', 'Показатель_текстовый'])

    # Удалить ребилд после исправления PKM-9312
#    model_api.rebuild_model(model_uuid)

    with allure.step(f'Переключиться в режим просмотра таблицы'):
        table_page.switch_table_page_type('Таблица')
        print('12')


    with allure.step(f'Проверить отображение всех объектов в качестве строк таблицы'):
        actual_names = table_page.get_table_rows_titles(names_only=True)
        expected_names = ['Объект_1', 'Объект_2']
        assert actual_names == expected_names, 'Фактические объекты не совпадают с ожидаемыми'
        print('13')


    with allure.step(f'Проверить отображение всех наборов данных и показателей в качестве столбцов таблицы'):
        actual_names = table_page.get_table_cols_titles(names_only=True)
        expected_names = ['Набор_1', 'Набор_2', 'Показатель_1', 'Показатель_2', 'Показатель_3', 'Показатель_текстовый', 'Показатель_1', 'Показатель_2', 'Показатель_3', 'Показатель_текстовый']
        assert actual_names == expected_names, 'Фактические объекты не совпадают с ожидаемыми'
        print('14')


    '''
    expected_data = [
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_3', 'value': '0.00'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_3', 'value': '0.00'},
        {'object_name': 'Объект_1', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_3', 'value': '0.00'},
        {'object_name': 'Объект_2', 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_3', 'value': '0.00'}
    ]
    with allure.step(f'Проверить расчет показателей созданных объектов по формуле'):
        table_page.wait_cells_value(expected_data)
    '''

    with allure.step(f'Проверить что ячейки таблицы не заполнены'):
        actual_data = table_page.get_table_data()
        assert actual_data == [], 'Таблица заполнена'
        print('15')


    with allure.step(f'Заполнить ячейки тестовыми данными'):
        table_page.fill_cells(cells_fill_data)
        print('16')


    with allure.step(f'Проверить расчет всех ячеек с показателями по формуле'):
        table_page.wait_cells_value(cells_calc_data)
        print('17')


#    with allure.step(f'Проверить корректное отображение значений всех ячеек в таблице'):
#        expected_cells_data = cells_fill_data + cells_calc_data
#        actual_cells_data = table_page.get_table_data()
#        table_page.compare_dicts_lists(actual_cells_data, expected_cells_data)
#        print('18')


    new_table_name = table_name + '_переименованная'
    
    with allure.step(f'Переименовать таблицу "{table_name}" на "{new_table_name}" на странице таблицы'):
        table_page.rename_title(new_table_name)
        print('19')


    with allure.step(f'Проверить изменение названия таблицы в дереве'):
        table_page.tree.wait_selected_node_name(new_table_name, timeout=20)
        print('20')


    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()
        print('21')


    with allure.step(f'Проверить отображение измененного названия таблицы в дереве'):
        table_page.tree.wait_selected_node_name(new_table_name, timeout=20)
        print('22')


    with allure.step(f'Проверить отображение измененного названия таблицы на странице таблицы'):
        table_page.wait_page_title(new_table_name, timeout=20)
        print('23')


#    with allure.step(f'Проверить корректное отображение значений всех ячеек в таблице'):
#        actual_cells_data = table_page.get_table_data()
#        table_page.compare_dicts_lists(actual_cells_data, expected_cells_data)
#        print('24')


    with allure.step(f'Переключиться в режим конструктора таблицы'):
        table_page.switch_table_page_type('Конструктор')
        print('25')

    with allure.step(f'Очистить структуру таблицы'):
        table_page.clear_structure()
        print('26')

    with allure.step(f'Задать структуру таблицы c объектами класса "{class_name}"'):
        table_page.set_class_objects_structure(class_name)
        print('27')

    # Удалить принудительное указание сущностей после исправления PKM-8966 и PKM-9767
#    table_page.set_entity_values('Столбцы', 'Наборы данных', [dataset_1_name, dataset_2_name])
#    table_page.set_entity_values('Столбцы', 'Показатели', ['Показатель_1', 'Показатель_2', 'Показатель_3', 'Показатель_текстовый'])
#    print('28')

    with allure.step(f'Переключиться в режим настройки таблицы'):
        table_page.switch_table_page_type('Настройки')
        print('29')

    with allure.step(f'Разрешить добавление объектов'):
        table_page.enable_objects_adding()
        print('30')

    with allure.step(f'Переключиться в режим просмотра таблицы'):
        table_page.switch_table_page_type('Таблица')
        print('31')

    table_object_1_name = 'Из таблицы 1'
    table_object_2_name = 'Из таблицы 2'
    print('32')

    with allure.step(f'Добавить объект "{table_object_1_name}" в таблицу'):
        table_page.add_table_object(table_object_1_name)
        print('33')

    with allure.step(f'Проверить отображение объекта "{table_object_1_name}" в дереве'):
        assert table_page.tree.wait_child_node(model_name, table_object_1_name), f'Объект {table_object_1_name} не отображается в дереве'
        print('34')

    with allure.step(f'Добавить объект "{table_object_2_name}" в таблицу'):
        table_page.add_table_object(table_object_2_name)
        print('35')

    with allure.step(f'Проверить отображение объекта "{table_object_1_name}" в дереве'):
        assert table_page.tree.wait_child_node(model_name, table_object_2_name), f'Объект {table_object_2_name} не отображается в дереве'
        print('36')

#    with allure.step(f'Проверить корректное отображение значений всех ячеек в таблице (включая вновь созданные объекты)'):
        # new_expected_cells_data = expected_cells_data + new_objects_data
#        actual_cells_data = table_page.get_table_data()
#        table_page.compare_dicts_lists(actual_cells_data, expected_cells_data)
#        print('37')

    incorrect_data = [
        {'object_name': table_object_1_name, 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_1',
         'value': 'abd'},
        {'object_name': table_object_1_name, 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_2',
         'value': 'def'}
    ]

    new_cells_fill_data = [
        {'object_name': table_object_1_name, 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_текстовый',
         'value': '100500'},
        {'object_name': table_object_2_name, 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_1', 'value': '2777.88'},
        {'object_name': table_object_2_name, 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_2', 'value': '1666.55'},
        {'object_name': table_object_2_name, 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_текстовый',
         'value': 'Что-то'}
    ]
    new_cells_calc_data = [
        {'object_name': table_object_2_name, 'dataset_name': 'Набор_2', 'indicator_name': 'Показатель_3', 'value': '1 111.33'},
        {'object_name': table_object_1_name, 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_1', 'value': ''},
        {'object_name': table_object_1_name, 'dataset_name': 'Набор_1', 'indicator_name': 'Показатель_2', 'value': ''}
    ]
    with allure.step(f'Заполнить ячейки вновь созданных объектов тестовыми данными'):
        table_page.fill_cells(new_cells_fill_data)
        print('38')

    with allure.step(f'Заполнить ячейки вновь созданных объектов некорректными тестовыми данными'):
        table_page.fill_cells(incorrect_data)
        print('39')

    with allure.step(f'Проверить расчет всех ячеек с показателями по формуле'):
        table_page.wait_cells_value(new_cells_calc_data)
        new_cells_calc_data.pop(2)
        new_cells_calc_data.pop(1)
        print('40')

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()
        print('41')

#    with allure.step(f'Проверить корректное отображение значений всех ячеек в таблице'):
#        actual_cells_data = table_page.get_table_data()
#        expected_cells_data = expected_cells_data + new_cells_fill_data + new_cells_calc_data
#        table_page.compare_dicts_lists(actual_cells_data, expected_cells_data)
#        print('42')

    with allure.step(f'Удалить таблицу {new_table_name}'):
        table_page.tree.delete_node(new_table_name, 'Таблица', parent_node_name=model_name)
        print('43')

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()
        print('44')

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        table_page.tree.expand_node(test_folder_name)
        print('45')

    with allure.step(f'Проверить отсутствие удаленной таблицы {new_table_name} в дереве'):
        assert new_table_name not in table_page.tree.get_node_children_names(model_name)
        print('46-конец')
