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

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве классов'):
        class_page.tree.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Проверить наличие класса для создания связи'):
        if not api.is_node_exists(Vars.PKM_RELATION_CLASS_NAME, 'class', Vars.PKM_TEST_FOLDER_NAME):
            class_page.create_class(Vars.PKM_TEST_FOLDER_NAME, Vars.PKM_RELATION_CLASS_NAME)

    with allure.step(f'Определить уникальное название класса'):
        class_name = api.create_unique_class_name(Vars.PKM_BASE_DICTIONARY_NAME)

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
        class_page.tree.rename_node(new_class_name, class_name)

    with allure.step(f'Проверить изменение названия справочника на странице справочника'):
        assert class_page.get_entity_page_title() == class_name.upper()

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    #выключить!
    class_page.tree.expand_node(Vars.PKM_TEST_FOLDER_NAME)
    #выключить!

    with allure.step('Проверить отображение обновленного имени справочника на странице справочника'):
        assert class_page.get_entity_page_title() == class_name.upper()

    with allure.step('Проверить отображение обновленного имени справочника в дереве'):
        assert class_page.tree.get_selected_node_name() == class_name

    with allure.step(f'Удалить класс "{class_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве классов'):
        class_page.tree.delete_node(class_name, 'Класс', parent_node_name=Vars.PKM_TEST_FOLDER_NAME)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить отсутствие класса "{class_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}"'):
        assert class_name not in class_page.tree.get_node_children_names(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Проверить отсутствие справочника "{class_name}" в дереве справочников'):
        assert class_name not in api.get_classes_names()
