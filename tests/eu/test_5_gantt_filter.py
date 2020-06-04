from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan
from pages.components.eu_filter import EuFilter
from variables import PkmVars as Vars
import users as user
import allure
import time
from selenium.common.exceptions import TimeoutException


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Фильтр незаполненных мероприятий')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_unfilled_events_filter(driver_eu_login):
    header = EuHeader(driver_eu_login)
    eu_filter = EuFilter(driver_eu_login)
    k6_plan_comment = driver_eu_login.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
    plan_registry_page = PlanRegistry(driver_eu_login)
    events_plan = EventsPlan(driver_eu_login, token=driver_eu_login.token)
    plan_uuid = driver_eu_login.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login
    versions = ('Проект плана', 'Факт')

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
        plan_registry_page.watch_plan_by_comment(k6_plan_comment)

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0])

    with allure.step('Проерить, что отображение незаполненных мероприятий отключено'):
        assert not eu_filter.is_show_empty_events(), 'Отображение незаполненных мероприятий включено'
        assert not eu_filter.is_show_empty_events_only(), 'Отображение только незаполненных мероприятий включено'

    with allure.step('Включить отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step('Проверить что на диаграме отображаются все мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Включить отображение только незаполненных мероприятий'):
        events_plan.scroll_to_gantt_top()
        eu_filter.switch_on_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': True,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step('Проерить, что отображение незаполненных мероприятий включено'):
        time.sleep(Vars.PKM_USER_WAIT_TIME)
        assert eu_filter.is_show_empty_events(), 'Отображение незаполненных мероприятий отключено'
        assert eu_filter.is_show_empty_events_only(), 'Отображение только незаполненных мероприятий отключено'

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': True,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Отключить отображение только незаполненных мероприятий'):
        eu_filter.switch_off_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются все мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Отключить отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step('Проверить что на диаграме отображаются только заполненные мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': False
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step(f'Выбрать версию плана "{versions[1]}"'):
        events_plan.set_version(versions[1])

    with allure.step('Проерить, что отображение незаполненных мероприятий отключено'):
        assert not eu_filter.is_show_empty_events(), 'Отображение незаполненных мероприятий включено'
        assert not eu_filter.is_show_empty_events_only(), 'Отображение только незаполненных мероприятий включено'

    with allure.step('Включить отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step('Проверить что на диаграме отображаются все мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Включить отображение только незаполненных мероприятий'):
        events_plan.scroll_to_gantt_top()
        eu_filter.switch_on_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': True,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step('Проерить, что отображение незаполненных мероприятий включено'):
        time.sleep(Vars.PKM_USER_WAIT_TIME)
        assert eu_filter.is_show_empty_events(), 'Отображение незаполненных мероприятий отключено'
        assert eu_filter.is_show_empty_events_only(), 'Отображение только незаполненных мероприятий отключено'

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': True,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Отключить отображение только незаполненных мероприятий'):
        eu_filter.switch_off_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются все мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': True
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Отключить отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step('Проверить что на диаграме отображаются только заполненные мероприятия плана'):
        filter_set = {
                    "unfilled_events_filter": {
                        'deleted_only': False,
                        'get_deleted': False
                    },
                    "custom_relations_filter": {}
                }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)
