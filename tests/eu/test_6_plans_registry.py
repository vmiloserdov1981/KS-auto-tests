from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan
from pages.components.eu_filter import EuFilter
import users as user
import allure
import pytest
import time
from variables import PkmVars as Vars


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
    events_plan = EventsPlan(parametrized_login_driver)
    plans_registry = PlanRegistry(parametrized_login_driver)
    login = user.system_user.login
    versions = ['Проект плана', 'Факт']
    eu_filter = EuFilter(parametrized_login_driver)
    api = events_plan.api_creator.get_api_eu()

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step('Выбрать план-копию последнего плана к6'):
        plans_registry.select_plan_by_uuid(k6_plan_copy_uuid)

    with allure.step('Проверить, что в списке версий отображаются все версии плана'):
        plans_registry.check_plan_versions(k6_plan_copy_uuid)

    ui_versions = plans_registry.get_versions_names(with_dates=False)
    default_version = plans_registry.get_default_version()


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
        version1 = plans_registry.add_version(k6_plan_copy_uuid)
        parametrized_login_driver.test_data['to_delete']['datasets'] = [version1[1]]

    ui_versions.append(plans_registry.cut_version_date(version1[0]))

    with allure.step(f'Проверить что вновь созданная версия отображается в списке планов со статусом "Начальный"'):
        assert plans_registry.get_version_state(version1[0]) == 'Начальный'

    with allure.step(f'Добавить новую версию плана, созданную на основе версии "Проект плана"'):
        version2 = plans_registry.add_version(k6_plan_copy_uuid, based_on=versions[0])
        parametrized_login_driver.test_data['to_delete']['datasets'] = [version2[1]]

    ui_versions.append(plans_registry.cut_version_date(version2[0]))

    with allure.step(f'Проверить что вновь созданная версия отображается в списке планов со статусом "Начальный"'):
        assert plans_registry.get_version_state(version2[0]) == 'Начальный'

    with allure.step('Обновить страницу'):
        parametrized_login_driver.refresh()

    with allure.step('Проверить, что в списке версий отображаются все версии плана, включая вновь созданные'):
        plans_registry.check_plan_versions(k6_plan_copy_uuid, expected_ui_versions=ui_versions)

    with allure.step('Проверить, что версия по умолчанию не изменилась'):
        assert plans_registry.get_default_version() == default_version, 'Версия по умолчанию не соответствует изначальной'

    with allure.step('Посмотреть выбранный план на плане мероприятий'):
        plans_registry.find_and_click(plans_registry.LOCATOR_VIEW_PLAN_BUTTON)

    with allure.step('Проверить, что в дропдауне выбора версий отображаются все версии плана'):
        assert events_plan.compare_lists(events_plan.get_versions_names(), ui_versions), 'В дропдауне выбора версий не отображаются все версии плана'

    with allure.step(f'Выбрать версию плана {plans_registry.cut_version_date(version2[0])}'):
        events_plan.set_version(plans_registry.cut_version_date(version2[0]))

    with allure.step(f'Проверить, что на диаграмме отображаются все мероприятия из версии "Проект плана"'):
        eu_filter.reset_filters()
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True
            }
        }
        eu_filter.set_gantt_filters(filter_set)
        events_plan.check_plan_events(k6_plan_copy_uuid, versions[0], login, filter_set=filter_set)

    with allure.step(f'Проверить, что мероприятия в версии {version2[0]} соответствуют мероприятиям версии {versions[0]}'):
        version2_tasks = api.api_get_gantt_tasks(api.api_get_gantt(plans_registry.cut_version_date(version2[0]), k6_plan_copy_uuid, login))
        base_version_tasks = api.api_get_gantt_tasks(api.api_get_gantt(versions[0], k6_plan_copy_uuid, login))
        events_plan.compare_dicts(base_version_tasks, version2_tasks)

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    plans_registry_url = parametrized_login_driver.current_url

    with allure.step('Выбрать план-копию последнего плана к6'):
        plans_registry.select_plan_by_uuid(k6_plan_copy_uuid)

    with allure.step(f'Удалить вновь созданную версию f{version2[0]}'):
        plans_registry.delete_version(version2[0])
        parametrized_login_driver.test_data['to_delete']['datasets'].remove(version2[1])
        ui_versions.remove(plans_registry.cut_version_date(version2[0]))

    with allure.step(f'Установить вновь созданную версию {version1[0]} версией по умолчанию (отметить звездочкой)'):
        plans_registry.set_default_version(version1[0])

    with allure.step('Перейти на страницу "План мероприятий"'):
        header.navigate_to_page('План мероприятий (Главная)')

    '''
    with allure.step(f'Проверить, что в дропдауне выбора версий отображаются все версии плана, кроме удаленной версии "{version2[0]}"'):
        assert events_plan.compare_lists(events_plan.get_versions_names(), ui_versions), f'В дропдауне выбора версий не отображаются все версии плана'
    '''

    with allure.step(f'Выбрать версию плана {plans_registry.cut_version_date(version1[0])}'):
        events_plan.set_version(plans_registry.cut_version_date(version1[0]))

    with allure.step(f'Проверить, что на диаграмме отображаются все мероприятия из версии "Проект плана" незаполненными'):
        eu_filter.reset_filters()
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': False
            }
        }
        eu_filter.set_gantt_filters(filter_set)
        assert events_plan.get_events(names_only=True) == []
        filter_set['unfilled_events_filter']['Отображать незаполненные мероприятия'] = True
        eu_filter.set_gantt_filters(filter_set)
        events_plan.check_plan_events(k6_plan_copy_uuid, versions[0], login, filter_set=filter_set)

    with allure.step(f'Перейти к странице "Реестр интегрированных планов" (по ссылке, чтобы обновить страницу)'):
        parametrized_login_driver.get(plans_registry_url)

    with allure.step('Выбрать план-копию последнего плана к6'):
        plans_registry.select_plan_by_uuid(k6_plan_copy_uuid)

    with allure.step(f'Проверить, что в списке версий отображаются все версии плана, кроме удаленной версии "{version2[0]}"'):
        plans_registry.check_plan_versions(k6_plan_copy_uuid, expected_ui_versions=ui_versions)

    with allure.step(f'Проверить отображение вновь созданной версии {version1[0]} версией по умолчанию (отмечена звездочкой)'):
        assert plans_registry.get_default_version() == version1[0]


