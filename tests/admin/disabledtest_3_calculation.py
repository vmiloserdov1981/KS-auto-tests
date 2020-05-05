from variables import PkmVars as Vars
from api.api import ApiClasses
from api.api import ApiModels
import allure
from pages.components.trees import Tree
from pages.class_po import ClassPage
from pages.class_po import IndicatorPage
from pages.models_po import ModelsPage
from pages.models_po import TableConstructor
from pages.models_po import TablePage
import time


@allure.feature('End-to-end')
@allure.story('Базовые вычисления')
@allure.title('Создание простого вычисления')
@allure.severity(allure.severity_level.CRITICAL)
def test_simple_calculation(driver_login):
    tree = Tree(driver_login, None, None, token=driver_login.token)
    api = ApiClasses(None, None, token=driver_login.token)
    api_model = ApiModels(None, None, token=driver_login.token)
    class_name = api.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
    ind_names = [f'{Vars.PKM_BASE_INDICATOR_NAME}_{i+1}' for i in range(3)]
    class_page = ClassPage(driver_login, None, None, token=driver_login.token)
    ind_page = IndicatorPage(driver_login, None, None, token=driver_login.token)
    formula_name = Vars.PKM_DEFAULT_FORMULA_NAME
    folder_name = Vars.PKM_TEST_FOLDER_NAME
    model_name = api_model.create_unique_model_name(Vars.PKM_BASE_MODEL_NAME)
    object_name_one = f"{Vars.PKM_BASE_OBJECT_NAME}_1"
    object_name_two = f"{Vars.PKM_BASE_OBJECT_NAME}_2"
    dataset_name_one = f"{Vars.PKM_BASE_DATASET_NAME}_1"
    dataset_name_two = f"{Vars.PKM_BASE_DATASET_NAME}_2"
    table_name = Vars.PKM_BASE_TABLE_NAME
    model_page = ModelsPage(driver_login, None, None, token=driver_login.token)
    constructor_page = TableConstructor(driver_login)
    table_page = TablePage(driver_login)

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step(f'Проверить наличие тестовой папки "{folder_name}" в корне'):
        tree.check_test_folder(folder_name)

    with allure.step(f'Создать новый класс в папке "{folder_name}"'):
        tree.create_class_in_folder(folder_name, class_name)

    with allure.step('Проверить переход на страницу вновь созданного класса'):
        class_page.check_page(class_name=class_name, save_test_data=False)

    class_uuid = class_page.get_uuid_from_url()

    with allure.step(f'Развернуть папку "{folder_name}"'):
        tree.expand_node(folder_name)

    with allure.step('Проверить отображение вновь созданного класса в дереве'):
        tree.check_node_in_tree(class_name, last=False)

    with allure.step(f'Создать новый показатель c именем "{ind_names[0]}" через дерево'):
        tree.create_indicator(class_name, ind_names[0])

    with allure.step(f'Проверить переход на страницу показателя "{ind_names[0]}"'):
        ind_page.check_page(ind_names[0], class_uuid)

    with allure.step(f'Развернуть класс "{class_name}"'):
        tree.expand_node(class_name)

    with allure.step(f'Проверить отображение вновь созданного показателя {ind_names[0]} активным в дереве'):
        tree.check_indicator_in_tree(ind_names[0], class_name, active=True)

    with allure.step(f'Создать новый показатель c именем "{ind_names[1]}" через дерево'):
        tree.create_indicator(class_name, ind_names[1])

    with allure.step(f'Проверить переход на страницу показателя "{ind_names[1]}"'):
        ind_page.check_page(ind_names[1], class_uuid)

    with allure.step(f'Проверить отображение вновь созданного показателя {ind_names[1]} активным в дереве'):
        tree.check_indicator_in_tree(ind_names[1], class_name, active=True)

    with allure.step(f'Перейти на страницу класса "{class_name}"'):
        tree.open_node(class_name)

    with allure.step(f'Создать новый показатель c именем "{ind_names[2]}" на странице класса'):
        class_page.add_indicator(ind_names[2])

    with allure.step(f'Проверить переход на страницу показателя "{ind_names[2]}"'):
        ind_page.check_page(ind_names[2], class_uuid)

    ind_3_uuid = ind_page.get_uuid_from_url()

    with allure.step(f'Проверить отображение вновь созданного показателя {ind_names[2]} активным в дереве'):
        tree.check_indicator_in_tree(ind_names[2], class_name, active=True)

    with allure.step(f'Создать формулу "{formula_name}"'):
        ind_page.create_formula(formula_name)

    with allure.step(f'Проверить наличие формулы "{formula_name} в api"'):
        assert class_page.api_check_formula_exists(ind_3_uuid, formula_name)

    with allure.step(f'Открыть формулу "{formula_name}"'):
        ind_page.open_formula(formula_name)

    with allure.step(f'Задать формулу "{ind_names[0]} + {ind_names[1]}"'):
        ind_page.set_consolidation_formula(ind_names[0], ind_names[1], '+')

    with allure.step('Переключиться на дерево моделей'):
        tree.switch_to_models_tree()

    with allure.step(f'Проверить наличие тестовой папки "{folder_name}" в корне'):
        tree.check_test_folder(folder_name, tree_type='models')

    with allure.step(f'Создать модель в папке "{folder_name}"'):
        tree.create_model_in_folder(folder_name, model_name)

    with allure.step(f'Развернуть папку "{folder_name}"'):
        tree.expand_node(folder_name)

    with allure.step(f'Создать объект "{object_name_one}" класса "{class_name}" в модели "{model_name}"'):
        tree.create_model_object(model_name, class_name, object_name_one)

    with allure.step(f'Создать объект "{object_name_two}" класса "{class_name}" в модели "{model_name}"'):
        tree.create_model_object(model_name, class_name, object_name_two)

    with allure.step(f'Создать набор данных "{dataset_name_one}" в модели "{model_name}" через дерево'):
        tree.create_model_dataset(model_name, dataset_name_one)

    with allure.step(f'Открыть модель "{model_name}"'):
        tree.open_node(model_name)

    with allure.step(f'Создать набор данных "{dataset_name_two}" в модели "{model_name}" через страницу модели'):
        time.sleep(1)  # при нажатии на кнопку добавления датасета без задержки, модальное окно не появляется
        model_page.add_dataset(dataset_name_two)

    with allure.step(f'Создать таблицу данных "{table_name}" в модели "{model_name}"'):
        tree.create_model_table(model_name, table_name)

    with allure.step(f'Открыть таблицу данных "{table_name}" в модели "{model_name}"'):
        tree.open_node(table_name)

    with allure.step(f'Задать базовую структуру в таблице "{table_name}"'):
        constructor_page.create_base_structure()

    with allure.step(f'Переключиться к отображению таблицы'):
        constructor_page.switch_to_table()

    with allure.step(f'Заполнить таблицу "{table_name}" данными и проверить выполнение расчетов'):
        table_page.check_table_calculation()
