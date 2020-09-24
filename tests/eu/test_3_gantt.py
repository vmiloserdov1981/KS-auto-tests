from pages.events_plan_po import EventsPlan
from pages.components.eu_filter import EuFilter
from pages.components.modals import NewEventModal
from api.api import ApiEu
from variables import PkmVars as Vars
import users as user
import allure
import time
from variables import PkmVars
from selenium.common.exceptions import TimeoutException
import pytest
from pages.components.eu_header import EuHeader
from pages.login_po import LoginPage


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Создание мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.green_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user2',
        'get_last_k6_plan': True,
        'select_last_k6_plan': False,
        'select_last_k6_plan_copy': True,
        'name': 'Создание мероприятия'
    })])
def test_eu_create_gantt_event(parametrized_login_driver, parameters):
    eu_filter = EuFilter(parametrized_login_driver)
    events_plan = EventsPlan(parametrized_login_driver)
    version1 = 'Проект плана'
    version2 = 'Факт'
    api = ApiEu(None, None, token=parametrized_login_driver.token)
    versions = ['Проект плана', 'Факт', 'План потребности']
    plan_uuid = parametrized_login_driver.test_data.get('copy_last_k6_plan').get('uuid')
    login = user.system_user.login

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
            'event_type': 'Не заполнено',
            'works_type': 'Не заполнено',
            'plan': 'Не заполнено',
            'ready': 'Не заполнено',
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
        parametrized_login_driver.refresh()

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
@pytest.mark.green_label
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user2',
        'get_last_k6_plan': True,
        'select_last_k6_plan': False,
        'select_last_k6_plan_copy': True,
        'name': 'Удаление мероприятия'
    })])
def test_eu_delete_gantt_event(parametrized_login_driver, parameters):
    api = ApiEu(None, None, token=parametrized_login_driver.token)
    eu_filter = EuFilter(parametrized_login_driver)
    events_plan = EventsPlan(parametrized_login_driver)
    login = user.system_user.login
    versions = ('Проект плана', 'Факт', 'План потребности')
    k6_copy_plan_uuid = parametrized_login_driver.test_data.get('copy_last_k6_plan').get('uuid')
    event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, k6_copy_plan_uuid, login, subname='Удаление')
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

    empty_data = {
        'event_name': event_name,
        'start_date': [''],
        'duration': '',
        'end_date': [''],
        'event_type': 'Не заполнено',
        'works_type': 'Не заполнено',
        'plan': 'Не заполнено',
        'ready': 'Не заполнено',
        'comment': '',
        'responsible': '',
        'is_cross_platform': False,
        'is_need_attention': False
    }

    with allure.step('Создать тестовое мероприятие через API"'):
        api.api_create_event(event_name, k6_copy_plan_uuid, 'Проект плана', login, event_data)

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0], force=True)

    with allure.step(f'Удалить мероприятие "{event_name}"'):
        events_plan.delete_event(event_name)

    with allure.step('Обновить страницу'):
        parametrized_login_driver.refresh()
    
    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Проверить отсутствие удаленного мероприятия "{event_name}" в списке мероприятий на Ганте'):
        assert not events_plan.is_event_exists(event_name), f'Мероприятие "{event_name}" присутствует в списке мероприятий на Ганте'
    
    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть созданное мероприятие "{event_name}" на Ганте'):
        events_plan.open_event(event_name)

    with allure.step(f'Проверить, что при удалении мероприятия "{event_name}", у него удалились только даты и длительность'):
        assert events_plan.get_event_data() == deleted_event_data
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
@pytest.mark.green_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user2',
        'get_last_k6_plan': True,
        'select_last_k6_plan': False,
        'select_last_k6_plan_copy': True,
        'name': 'Редактирование мероприятия'
    })])
def test_eu_modify_gantt_event(parametrized_login_driver, parameters):
    api = ApiEu(None, None, token=parametrized_login_driver.token)
    eu_filter = EuFilter(parametrized_login_driver)
    events_plan = EventsPlan(parametrized_login_driver)
    event_modal = NewEventModal(parametrized_login_driver)
    login = user.system_user.login
    versions = ('Проект плана', 'Факт', 'План потребности')
    k6_copy_plan_uuid = parametrized_login_driver.test_data.get('copy_last_k6_plan').get('uuid')
    event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, k6_copy_plan_uuid, login, subname='Изменение')
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
        'event_type': 'Не заполнено',
        'works_type': 'Не заполнено',
        'plan': 'Не заполнено',
        'ready': 'Не заполнено',
        'comment': '',
        'responsible': '',
        'is_cross_platform': False,
        'is_need_attention': False
    }

    with allure.step('Создать тестовое мероприятие через API"'):
        event_plan = api.api_create_event(event_name, k6_copy_plan_uuid, 'Проект плана', login, event_data_plan)
        event_uuid = event_plan.get('event_uuid')
        created_event_data_plan = event_plan.get('event_data')

    with allure.step('заполнить версию "Факт" для мероприятия, созданного через API"'):
        event_fact = api.api_update_event(event_uuid, k6_copy_plan_uuid, versions[1], login, event_data_fact)
        created_event_data_fact = event_fact.get('event_data')

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0], force=True)

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
        parametrized_login_driver.refresh()

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
        parametrized_login_driver.refresh()

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
        try:
            assert event_modal.check_event(empty_data), f'Мероприятие "{event_name}" не пустое в версии "{versions[2]}"'
        except TimeoutException:
            parametrized_login_driver.refresh()
            time.sleep(PkmVars.PKM_USER_WAIT_TIME)
            assert event_modal.check_event(empty_data), f'Мероприятие "{event_name}" не пустое в версии "{versions[2]}"'


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Копирование мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.green_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user2',
        'get_last_k6_plan': True,
        'select_last_k6_plan': False,
        'select_last_k6_plan_copy': True,
        'name': 'Копирование мероприятия'
})])
def test_eu_copy_gantt_event(parametrized_login_driver, parameters):
    api = ApiEu(None, None, token=parametrized_login_driver.token)
    eu_filter = EuFilter(parametrized_login_driver)
    events_plan = EventsPlan(parametrized_login_driver)
    event_modal = NewEventModal(parametrized_login_driver)
    login = user.system_user.login
    versions = ('Проект плана', 'Факт', 'План потребности')
    k6_copy_plan_uuid = parametrized_login_driver.test_data.get('copy_last_k6_plan').get('uuid')
    event_name = api.api_create_unique_event_name(Vars.PKM_BASE_EVENT_NAME, versions, k6_copy_plan_uuid, login, subname='для копирования')
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
    empty_data = {
        'event_name': event_name + ' (копия)',
        'start_date': [''],
        'duration': '',
        'end_date': [''],
        'event_type': 'Не заполнено',
        'works_type': 'Не заполнено',
        'plan': 'Не заполнено',
        'ready': 'Не заполнено',
        'comment': '',
        'responsible': '',
        'is_cross_platform': False,
        'is_need_attention': False
    }

    with allure.step('Создать тестовое мероприятие через API"'):
        event_plan = api.api_create_event(event_name, k6_copy_plan_uuid, versions[0], login, event_data)
        copied_event_data = event_plan.get('event_data')
        copied_event_data['event_name'] += ' (копия)'
        copied_event_name = copied_event_data.get('event_name')

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0], force=True)

    with allure.step(f'Копировать мероприятие "{event_name}" на Ганте'):
        events_plan.copy_event(event_name)

    with allure.step(f'Проверить, что скопированное мероприятие заполнено данными, которые соответствуют данным мероприятия "{event_name}"'):
        assert event_modal.check_event(copied_event_data), f'Данные скопированного мероприятия не соответствуют данным мероприятия "{event_name}"'

    with allure.step(f'Сохранить мероприятие "{copied_event_name}"'):
        event_modal.save_event()

    with allure.step(f'Открыть мероприятие "{copied_event_name}" на Ганте'):
        events_plan.open_event(copied_event_name)

    with allure.step(f'Проверить, что данные мероприятия "{copied_event_name}" соответствуют указанным при копировании'):
        assert event_modal.check_event(copied_event_data), f'Данные мероприятия "{copied_event_name}" не соответствуют указанным при создании'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step('Обновить страницу'):
        parametrized_login_driver.refresh()

    with allure.step(f'Открыть мероприятие "{copied_event_name}" на Ганте'):
        events_plan.open_event(copied_event_name)

    with allure.step(
            f'Проверить, что данные мероприятия "{copied_event_name}" соответствуют указанным при копировании'):
        assert event_modal.check_event(
            copied_event_data), f'Данные мероприятия "{copied_event_name}" не соответствуют указанным при создании'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step(f'Выбрать версию плана "{versions[1]}"'):
        events_plan.set_version(versions[1])

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(f'Проверить отсутствие скопированного мероприятия "{copied_event_name}" в списке мероприятий на Ганте'):
        assert not events_plan.is_event_exists(copied_event_name), f'Мероприятие "{copied_event_name}" присутствует в списке мероприятий на Ганте'

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть мероприятие "{copied_event_name}" на Ганте'):
        events_plan.open_event(copied_event_name)

    with allure.step(
            f'Проверить, что мероприятие "{copied_event_name}" пустое'):
        assert event_modal.check_event(empty_data), f'Мероприятие "{copied_event_name}" не пустое'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)

    with allure.step(f'Выбрать версию плана "{versions[2]}"'):
        events_plan.set_version(versions[2])

    with allure.step('Выключить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step(
            f'Проверить отсутствие скопированного мероприятия "{copied_event_name}" в списке мероприятий на Ганте'):
        assert not events_plan.is_event_exists(
            copied_event_name), f'Мероприятие "{copied_event_name}" присутствует в списке мероприятий на Ганте'

    with allure.step('Включить в фильтре отображение незаполненных мероприятий'):
        eu_filter.switch_on_empty_events()

    with allure.step(f'Открыть мероприятие "{copied_event_name}" на Ганте'):
        events_plan.open_event(copied_event_name)

    with allure.step(
            f'Проверить, что мероприятие "{copied_event_name}" пустое'):
        assert event_modal.check_event(empty_data), f'Мероприятие "{copied_event_name}" не пустое'
        event_modal.find_and_click(event_modal.LOCATOR_CANCEL_BUTTON)


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Группировка мероприятий')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.green_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user3',
        'get_last_k6_plan': True,
        'select_last_k6_plan': True,
        'select_last_k6_plan_copy': False,
        'name': 'Группировка мероприятий'
    })])
def test_eu_group_gantt_events(parametrized_login_driver, parameters):
    events_plan = EventsPlan(parametrized_login_driver)
    header = EuHeader(parametrized_login_driver)
    login_page = LoginPage(parametrized_login_driver)
    login = user.system_user.login
    versions = ('Проект плана', 'Факт', 'План потребности')
    k6_plan_uuid = parametrized_login_driver.test_data.get('last_k6_plan').get('uuid')
    group_values = ['Комментарий', 'Зона']
    filter_set = {
        "unfilled_events_filter": {
            'Только незаполненные мероприятия': False,
            'Отображать незаполненные мероприятия': False
        }
    }

    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0])

    with allure.step(f'Установить группировку мероприятий по значению "{group_values[0]}"'):
        events_plan.set_grouping(group_values[0])

    with allure.step(f'Проверить что на диаграме отображаются все мероприятия плана, сгруппированные по значению "{group_values[0]}"'):
        events_plan.check_plan_events(k6_plan_uuid, versions[0], login, filter_set=filter_set, group_by=group_values[0])

    with allure.step('Обновить страницу'):
        parametrized_login_driver.refresh()

    with allure.step(f'Проверить что на диаграмме Ганта установлена группировка по значению "{group_values[0]}"'):
        assert events_plan.get_grouping_value() == group_values[0]

    with allure.step(f'Проверить что на диаграме отображаются все мероприятия плана, сгруппированные по значению "{group_values[0]}"'):
        events_plan.check_plan_events(k6_plan_uuid, versions[0], login, filter_set=filter_set, group_by=group_values[0])

    with allure.step(f'Установить группировку мероприятий по значению "{group_values[1]}"'):
        events_plan.unset_grouping(group_values[0])
        events_plan.set_grouping(group_values[1])

    with allure.step(f'Проверить что на диаграме отображаются все мероприятия плана, сгруппированные по значению "{group_values[1]}"'):
        events_plan.check_plan_events(k6_plan_uuid, versions[0], login, filter_set=filter_set, group_by=group_values[1])

    with allure.step(f'Выбрать версию плана "{versions[1]}"'):
        events_plan.set_version(versions[1])

    with allure.step(f'Проверить что на диаграмме Ганта установлена группировка по значению "{group_values[1]}"'):
        assert events_plan.get_grouping_value() == group_values[1]

    with allure.step(f'Проверить что на диаграме отображаются все мероприятия плана, сгруппированные по значению "{group_values[1]}"'):
        events_plan.check_plan_events(k6_plan_uuid, versions[1], login, filter_set=filter_set, group_by=group_values[1])

    with allure.step(f'Выйти из системы'):
        header.logout()

    with allure.step(f'Залогиниться в системе как {parameters.get("login")}'):
        login_page.eu_login(parameters.get('login'))

    with allure.step('Перейти на страницу "План мероприятий"'):
        header.navigate_to_page('План мероприятий (Главная)')

    with allure.step(f'Проверить что на диаграмме Ганта установлена группировка по значению "{group_values[1]}"'):
        assert events_plan.get_grouping_value() == group_values[1]

    with allure.step(f'Проверить что на диаграме отображаются все мероприятия плана, сгруппированные по значению "{group_values[1]}"'):
        events_plan.check_plan_events(k6_plan_uuid, versions[1], login, filter_set=filter_set, group_by=group_values[1])
