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
        'tree_type': 'Справочники'
    })])
def test_eu_plan_versions_control(parametrized_login_admin_driver, parameters):
    dictionary_page = DictionaryPage(parametrized_login_admin_driver)

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве справочников'):
        dictionary_page.tree.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)
