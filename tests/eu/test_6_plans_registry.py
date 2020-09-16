from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan
from api.api import ApiEu
import users as user
import allure
import pytest


@allure.feature('Интерфейс КП')
@allure.story('Реестр интегрированных планов')
@allure.title('Управление версиями ИП')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user2',
        'get_last_k6_plan': True,
        'get_last_k6_plan_copy': True,
        'select_last_k6_plan': False,
        'select_last_k6_plan_copy': False,
        'name': 'Управление версиями ИП'
    })])
def test_eu_plan_versions_control(parametrized_login_driver, parameters):
    header = EuHeader(parametrized_login_driver)
    k6_plan_copy_uuid = parametrized_login_driver.test_data.get('copy_last_k6_plan').get('uuid')
    events_plan = EventsPlan(parametrized_login_driver, token=parametrized_login_driver.token)
    plans_registry = PlanRegistry(parametrized_login_driver)
    login = user.system_user.login
    versions = ['Проект плана', 'Факт']

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step('Выбрать план-копию последнего плана к6'):
        plans_registry.select_plan_by_uuid(k6_plan_copy_uuid)

    with allure.step('Проверить, что в списке версий отображаются все версии плана'):
        plans_registry.check_plan_versions(k6_plan_copy_uuid)

    with allure.step('Проверить, что в списке версий не выделено никаких планов'):
        assert plans_registry.get_selected_version() is None, 'В списке версий присутствует выделенный план'

    with allure.step('Проверить, что в блоке кнопок управления версиями кликабельная только кнопка создания новой версии'):
        assert plans_registry.get_control_buttons(enabled_only=True) == ['Добавить'], 'Некорректные кликабельные кнопки управления версиями'

    with allure.step(f'Выбрать версию {versions[0]}'):
        plans_registry.select_version(versions[0])

    with allure.step('Проверить, что в блоке кнопок управления версиями все кнопки кликабельные'):
        assert plans_registry.get_control_buttons(disabled_only=True) == [], 'Некорректные кликабельные кнопки управления версиями'

    with allure.step(f'Выбрать версию {versions[1]}'):
        plans_registry.select_version(versions[1])

    with allure.step('Проверить, что в блоке кнопок управления версиями кнопки удаления и изменения статуса некликабельные'):
        assert plans_registry.compare_lists(plans_registry.get_control_buttons(disabled_only=True), ['Удалить', 'Изменить статус']), 'Некорректные кликабельные кнопки управления версиями'

    with allure.step(f'Добавить новую версию плана'):
        version1 = plans_registry.add_new_version(k6_plan_copy_uuid)
        parametrized_login_driver.test_data['to_delete']['datasets'] = [version1[1]]

    with allure.step(f'Проверить что вновь созданная версия отображается в списке планов со статусом "Начальный"'):
        assert plans_registry.get_version_state(version1[0]) == 'Начальный'
