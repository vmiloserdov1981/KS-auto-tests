from pages.events_plan_po import EventsPlan
from pages.components.eu_filter import EuFilter
from variables import PkmVars as Vars
import users as user
import allure
import time
import pytest


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Фильтр незаполненных мероприятий')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.green_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user3',
        'get_last_k6_plan': True,
        'select_last_k6_plan': True,
        'select_last_k6_plan_copy': False,
        'name': 'Фильтр незаполненных мероприятий'
    })])
def test_eu_unfilled_events_filter(parametrized_login_driver, parameters):
    eu_filter = EuFilter(parametrized_login_driver)
    events_plan = EventsPlan(parametrized_login_driver)
    plan_uuid = parametrized_login_driver.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login
    versions = ('Проект плана', 'Факт')

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
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True
            }
        }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Включить отображение только незаполненных мероприятий'):
        events_plan.scroll_to_gantt_top()
        eu_filter.switch_on_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': True,
                'Отображать незаполненные мероприятия': True
            }
        }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Обновить страницу'):
        parametrized_login_driver.refresh()

    with allure.step('Проерить, что отображение незаполненных мероприятий включено'):
        time.sleep(Vars.PKM_USER_WAIT_TIME * 2)
        assert eu_filter.is_show_empty_events(), 'Отображение незаполненных мероприятий отключено'
        assert eu_filter.is_show_empty_events_only(), 'Отображение только незаполненных мероприятий отключено'

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Отключить отображение только незаполненных мероприятий'):
        eu_filter.switch_off_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются все мероприятия плана'):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True
            }
        }
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set=filter_set)

    with allure.step('Отключить отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step('Проверить что на диаграме отображаются только заполненные мероприятия плана'):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': False
            }
        }
        parametrized_login_driver.refresh()
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
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True
            }
        }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Включить отображение только незаполненных мероприятий'):
        events_plan.scroll_to_gantt_top()
        eu_filter.switch_on_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': True,
                'Отображать незаполненные мероприятия': True
            }
        }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Обновить страницу'):
        parametrized_login_driver.refresh()

    with allure.step('Проерить, что отображение незаполненных мероприятий включено'):
        time.sleep(Vars.PKM_USER_WAIT_TIME * 2)
        assert eu_filter.is_show_empty_events(), 'Отображение незаполненных мероприятий отключено'
        assert eu_filter.is_show_empty_events_only(), 'Отображение только незаполненных мероприятий отключено'

    with allure.step('Проверить что на диаграме отображаются только незаполненные мероприятия плана'):
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Отключить отображение только незаполненных мероприятий'):
        eu_filter.switch_off_empty_only_events()

    with allure.step('Проверить что на диаграме отображаются все мероприятия плана'):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True
            }
        }
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)

    with allure.step('Отключить отображение незаполненных мероприятий'):
        eu_filter.switch_off_empty_events()

    with allure.step('Проверить что на диаграме отображаются только заполненные мероприятия плана'):
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': False
            }
        }
        parametrized_login_driver.refresh()
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set=filter_set)


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Фильтр custom relation')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.green_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user3',
        'get_last_k6_plan': True,
        'select_last_k6_plan': True,
        'select_last_k6_plan_copy': False,
        'name': 'Фильтр custom relation'
    })])
def test_eu_custom_relations_filter(parametrized_login_driver, parameters):
    eu_filter = EuFilter(parametrized_login_driver)
    events_plan = EventsPlan(parametrized_login_driver)
    plan_uuid = parametrized_login_driver.test_data.get('last_k6_plan').get('uuid')
    login = user.system_user.login
    versions = ('Проект плана', 'Факт')
    api = events_plan.api_creator.get_api_eu()
    # prefix = parametrized_login_driver.test_data['last_k6_plan']['plan_prefix']
    gantt = api.api_get_gantt(versions[0], plan_uuid, login)
    prefixes = api.get_plan_prefixes(gantt)

    default_filter_set = {
        "unfilled_events_filter": {
            'Только незаполненные мероприятия': False,
            'Отображать незаполненные мероприятия': False,
            'Скрывать мероприятия при фильтрации': False
        },
        "custom_fields_filter": {
            'Тип одновременных работ': [],
            'Функциональный план': [],
            'Готовность': [],
            'Тип мероприятия': [],

        },
        "custom_relations_filter": {
            'Персонал': [],
            'Зона': [],
            'Влияние на показатели': [],
            'Риски': [],
            'События для ИМ': []
        }

    }

    filter_set_1 = {
        "unfilled_events_filter": {
            'Только незаполненные мероприятия': False,
            'Отображать незаполненные мероприятия': False,
            'Скрывать мероприятия при фильтрации': True
        },
        "custom_fields_filter": {
            'Тип одновременных работ': [],
            'Функциональный план': [],
            'Готовность': [],
            'Тип мероприятия': ['Бурение']
        },
        "custom_relations_filter": {
            'Персонал': [],
            'Зона': [],
            'Влияние на показатели': [],
            'Риски': [],
            'События для ИМ': []
        }

    }

    filter_set_2 = {
        "unfilled_events_filter": {
            'Только незаполненные мероприятия': False,
            'Отображать незаполненные мероприятия': False,
            'Скрывать мероприятия при фильтрации': True
        },
        "custom_fields_filter": {
            'Тип одновременных работ': [],
            'Функциональный план': [],
            'Готовность': [],
            'Тип мероприятия': [],

        },
        "custom_relations_filter": {
            'Персонал': [],
            # 'Зона': [f'0 D1L5 {prefix}'],
            'Зона': [f'{prefixes[0]}D1L5{prefixes[1]}'],
            'Влияние на показатели': [],
            'Риски': [],
            'События для ИМ': []
        }

    }

    filter_set_3 = {
        "unfilled_events_filter": {
            'Только незаполненные мероприятия': False,
            'Отображать незаполненные мероприятия': True,
            'Скрывать мероприятия при фильтрации': False
        },
        "custom_fields_filter": {
            'Тип одновременных работ': ['(пусто)'],
            'Функциональный план': [],
            'Готовность': ['Выполнено', 'Не будет выполнено'],
            'Тип мероприятия': ['Текущая', 'ТОРО'],

        },
        "custom_relations_filter": {
            'Персонал': ['(пусто)'],
            # 'Зона': [f'0 D1L5 {prefix}'],
            'Зона': [f'{prefixes[0]}D1L5{prefixes[1]}'],
            'Влияние на показатели': [],
            # 'Риски': [f'0 Риск 2 {prefix}', f'0 Риск 1 {prefix}'],
            'Риски': [f'{prefixes[0]}Риск 1{prefixes[1]}', f'{prefixes[0]}Риск 2{prefixes[1]}'],
            'События для ИМ': []
        }

    }
    with allure.step(f'Выбрать версию плана "{versions[0]}"'):
        events_plan.set_version(versions[0])

    with allure.step(f'Проверить, что фильтры custom_relations не заполнены по умолчанию'):
        assert events_plan.get_filter_set() == default_filter_set
    
    with allure.step(f'Задать сет фильтров {filter_set_1}'):
        eu_filter.set_gantt_filters(filter_set_1)

    with allure.step(f'Проверить, что на диаграмме Ганта отображаются мероприятия согласно установленных фильтров'):
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set_1)

    with allure.step(f'Задать сет фильтров {filter_set_2}'):
        eu_filter.reset_filters()
        eu_filter.set_gantt_filters(filter_set_2)

    with allure.step(f'Проверить, что на диаграмме Ганта отображаются мероприятия согласно установленных фильтров'):
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set_2)

    with allure.step(f'Задать сет фильтров {filter_set_3}'):
        eu_filter.reset_filters()
        eu_filter.set_gantt_filters(filter_set_3)

    with allure.step(f'Проверить, что на диаграмме Ганта отображаются все мероприятия (мероприятия, не совпадающие с фильтром отображаются скрытыми)'):
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set_3)

    with allure.step('Включить тогл "Скрывать мероприятия при фильтрации"'):
        eu_filter.switch_on_events_hiding()

    with allure.step(f'Проверить, что на диаграмме Ганта отображаются мероприятия согласно установленных фильтров'):
        filter_set_3['unfilled_events_filter']['Скрывать мероприятия при фильтрации'] = True
        events_plan.check_plan_events(plan_uuid, versions[0], login, filter_set_3)

    with allure.step(f'Обновить страницу'):
        parametrized_login_driver.refresh()

    with allure.step(f'Проверить, что состояние установленных фильтров не изменилось'):
        time.sleep(10)
        actual_filters = eu_filter.get_filter_set()
        for i in actual_filters:
            eu_filter.compare_dicts(actual_filters.get(i), filter_set_3.get(i))

    with allure.step(f'Выбрать версию плана "{versions[1]}"'):
        events_plan.set_version(versions[1])

    with allure.step(f'Проверить, что состояние установленных фильтров не изменилось'):
        actual_filters = eu_filter.get_filter_set()
        for i in actual_filters:
            eu_filter.compare_dicts(actual_filters.get(i), filter_set_3.get(i))

    with allure.step(f'Проверить, что на диаграмме Ганта отображаются мероприятия согласно установленных фильтров'):
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set_3)

    with allure.step(f'Сбросить настройки фильтров'):
        eu_filter.reset_filters()

    for filter_val in filter_set_3.get("custom_fields_filter"):
        filter_set_3["custom_fields_filter"][filter_val] = []
    for relation in filter_set_3.get("custom_relations_filter"):
        filter_set_3['custom_relations_filter'][relation] = []

    with allure.step(f'Проверить, что фильтры custom_relation отображаются пустыми'):
        assert eu_filter.get_filter_set() == filter_set_3

    with allure.step(f'Проверить, что на диаграмме Ганта отображаются мероприятия согласно установленных фильтров'):
        events_plan.check_plan_events(plan_uuid, versions[1], login, filter_set_3)
