from variables import PkmVars as Vars
from api.api import ApiClasses
import allure
from pages.components.trees import Tree
from pages.components.modals import Modals
from pages.class_po import ClassPage
from pages.class_po import IndicatorPage
from pages.main_po import MainPage
import time


@allure.feature('Классы')
@allure.story('Управление классами')
@allure.title('Создание класса в корне')
@allure.severity(allure.severity_level.CRITICAL)
def test_create_class(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    api = ApiClasses(None, None, token=driver_session.token)
    class_name = api.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
    class_page = ClassPage(driver_session, None, None, token=driver_session.token)

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step('Создать новый класс в корне дерева'):
        tree.create_root_class(class_name)
    with allure.step('Проверить переход на страницу вновь созданного класса'):
        class_page.check_page(class_name)

    with allure.step('Проверить отображение вновь созданного класса в дереве'):
        tree.check_node_in_tree(class_name)


@allure.feature('Классы')
@allure.story('Управление классами')
@allure.title('Удаление класса в корне')
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_class(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    api = ApiClasses(None, None, token=driver_session.token)
    class_name = driver_session.test_data.get('class_3').get('name')

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    nodes_order = tree.get_root_elements()
    nodes_order.remove(class_name)
    nodes_order = tuple(nodes_order)

    with allure.step(f'Удалить класс "{class_name}" в корне дерева'):
        tree.delete_node(class_name)

    with allure.step(f'Проверить отсутствие удаленного класса "{class_name}" в дереве'):
        tree.check_node_absence(class_name)

    with allure.step('Обновить страницу'):
        driver_session.refresh()

    with allure.step('Открыть дерево'):
        tree.open_tree()

    with allure.step(f'Проверить отсутствие удаленного класса "{class_name}" в дереве'):
        tree.check_node_absence(class_name)

    with allure.step(f'Проверить отсутствие удаленного класса "{class_name}" в апи'):
        api.api_check_class_absence(class_name)
        driver_session.test_data.pop('class_3')

    new_nodes_order = tuple(tree.get_root_elements())

    with allure.step(f'Проверить что порядок прошлых нод в дереве не изменился после удаления ноды "{class_name}"'):
        assert new_nodes_order == nodes_order, 'Порядок существующих нод изменился после удаления ноды'


@allure.feature('Классы')
@allure.story('Управление классами')
@allure.title('Переименование класса на странице класса')
@allure.severity(allure.severity_level.CRITICAL)
def test_rename_class_on_class_page(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    class_page = ClassPage(driver_session, None, None, token=driver_session.token)
    test_folder_name = driver_session.test_data.get('folder').get('name')
    test_class_name = driver_session.test_data.get('class_4').get('name')
    new_class_name = f'{test_class_name}_renamed'
    test_class_uuid = driver_session.test_data.get('class_4').get('class_uuid')
    main_page = MainPage(driver_session, url=f'{Vars.PKM_MAIN_URL}#/main')

    with allure.step('Перейти на главную страницу'):
        main_page.go_to_default_page()

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step(f'Развернуть в дереве тестовую папку"{test_folder_name}"'):
        tree.expand_node(test_folder_name)

    with allure.step(f'Открыть класс "{test_class_name}"'):
        tree.open_node(test_class_name)

    with allure.step(f'Переименовать класс "{test_class_name}" в заголовке'):
        class_page.rename_title(new_class_name)

    with allure.step(f'Проверить переименование класса "{test_class_name}" на класс "{new_class_name}"  в api'):
        time.sleep(Vars.PKM_API_WAIT_TIME)
        api_name = class_page.api_get_class_name_by_id(test_class_uuid)
        assert api_name == new_class_name


@allure.feature('Классы')
@allure.story('Управление показателями')
@allure.title('Создание показателей')
@allure.severity(allure.severity_level.CRITICAL)
def test_indicators_create(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    indicator_page = IndicatorPage(driver_session, None, None, token=driver_session.token)
    class_page = ClassPage(driver_session, None, None, token=driver_session.token)
    ind_names = tuple(f'{Vars.PKM_BASE_INDICATOR_NAME}_{i}' for i in range(2))
    test_folder_name = driver_session.test_data.get('folder').get('name')
    test_class_name = driver_session.test_data.get('class_1').get('name')
    test_class_uuid = indicator_page.api_get_class_id_by_name(test_class_name)
    modal = Modals(driver_session)
    main_page = MainPage(driver_session, url=f'{Vars.PKM_MAIN_URL}#/main')

    with allure.step('Перейти на главную страницу'):
        main_page.go_to_default_page()

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step(f'Развернуть в дереве тестовую папку"{test_folder_name}"'):
        tree.expand_node(test_folder_name)

    with allure.step('Создать новый показатель'):
        tree.create_indicator(test_class_name, ind_names[0])

    with allure.step('Проверить переход на страницу вновь созданного показателя'):
        indicator_page.check_page(indicator_name=ind_names[0], parent_class_uuid=test_class_uuid)

    with allure.step('Развернуть тестовый класс'):
        tree.expand_node(test_class_name)

    with allure.step('Проверить отображение вновь созданного показателя активным в дереве'):
        tree.check_indicator_in_tree(ind_names[0], test_class_name, active=True)

    with allure.step(f'Открыть родительский класс показателя "{ind_names[0]}"'):
        tree.open_node(test_class_name)

    with allure.step(f'Кликнуть на иконку добавления показателя'):
        class_page.find_and_click(class_page.LOCATOR_ADD_INDICATOR_BUTTON)

    with allure.step(f'Ввести имя показателя "{ind_names[1]} и нажать кнопку "Сохранить"'):
        modal.enter_and_save(ind_names[1])

    with allure.step('Проверить переход на страницу вновь созданного показателя'):
        indicator_page.check_page(indicator_name=ind_names[1], parent_class_uuid=test_class_uuid)
        indicator_uuid = indicator_page.get_uuid_from_url()

    with allure.step(f'Назначить показателю "{ind_names[1]}" тип "Строка"'):
        indicator_page.set_indicator_type('Строка')

    with allure.step(f'Проверить отображение вновь созданного показателя "{ind_names[1]}" активным в дереве'):
        tree.check_indicator_in_tree(ind_names[1], test_class_name, active=True)

    with allure.step(f'Проверить, что показателю "{ind_names[1]}" в апи установлен тип "Cтрока" '):
        time.sleep(Vars.PKM_API_WAIT_TIME)
        api_type = indicator_page.api_get_indicator_type(test_class_uuid, indicator_uuid)
        assert api_type == 'string', 'Для показателя в апи не установлен тип "Строка"'

    with allure.step('Открыть родительский класс показателей'):
        tree.open_node(test_class_name)

    with allure.step('Проверить отображение всех показателей на странице класса'):
        created_indicators = tuple(class_page.get_indicators_list())
        expected_indicators = ind_names
        assert created_indicators == expected_indicators

    with allure.step('Проверить порядок показателей в дереве'):
        tree_created_indicators = tuple(tree.get_node_childrens(test_class_name))
        tree_expected_indicators = ind_names
        assert tree_created_indicators == tree_expected_indicators


@allure.feature('Классы')
@allure.story('Управление показателями')
@allure.title('Удаление показателей')
@allure.severity(allure.severity_level.CRITICAL)
def test_indicators_delete(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    class_page = ClassPage(driver_session, None, None, token=driver_session.token)
    main_page = MainPage(driver_session, url=f'{Vars.PKM_MAIN_URL}#/main')
    api = ApiClasses(None, None, token=driver_session.token)
    ind_names = tuple(ind.get('name') for ind in driver_session.test_data.get('class_2').get('indicators'))
    ind_uuids = tuple(ind.get('indicator_uuid') for ind in driver_session.test_data.get('class_2').get('indicators'))
    test_folder_name = driver_session.test_data.get('folder').get('name')
    test_class_name = driver_session.test_data.get('class_2').get('name')
    test_class_uuid = driver_session.test_data.get('class_2').get('class_uuid')

    with allure.step('Перейти на главную страницу'):
        main_page.go_to_default_page()

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step(f'Развернуть в дереве тестовую папку"{test_folder_name}"'):
        tree.expand_node(test_folder_name)

    with allure.step(f'Развернуть в дереве тестовый класс "{test_class_name}" с показателями'):
        tree.expand_node(test_class_name)

    nodes_order = tree.get_node_childrens(test_class_name)
    nodes_order.remove(ind_names[0])
    nodes_order = tuple(nodes_order)

    with allure.step(f'Открыть в дереве тестовый класс "{test_class_name}" с показателями'):
        tree.open_node(test_class_name)

    with allure.step(f'Удалить показатель "{ind_names[0]}" в дереве'):
        tree.delete_node(ind_names[0])

    with allure.step(f'Проверить отсутствие удаленного показателя "{ind_names[0]}" в дереве у класса "{test_class_name}"'):
        tree.check_child_node_absense(test_class_name, ind_names[0])

    new_nodes_order = tuple(tree.get_node_childrens(test_class_name))

    with allure.step(f'Проверить что порядок дочерних элементов класса "{test_class_name}" не изменился после удаления показателя "{ind_names[0]}"'):
        assert new_nodes_order == nodes_order, 'Порядок существующих нод изменился после удаления ноды'

    with allure.step(f'Проверить отсутствие удаленного показателя "{ind_names[0]}" в api у класса "{test_class_name}"'):
        api.api_check_indicator_absense(test_class_uuid, ind_uuids[0])

    with allure.step('Обновить страницу'):
        driver_session.refresh()

    with allure.step(f'Открыть класс "{test_class_name}"'):
        tree.open_tree()
        tree.switch_to_classes_tree()
        tree.expand_node(test_folder_name)
        tree.expand_node(test_class_name)

    with allure.step(f'Проверить отсутствие удаленного показателя "{ind_names[0]}" в дереве у класса "{test_class_name}"'):
        tree.check_child_node_absense(test_class_name, ind_names[0])

    with allure.step(f'Проверить отсутствие удаленного показателя "{ind_names[0]}" на странице класса "{test_class_name}"'):
        assert ind_names[0] not in class_page.get_indicators_list()

    with allure.step(f'Удалить показатель"{ind_names[2]}" на странице класса "{test_class_name}"'):
        class_page.delete_indicator(ind_names[2])

    with allure.step(f'Проверить отсутствие удаленного показателя "{ind_names[2]}" в api у класса "{test_class_name}"'):
        api.api_check_indicator_absense(test_class_uuid, ind_uuids[2])

    with allure.step(f'Проверить отсутствие удаленного показателя "{ind_names[2]}" в дереве у класса "{test_class_name}"'):
        tree.check_child_node_absense(test_class_name, ind_names[2])


@allure.feature('Классы')
@allure.story('Управление показателями')
@allure.title('Переименование показателя на странице показателя')
@allure.severity(allure.severity_level.CRITICAL)
def test_rename_indicator_on_indicator_page(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    test_folder_name = driver_session.test_data.get('folder').get('name')
    test_class_name = driver_session.test_data.get('class_5').get('name')
    test_class_uuid = driver_session.test_data.get('class_5').get('class_uuid')
    main_page = MainPage(driver_session, url=f'{Vars.PKM_MAIN_URL}#/main')
    ind_name = driver_session.test_data.get('class_5').get('indicators')[0].get('name')
    new_ind_name = f'{ind_name}_renamed'
    ind_uuid = driver_session.test_data.get('class_5').get('indicators')[0].get('indicator_uuid')
    indicator_page = IndicatorPage(driver_session, None, None, token=driver_session.token)

    with allure.step('Перейти на главную страницу'):
        main_page.go_to_default_page()

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step(f'Развернуть в дереве тестовую папку"{test_folder_name}"'):
        tree.expand_node(test_folder_name)

    with allure.step(f'Развернуть в дереве тестовый класс "{test_class_name}" с показателями'):
        tree.expand_node(test_class_name)

    nodes_order = tree.get_node_childrens(test_class_name)
    nodes_order[0] = new_ind_name
    nodes_order = tuple(nodes_order)

    with allure.step(f'Открыть показатель "{ind_name}"'):
        tree.open_node(ind_name)

    with allure.step(f'Переименовать показатель "{ind_name}" в заголовке'):
        indicator_page.rename_title(new_ind_name)

    with allure.step(f'Проверить переименование показателя "{ind_name}" на показатель "{new_ind_name}"  в api'):
        time.sleep(Vars.PKM_API_WAIT_TIME)
        api_data = indicator_page.api_get_indicator(test_class_uuid, ind_uuid)
        api_name = api_data.get('name')
        assert api_name == new_ind_name

    new_nodes_order = tree.get_node_childrens(test_class_name)
    new_nodes_order = tuple(new_nodes_order)

    with allure.step('Проверить что переименованный показатель отображается в дереве корректно'):
        assert new_nodes_order == nodes_order, 'Показатель отображается в дереве некорректно'


@allure.feature('Классы')
@allure.story('Управление показателями')
@allure.title('Переименование показателя на странице класса')
@allure.severity(allure.severity_level.CRITICAL)
def test_rename_indicator_on_class_page(driver_session):
    tree = Tree(driver_session, None, None, token=driver_session.token)
    test_folder_name = driver_session.test_data.get('folder').get('name')
    test_class_name = driver_session.test_data.get('class_6').get('name')
    test_class_uuid = driver_session.test_data.get('class_6').get('class_uuid')
    main_page = MainPage(driver_session, url=f'{Vars.PKM_MAIN_URL}#/main')
    ind_name = driver_session.test_data.get('class_6').get('indicators')[0].get('name')
    new_ind_name = f'{ind_name}_renamed'
    ind_uuid = driver_session.test_data.get('class_6').get('indicators')[0].get('indicator_uuid')
    class_page = ClassPage(driver_session, None, None, token=driver_session.token)

    with allure.step('Перейти на главную страницу'):
        main_page.go_to_default_page()

    with allure.step('Переключиться на дерево классов'):
        tree.switch_to_classes_tree()

    with allure.step(f'Развернуть в дереве тестовую папку"{test_folder_name}"'):
        tree.expand_node(test_folder_name)

    with allure.step(f'Развернуть в дереве тестовый класс "{test_class_name}" с показателями'):
        tree.expand_node(test_class_name)

    nodes_order = tree.get_node_childrens(test_class_name)
    nodes_order[0] = new_ind_name
    nodes_order = tuple(nodes_order)

    with allure.step(f'Открыть класс "{test_class_name}"'):
        tree.open_node(test_class_name)

    with allure.step(f'Переименовать показатель "{ind_name}" в списке показателей'):
        class_page.rename_indicator(ind_name, new_ind_name)

    with allure.step(f'Проверить переименование показателя "{ind_name}" на показатель "{new_ind_name}"  в api'):
        time.sleep(Vars.PKM_API_WAIT_TIME)
        api_data = class_page.api_get_indicator(test_class_uuid, ind_uuid)
        api_name = api_data.get('name')
        assert api_name == new_ind_name

    new_nodes_order = tree.get_node_childrens(test_class_name)
    new_nodes_order = tuple(new_nodes_order)

    with allure.step('Проверить что переименованный показатель отображается в дереве корректно'):
        assert new_nodes_order == nodes_order, 'Переименованный показатель отображается в дереве некорректно'
