import allure
import pytest
from variables import PkmVars as Vars
from pages.class_po import ClassPage


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево классов')
@allure.title('Управление сущностями дерева классов')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Классы',
        'name': 'Управление сущностями дерева классов'
    })])
def test_admin_classes_entities_control(parametrized_login_admin_driver, parameters):
    class_page = ClassPage(parametrized_login_admin_driver)
    api = class_page.api_creator.get_api_classes()
    indicator_1 = f'{class_page.BASE_INDICATOR_NAME}_1'
    indicator_2 = f'{class_page.BASE_INDICATOR_NAME}_2'
    relation_1 = f'{class_page.BASE_CLASS_RELATION_NAME}_1'
    relation_2 = f'{class_page.BASE_CLASS_RELATION_NAME}_2'

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве классов'):
        class_page.tree.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Проверить наличие класса для создания связи'):
        if not api.is_node_exists(Vars.PKM_RELATION_CLASS_NAME, 'class', Vars.PKM_TEST_FOLDER_NAME):
            class_page.create_class(Vars.PKM_TEST_FOLDER_NAME, Vars.PKM_RELATION_CLASS_NAME)

    with allure.step(f'Определить уникальное название класса'):
        class_name = api.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)

    with allure.step(f'Создать класс {class_name} в папке {Vars.PKM_TEST_FOLDER_NAME}'):
        class_page.create_class(Vars.PKM_TEST_FOLDER_NAME, class_name)

    new_class_name = api.create_unique_class_name(f'{class_name}_измененный')

    with allure.step(f'Переименовать класс "{class_name}" на "{new_class_name}" на странице справочника'):
        class_page.rename_title(new_class_name)

    with allure.step(f'Проверить изменение названия справочника в дереве'):
        class_page.wait_until_text_in_element(class_page.tree.LOCATOR_SELECTED_NODE, new_class_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени справочника на странице справочника'):
        assert class_page.get_entity_page_title() == new_class_name.upper()

    with allure.step('Проверить отображение обновленного имени справочника в дереве'):

        #выключить!
        class_page.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
        #выключить!

        assert class_page.tree.get_selected_node_name() == new_class_name

    with allure.step(f'Переименовать класс "{new_class_name}" на "{class_name}" в дереве'):
        title_html = class_page.find_element(class_page.LOCATOR_ENTITY_PAGE_TITLE).get_attribute('innerHTML')
        class_page.tree.rename_node(new_class_name, class_name)


    with allure.step(f'Проверить изменение названия класса на странице класса'):
        assert class_page.get_entity_page_title(prev_title_html=title_html) == class_name.upper()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    #выключить!
    class_page.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
    #выключить!

    with allure.step('Проверить отображение обновленного имени справочника на странице справочника'):
        assert class_page.get_entity_page_title() == class_name.upper()

    with allure.step('Проверить отображение обновленного имени справочника в дереве'):
        assert class_page.tree.get_selected_node_name() == class_name

    with allure.step(f'Создать новый показатель класса "{indicator_1}" через дерево '):
        indicator_1 = class_page.create_indicator(indicator_1, tree_parent_node=class_name)

    with allure.step(f'Перейти к классу "{class_name}"'):
        class_page.tree.select_node(class_name)

    with allure.step(f'Создать новый показатель класса "{indicator_2}" через страницу класса "{class_name}"'):
        indicator_2 = class_page.create_indicator(indicator_2)

    with allure.step(f'Создать новый класс-связь "{relation_1}" через дерево '):
        relation_1 = class_page.create_relation(f'{class_name}:{relation_1}', Vars.PKM_RELATION_CLASS_NAME, tree_parent_node=class_name)

    with allure.step(f'Перейти к классу "{class_name}"'):
        class_page.tree.select_node(class_name)

    with allure.step(f'Создать новый класс-связь "{relation_2}" через страницу класса "{class_name}"'):
        relation_2 = class_page.create_relation(f'{class_name}:{relation_2}', Vars.PKM_RELATION_CLASS_NAME)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

        # выключить!
        class_page.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
        # выключить!

    with allure.step(f'Проверить отображение всех созданных показателей и связей класса в дереве'):
        class_page.tree.expand_node(class_name)
        expected_children = [indicator_1['indicator_name'], indicator_2['indicator_name'], relation_1['relation_name'], relation_2['relation_name']]
        actual_children = class_page.tree.get_node_children_names(class_name)
        assert expected_children == actual_children, f'Некорректный список дочерних элементов класса {class_name}'

    with allure.step(f'Проверить отображение всех созданных показателей и связей класса на странице класса'):
        class_page.tree.select_node(class_name)
        assert class_page.compare_lists(class_page.get_class_indicators(), [indicator_1['indicator_name'], indicator_2['indicator_name']]), 'Некорректный список показателей класса'
        assert class_page.get_class_dimensions() is None, 'Некорректный список измерений класса'
        assert class_page.compare_lists(class_page.get_class_relations(), [relation_1['relation_name'], relation_2['relation_name']]), 'Некорректный список связей класса'

    with allure.step(f'Проверить успешный переход к созданному показателю через дерево'):
        class_page.tree.select_node(indicator_1['indicator_name'])
        assert class_page.get_indicator_page_data() == indicator_1

    with allure.step(f'Проверить успешный переход к созданной связи через дерево'):
        class_page.tree.select_node(relation_1['relation_name'])
        assert class_page.get_relation_page_data() == relation_1

    with allure.step(f'Проверить успешный переход к созданному показателю через страницу класса'):
        class_page.tree.select_node(class_name)
        class_page.find_and_click(class_page.list_element_creator(class_page.INDICATORS_LIST_NAME, indicator_1['indicator_name']))
        assert class_page.get_indicator_page_data() == indicator_1
        #assert class_page.tree.get_selected_node_name() == indicator_1['indicator_name']

    with allure.step(f'Проверить успешный переход к созданной связи через страницу класса'):
        class_page.tree.select_node(class_name)
        class_page.select_relation(relation_1['relation_name'])
        assert class_page.get_relation_page_data() == relation_1
        #assert class_page.tree.get_selected_node_name() == relation_1['relation_name']

    with allure.step(f'Перейти на страницу класса "{class_name}"'):
        class_page.find_and_click(class_page.tree.node_locator_creator(class_name))

    relation_1_name = relation_1['relation_name']
    with allure.step(f'Переименовать связь "{relation_1_name}" через дерево'):
        new_relation_name = relation_1_name + '_ред'
        class_page.tree.rename_node(relation_1_name, new_relation_name)
        relation_1['relation_name'] = relation_1_name = new_relation_name

    with allure.step(f'Проверить переименование связи на странице класса'):
        #assert class_page.get_class_relations() == [relation_1['relation_name'], relation_2['relation_name']]
        pass

    with allure.step(f'Проверить переименование связи на странице связи'):
        class_page.select_relation(relation_1['relation_name'])
        assert class_page.get_entity_page_title(return_raw=True) == relation_1['relation_name'], 'Некорректное название связи'

    with allure.step(f'Переименовать связь на странице связи'):
        relation_1_name += '_2'
        class_page.rename_title(relation_1_name)
        relation_1['relation_name'] = relation_1_name

    with allure.step(f'Проверить переименование связи в дереве'):
        # assert class_page.tree.get_selected_node_name() == relation_1['relation_name'], 'Некорректное название связи в дереве'
        # удалить остальные строчки в шаге после включения первой
        class_page.tree.expand_node(class_name)
        expected_children = [indicator_1['indicator_name'], indicator_2['indicator_name'], relation_1['relation_name'], relation_2['relation_name']]
        actual_children = class_page.tree.get_node_children_names(class_name)
        assert expected_children == actual_children, f'Некорректный список дочерних элементов класса {class_name}'

    with allure.step(f'Перейти на страницу класса "{class_name}"'):
        class_page.find_and_click(class_page.tree.node_locator_creator(class_name))

    with allure.step(f'Проверить переименование связи на странице класса'):
        assert class_page.compare_lists(class_page.get_class_relations(), [relation_1['relation_name'], relation_2['relation_name']])

    indicator_name = indicator_1['indicator_name']
    with allure.step(f'Переименовать показатель "{indicator_name}" на странице класса'):
        new_indicator_name = indicator_1['indicator_name'] + '_ред'
        class_page.rename_indicator(indicator_name, new_indicator_name)
        indicator_1['indicator_name'] = new_indicator_name

    with allure.step(f'Проверить переименование показателя "{indicator_name}" в дереве'):
        actual_children = class_page.tree.get_node_children_names(class_name)
        expected_children = [indicator_1['indicator_name'], indicator_2['indicator_name'], relation_1['relation_name'], relation_2['relation_name']]
        assert expected_children == actual_children, f'Некорректный список дочерних элементов класса {class_name}'

    with allure.step(f'Проверить переименование показателя "{indicator_name}" на странице показателя'):
        class_page.find_and_click(class_page.list_element_creator(class_page.INDICATORS_LIST_NAME, indicator_1['indicator_name']))
        assert class_page.get_entity_page_title() == indicator_1['indicator_name'].upper()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

        # выключить!
        class_page.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
        class_page.tree.expand_node(class_name)
        # выключить!

    with allure.step(f'Проверить отображение всех созданных показателей и связей класса в дереве'):
        expected_children = [indicator_1['indicator_name'], indicator_2['indicator_name'], relation_1['relation_name'], relation_2['relation_name']]
        actual_children = class_page.tree.get_node_children_names(class_name)
        assert expected_children == actual_children, f'Некорректный список дочерних элементов класса {class_name}'

    with allure.step(f'Проверить отображение всех созданных показателей и связей класса на странице класса'):
        class_page.tree.select_node(class_name)
        assert class_page.compare_lists(class_page.get_class_indicators(), [indicator_1['indicator_name'], indicator_2['indicator_name']]), 'Некорректный список показателей класса'
        assert class_page.get_class_dimensions() is None, 'Некорректный список измерений класса'
        assert class_page.compare_lists(class_page.get_class_relations(), [relation_1['relation_name'], relation_2['relation_name']]), 'Некорректный список связей класса'

    indicator_name = indicator_1['indicator_name']
    with allure.step(f'Удалить показатель {indicator_name} через дерево'):
        class_page.tree.delete_node(indicator_name, 'Показатель', parent_node_name=class_name)

    with allure.step(f'Проверить удаление показателя {indicator_name} на странице класса'):
        assert class_page.is_element_disappearing(class_page.list_element_creator(class_page.INDICATORS_LIST_NAME, indicator_name), wait_display=False), f'показатель {indicator_name} не удаляется на странице класса'

    indicator_name = indicator_2['indicator_name']
    with allure.step(f'Удалить показатель {indicator_name} класса через страницу класса'):
        class_page.delete_indicator(indicator_name)

    with allure.step(f'Проверить удаление показателя {indicator_name} в дереве'):
        assert class_page.is_element_disappearing(class_page.tree.children_node_locator_creator(class_name, children_node_name=indicator_name), wait_display=False), f'показатель {indicator_name} не удаляется на странице класса'

    with allure.step(f'Удалить связь {relation_1_name} через дерево'):
        class_page.tree.delete_node(relation_1_name, 'Связь', parent_node_name=class_name)

    with allure.step(f'Проверить удаление связи {relation_1_name} на странице класса'):
        assert class_page.is_element_disappearing(class_page.list_element_creator(class_page.RELATIONS_LIST_NAME, relation_1_name), wait_display=False), f'связь {relation_1_name} не удаляется на странице класса'

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    # выключить!
    class_page.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
    class_page.tree.expand_node(class_name)
    # выключить!

    with allure.step(f'Проверить отображение корректных показателей и связей класса на странице класса'):
        assert class_page.get_class_indicators() is None, 'Некорректный список показателей класса'
        assert class_page.get_class_dimensions() is None, 'Некорректный список измерений класса'
        assert class_page.get_class_relations() == [relation_2['relation_name']], 'Некорректный список связей класса'

    with allure.step(f'Проверить отображение корректных показателей и связей класса в дереве'):
        expected_children = [relation_2['relation_name']]
        actual_children = class_page.tree.get_node_children_names(class_name)
        assert expected_children == actual_children, f'Некорректный список дочерних элементов класса {class_name}'

    with allure.step(f'Удалить класс "{class_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве классов'):
        class_page.tree.delete_node(class_name, 'Класс', parent_node_name=Vars.PKM_TEST_FOLDER_NAME)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить отсутствие класса "{class_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}"'):
        assert class_name not in class_page.tree.get_node_children_names(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Проверить отсутствие справочника "{class_name}" в дереве справочников'):
        assert class_name not in api.get_classes_names()

