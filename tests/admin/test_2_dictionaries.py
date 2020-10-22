import allure
import pytest
from variables import PkmVars as Vars
from pages.dictionary_po import DictionaryPage


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево справочников')
@allure.title('Управление сущностями дерева справочников')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': 'Шельф. Приразломная',
        'tree_type': 'Справочники',
        'name': 'Управлениесущностями дерева справочников'
    })])
def test_admin_dictionaries_entities_control(parametrized_login_admin_driver, parameters):
    dictionary_page = DictionaryPage(parametrized_login_admin_driver)
    api = dictionary_page.api_creator.get_api_dictionaries()

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве справочников'):
        dictionary_page.tree.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)

    dict_name = api.create_unique_dict_name(Vars.PKM_BASE_DICTIONARY_NAME)

    with allure.step(f'Создать справочник "{dict_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве справочников'):
        dictionary_page.create_dictionary(Vars.PKM_TEST_FOLDER_NAME, dict_name)

    new_dict_name = api.create_unique_dict_name(Vars.PKM_BASE_DICTIONARY_NAME, subname='измененный')
    with allure.step(f'Переименовать справоник "{dict_name}" на "{new_dict_name}" на странице справочника'):
        node = dictionary_page.find_element(dictionary_page.tree.LOCATOR_SELECTED_NODE)
        dictionary_page.rename_title(new_dict_name)
    '''
    with allure.step(f'Проверить изменение названия справочника в дереве'):
        dictionary_page.wait_element_replacing(node, dictionary_page.tree.LOCATOR_SELECTED_NODE)
        assert dictionary_page.get_element_text(dictionary_page.tree.LOCATOR_SELECTED_NODE) == dictionary_page, 'Некорректное название ноды после переименования справочника'
    '''

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени справочника на странице справочника'):
        assert dictionary_page.get_entity_page_title() == new_dict_name.upper()

    with allure.step('Проверить отображение обновленного имени справочника в дереве'):
        assert dictionary_page.tree.get_selected_node_name() == new_dict_name

    with allure.step(f'Переименовать справоник "{new_dict_name}" на "{dict_name}" в дереве'):
        dictionary_page.tree.rename_node(new_dict_name, dict_name)
    '''
    with allure.step(f'Проверить изменение названия справочника на странице справочника'):
        assert dictionary_page.get_entity_page_title() == dict_name
    '''
    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени справочника на странице справочника'):
        assert dictionary_page.get_entity_page_title() == dict_name.upper()

    with allure.step('Проверить отображение обновленного имени справочника в дереве'):
        assert dictionary_page.tree.get_selected_node_name() == dict_name

    '''
    with allure.step(f'Удалить справочник "{dict_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве справочников'):
        dictionary_page.tree.delete_node(dict_name, 'Справочник')
    '''

