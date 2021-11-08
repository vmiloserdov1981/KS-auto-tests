import allure
import pytest
from variables import PkmVars as Vars
from api.api_classes import ApiClasses


@allure.feature('API тесты')
@allure.story('Дерево классов')
@allure.title('Управление сущностями дерева классов')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.blue_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
    })])
def test_api_classes_control(api_driver, parameters):
    api = ApiClasses(api_driver.login, api_driver.password, api_driver.project_uuid, token=api_driver.token)
    socket = api_driver.ws
    socket.ws_timeout = 30

    with allure.step(f'Создать уникальное название класса'):
        class_name = api.create_unique_class_name('API-класс')

    with allure.step(f'Создать класс {class_name}'):
        class_data = api.create_class_node(class_name)
        class_node_uuid = class_data['nodeUuid']
        class_uuid = class_data['referenceUuid']
        class_name = api.create_unique_class_name(class_name + '_renamed')

    with allure.step('Подписаться на WS дерева'):
        socket.send_message({'action': 'subscribe', 'subject': 'classes_tree_updated'})

    with allure.step(f'Переименовать класс {class_name}'):
        api.rename_class_node(class_node_uuid, class_name, ws=socket)

    with allure.step(f'Проверить переименование класса {class_name}'):
        assert api.get_class_name(class_uuid) == class_name

    with allure.step(f'Проверить переименование ноды класса {class_name}'):
        assert api.get_node_by_reference_uuid(class_uuid).get('name') == class_name

    with allure.step(f'Удалить класс {class_name}'):
        api.delete_class_node(class_node_uuid)

    with allure.step(f'Проверить отсутствие класса {class_name} в дереве классов'):
        assert class_name not in api.get_classes_names()
