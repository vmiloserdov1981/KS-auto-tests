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

    with allure.step(f'Удалить справочник "{dict_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве справочников'):
        dictionary_page.tree.delete_node(dict_name, 'Справочник')

