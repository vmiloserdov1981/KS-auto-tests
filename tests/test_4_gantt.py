from pages.login_po import LoginPage
from pages.main_po import MainPage
from pages.components.trees import UserBlock
from variables import PkmVars as Vars
from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan

from pages.components.modals import Modals
import users as user
import allure


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Создание мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_create_gantt_event(driver_eu_login):
    header = EuHeader(driver_eu_login)
    k6_plan_comment = driver_eu_login.test_data.get('last_k6_plan').get('settings').get('plan').get('comment')
    plan_registry_page = PlanRegistry(driver_eu_login)
    events_plan = EventsPlan(driver_eu_login)
    version1 = 'Проект плана'
    version2 = 'Факт'


    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step(f'Посмотреть на плане мероприятий последний план, созданный в к6 (с комментарием "{k6_plan_comment}")'):
        plan_registry_page.watch_plan_by_comment(k6_plan_comment)

    with allure.step(f'Выбрать версию плана "{version1}"'):
        events_plan.set_version(version1)

    with allure.step(f'Создать мероприятие'):
        event_name = events_plan.create_unique_event_name(Vars.PKM_BASE_EVENT_NAME)
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
        events_plan.create_event(event_data)
