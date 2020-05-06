from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan
from pages.components.eu_filter import EuFilter
from api.api import ApiEu
import time
from variables import PkmVars as Vars
import users as user
import allure


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Создание мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_create_gantt_event(driver_eu_login):
    header = EuHeader(driver_eu_login)
    eu_filter = EuFilter(driver_eu_login)
    k6_plan_comment = driver_eu_login.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
    plan_registry_page = PlanRegistry(driver_eu_login)
    events_plan = EventsPlan(driver_eu_login)
    version1 = 'Проект плана'
    version2 = 'Факт'
    api = ApiEu(None, None, token=driver_eu_login.token)
    versions = ['Проект плана', 'Факт', 'План потребности']
    plan_uuid = driver_eu_login.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
        plan_registry_page.watch_plan_by_comment(k6_plan_comment)

    with allure.step(f'Выбрать версию плана "{version1}"'):
        events_plan.set_version(version1)

    with allure.step(f'Создать мероприятие'):
        event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, plan_uuid, login)
        event_plan_data = {
            'event_name': event_name,
            'start_day': '10',
            'duration': '5',
            'event_type': 'Текущая',
            'works_type': 'Бурение',
            'plan': 'План отгрузок',
            'ready': 'Готово к реализации',
            'comment': 'Авто тест',
            'responsible': 'Олег Петров',
            'is_cross_platform': True,
            'is_need_attention': True
        }
        plan_event_data = events_plan.create_event(event_plan_data)
        empty_data = {
            'event_name': event_name,
            'start_date': [''],
            'duration': '',
            'end_date': [''],
            'event_type': '',
            'works_type': '',
            'plan': '',
            'ready': '',
            'comment': '',
            'responsible': '',
            'is_cross_platform': False,
            'is_need_attention': False
        }

    with allure.step(f'Проверить отображение мероприятия на Ганте'):
        events_plan.check_event(plan_event_data.get('event_name'), plan_event_data.get('start_date'), plan_event_data.get('end_date'))

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что параметры созданного мероприятия "{event_name}" не изменились'):
        assert events_plan.get_event_data() == plan_event_data

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step(f'Проверить отображение мероприятия на Ганте'):
        events_plan.check_event(plan_event_data.get('event_name'), plan_event_data.get('start_date'), plan_event_data.get('end_date'))

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что параметры созданного мероприятия "{event_name}" не изменились'):
        assert events_plan.get_event_data() == plan_event_data
        events_plan.find_and_click(events_plan.LOCATOR_CANCEL_BUTTON)

    with allure.step(f'Выбрать версию плана "{version2}"'):
        events_plan.set_version(version2)

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Проверить, что мероприятие "{event_name}" не отображается на Ганте'):
        assert event_name not in events_plan.get_event_names()

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()
        time.sleep(Vars.PKM_USER_WAIT_TIME)

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что мероприятие "{event_name}" пустое'):
        assert events_plan.get_event_data() == empty_data


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Удаление мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_delete_gantt_event(driver_eu_login):
    api = ApiEu(None, None, token=driver_eu_login.token)
    header = EuHeader(driver_eu_login)
    eu_filter = EuFilter(driver_eu_login)
    k6_plan_comment = driver_eu_login.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
    plan_registry_page = PlanRegistry(driver_eu_login)
    events_plan = EventsPlan(driver_eu_login)
    version1 = 'Проект плана'
    version2 = 'Факт'
    plan_uuid = driver_eu_login.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login
    versions = ['Проект плана', 'Факт', 'План потребности']
    event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, plan_uuid, login)

    with allure.step('Создать тестовое мероприятие через API"'):
        api.api_create_event(event_name, plan_uuid, 'Проект плана', login)
