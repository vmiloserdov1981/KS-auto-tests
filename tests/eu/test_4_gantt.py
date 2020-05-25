from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan
from pages.components.eu_filter import EuFilter
from pages.components.modals import NewEventModal
from api.api import ApiEu
from variables import PkmVars as Vars
import users as user
import allure
import time
from variables import PkmVars


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
        event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, plan_uuid, login, subname='Создание')
        event_plan_data = {
            'event_name': event_name,
            'start_day': '10',
            'duration': '11',
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

    with allure.step(f'Проверить созданное мероприятие "{event_name}" на Ганте и открыть его'):
        events_plan.open_event(event_name, start_date=plan_event_data.get('start_date'), end_date=plan_event_data.get('end_date'))

    with allure.step(f'Проверить, что параметры созданного мероприятия "{event_name}" не изменились'):
        assert events_plan.get_event_data() == plan_event_data

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step(f'Проверить созданное мероприятие "{event_name}" на Ганте и открыть его'):
        events_plan.open_event(event_name, start_date=plan_event_data.get('start_date'), end_date=plan_event_data.get('end_date'))

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
    plan_uuid = driver_eu_login.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login
    versions = ('Проект плана', 'Факт', 'План потребности')
    event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, plan_uuid, login, subname='Удаление')
    event_data = {
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
    deleted_event_data = {
        'event_name': event_name,
        'start_date': [''],
        'duration': '',
        'end_date': [''],
        'event_type': event_data.get('event_type'),
        'works_type': event_data.get('works_type'),
        'plan': event_data.get('plan'),
        'ready': event_data.get('ready'),
        'comment': event_data.get('comment'),
        'responsible': event_data.get('responsible'),
        'is_cross_platform': event_data.get('is_cross_platform'),
        'is_need_attention': event_data.get('is_need_attention'),
    }

    deleted_event_data_2 = {
        'event_name': event_name,
        'start_date': [''],
        'duration': '',
        'end_date': ['Invalid date'],
        'event_type': event_data.get('event_type'),
        'works_type': event_data.get('works_type'),
        'plan': event_data.get('plan'),
        'ready': event_data.get('ready'),
        'comment': event_data.get('comment'),
        'responsible': event_data.get('responsible'),
        'is_cross_platform': event_data.get('is_cross_platform'),
        'is_need_attention': event_data.get('is_need_attention'),
    }

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

    with allure.step('Создать тестовое мероприятие через API"'):
        api.api_create_event(event_name, plan_uuid, 'Проект плана', login, event_data)

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
        plan_registry_page.watch_plan_by_comment(k6_plan_comment)

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0])

    with allure.step(f'Удалить мероприятие "{event_name}"'):
        events_plan.delete_event(event_name)

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Проверить отсутствие удаленного мероприятия "{event_name}" в списке мероприятий на Ганте'):
        assert not events_plan.is_event_exists(event_name), f'Мероприятие "{event_name}" присутствует в списке мероприятий на Ганте'

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что при удалении мероприятия "{event_name}", у него удалились только даты и длительность'):
        assert events_plan.get_event_data() == deleted_event_data or events_plan.get_event_data() == deleted_event_data_2
        events_plan.find_and_click(events_plan.LOCATOR_CANCEL_BUTTON)
    
    with allure.step(f'Выбрать версию плана "{versions[1]}"'):
        events_plan.set_version(versions[1])

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Проверить отсутствие удаленного мероприятия "{event_name}" в списке мероприятий на Ганте'):
        assert not events_plan.is_event_exists(event_name), f'Мероприятие "{event_name}" присутствует в списке мероприятий на Ганте'

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что мероприятие "{event_name}" пустое'):
        assert events_plan.get_event_data() == empty_data
        events_plan.find_and_click(events_plan.LOCATOR_CANCEL_BUTTON)

    with allure.step(f'Выбрать версию плана "{versions[2]}"'):
        events_plan.set_version(versions[2])

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Проверить отсутствие удаленного мероприятия "{event_name}" в списке мероприятий на Ганте'):
        assert not events_plan.is_event_exists(event_name), f'Мероприятие "{event_name}" присутствует в списке мероприятий на Ганте'

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что мероприятие "{event_name}" пустое'):
        assert events_plan.get_event_data() == empty_data


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Редактирование мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_modify_gantt_event(driver_eu_login):
    api = ApiEu(None, None, token=driver_eu_login.token)
    header = EuHeader(driver_eu_login)
    eu_filter = EuFilter(driver_eu_login)
    k6_plan_comment = driver_eu_login.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
    plan_registry_page = PlanRegistry(driver_eu_login)
    events_plan = EventsPlan(driver_eu_login)
    event_modal = NewEventModal(driver_eu_login)
    plan_uuid = driver_eu_login.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login
    versions = ('Проект плана', 'Факт', 'План потребности')
    event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, plan_uuid, login, subname='Изменение')
    event_data_plan = {
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
    event_data_fact = {
        'event_name': event_name,
        'start_day': '11',
        'duration': '3',
        'plan': 'План отгрузок',
        'ready': 'Готово к реализации',
        'comment': 'Версия факт',
        'responsible': 'Андре Аполлонов'
    }

    new_event_data_plan = {
        'duration': '3',
        'event_type': 'ПНГ',
        'comment': 'Отредактированный',
        'responsible': 'Олег Петров',
        'is_cross_platform': True,
        'is_need_attention': False
    }
    new_event_data_fact = {
        'start_day': '12',
        'duration': '5',
        'plan': 'План отгрузок',
        'ready': 'Готово к реализации',
        'comment': 'отредактированная задача',
        'responsible': 'Андрей Аполлонов'
    }

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

    with allure.step('Создать тестовое мероприятие через API"'):
        event_plan = api.api_create_event(event_name, plan_uuid, 'Проект плана', login, event_data_plan)
        event_uuid = event_plan.get('event_uuid')
        created_event_data_plan = event_plan.get('event_data')

    with allure.step('заполнить версию "Факт" для мероприятия, созданного через API"'):
        event_fact = api.api_update_event(event_uuid, plan_uuid, versions[1], login, event_data_fact)
        created_event_data_fact = event_fact.get('event_data')

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
        plan_registry_page.watch_plan_by_comment(k6_plan_comment)

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0])

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что данные мероприятия "{event_name}" соответствуют указанным при создании через API для версии "{versions[0]}"'):
        assert event_modal.check_event(created_event_data_plan), f'Данные мероприятия "{event_name}" не соответствуют указанным при создании через API для версии "{versions[0]}"'

    with allure.step(f'Редактировать мероприятие "{event_name}" и сохранить его'):
        new_event_data_plan = event_modal.modify_event(new_event_data_plan)

    with allure.step(f'Открыть отредактированное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что данные мероприятие "{event_name}" соответствуют указанным при редактировании'):
        assert event_modal.check_event(new_event_data_plan), f'Данные мероприятия "{event_name}" не соответствуют указанным при создании через API для версии "{versions[0]}"'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что данные мероприятие "{event_name}" соответствуют указанным при редактировании'):
        assert event_modal.check_event(new_event_data_plan), f'Данные мероприятия "{event_name}" не соответствуют указанным при создании через API для версии "{versions[0]}"'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step(f'Выбрать версию плана "{versions[1]}"'):
        events_plan.set_version(versions[1])

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что данные мероприятия "{event_name}" соответствуют указанным при создании через API для версии "{versions[1]}"'):
        assert event_modal.check_event(created_event_data_fact), f'Данные мероприятия "{event_name}" не соответствуют указанным при создании через API для версии "{versions[1]}"'

    with allure.step(f'Редактировать мероприятие "{event_name}" и сохранить его'):
        new_event_data_fact = event_modal.modify_event(new_event_data_fact)

    with allure.step(f'Открыть отредактированное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что данные мероприятия "{event_name}" соответствуют указанным при редактировании'):
        assert event_modal.check_event(new_event_data_fact), f'Данные мероприятия "{event_name}" не соответствуют указанным при редактировании для версии "{versions[1]}"'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step('Обновить страницу'):
        driver_eu_login.refresh()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что данные мероприятие "{event_name}" соответствуют указанным при редактировании'):
        assert event_modal.check_event(new_event_data_fact), f'Данные мероприятия "{event_name}" не соответствуют указанным при создании через API для версии "{versions[1]}"'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)
        time.sleep(PkmVars.PKM_USER_WAIT_TIME)

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0])

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что измененные данные мероприятия "{event_name}" в версии "{versions[0]}" не изменились'):
        assert event_modal.check_event(new_event_data_plan), f'Данные мероприятия "{event_name}" не соответствуют указанным при редактировании для версии "{versions[0]}"'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step(f'Выбрать версию плана "{versions[2]}"'):
        events_plan.set_version(versions[2])

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что мероприятие "{event_name}" пустое (указано только название мероприятия)'):
        assert event_modal.check_event(empty_data), f'Мероприятие "{event_name}" не пустое в версии "{versions[2]}"'
