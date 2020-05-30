from pages.components.eu_header import EuHeader
from pages.plan_registry_po import PlanRegistry
from pages.events_plan_po import EventsPlan
from api.api import ApiEu
import users as user
import allure


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Создание мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_create_gantt_event(driver_eu_login):
    header = EuHeader(driver_eu_login, token=driver_eu_login.token)
    k6_plan = driver_eu_login.test_data.get('last_k6_plan')
    k6_plan_comment = k6_plan.get('settings').get('plan').get('comment')
    k6_plan_uuid = k6_plan.get('uuid')
    k6_plan_name = k6_plan.get('name')
    events_plan = EventsPlan(driver_eu_login, token=driver_eu_login.token)
    plans_registry = PlanRegistry(driver_eu_login, token=driver_eu_login.token)
    api = ApiEu(None, None, token=driver_eu_login.token)
    login = user.system_user.login

    with allure.step(f'Проверить наличие плана - копии ИП "{k6_plan_name}"'):
        driver_eu_login.test_data['copy_last_k6_plan'] = api.check_k6_plan_copy(k6_plan_comment, k6_plan_uuid)
        if driver_eu_login.test_data['copy_last_k6_plan'].get('is_new_created'):
            driver_eu_login.refresh()

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step('Проверить, что в дропдауне выбора планов отображается название плана, выбранного в реестре ИП'):
        plans_registry.check_selected_plan()

    with allure.step('Проверить, что в дропдауне выбора планов отображаются все планы системы'):
        header.check_plan_dropdown_values()

    with allure.step(f'Посмотреть на диаграмме Ганта план - копию ИП "{k6_plan_name}"'):
        plans_registry.watch_plan_by_comment(
            driver_eu_login.test_data['copy_last_k6_plan'].get('settings').get('plan').get('comment'))

    header.wait_until_text_in_element(header.LOCATOR_EU_PAGE_TITLE, 'ПЛАН МЕРОПРИЯТИЙ (ГЛАВНАЯ)')
    copy_name = driver_eu_login.test_data['copy_last_k6_plan'].get('name')
    copy_uuid = driver_eu_login.test_data['copy_last_k6_plan'].get('uuid')

    with allure.step(
            f'Проверить, что в дропдауне выбора планов отображается план "{copy_name}", выбранный в реестре ИП'):
        assert header.get_plan_dropdown_placeholder() == copy_name, 'В дропдануне планов отображается неправильный план'

    with allure.step(f'Выбрать план "{k6_plan_name}", в дропдауне выбора версий'):
        header.select_plan(plan_uuid=k6_plan_uuid, plan_name=k6_plan_name)
        events_plan.wait_dom_changing()

    with allure.step(f'Проверить что диаграмма Ганта отображается в соответствии с выбранной версией'):
        events_plan.check_plan_events(k6_plan_uuid, 'Проект плана', login)

    with allure.step(f'Выбрать план "{copy_name}", в дропдауне выбора версий'):
        header.select_plan(plan_uuid=copy_uuid, plan_name=copy_name)
        events_plan.wait_dom_changing()

    with allure.step(f'Проверить что диаграмма Ганта отображается в соответствии с выбранной версией'):
        events_plan.check_plan_events(copy_uuid, 'Проект плана', login)

    with allure.step('Перейти на страницу "Реестр ИП"'):
        header.navigate_to_page('Реестр интегрированных планов')

    with allure.step(f'Проверить, что в реестре ИП отображается выбранным план {copy_name}'):
        assert plans_registry.get_selected_plan().get('name') == copy_name

    with allure.step(f'Проверить, что в дропдауне планов в header отображается выбранным план "{copy_name}"'):
        assert header.get_plan_dropdown_placeholder() == copy_name

    with allure.step(
            f'Выбрать план "{k6_plan_name}", в дропдауне выбора версий и проверить что активный план в списке ИП обновился'):
        star = plans_registry.find_element(plans_registry.LOCATOR_STAR)
        header.select_plan(plan_uuid=k6_plan_uuid, plan_name=k6_plan_name)
        plans_registry.wait_element_changing(star, plans_registry.LOCATOR_STAR)
        assert plans_registry.get_selected_plan().get('uuid') == k6_plan_uuid, 'Неверный план отображается выбранным'

    with allure.step(
            f'Выбрать план "{copy_name}", в дропдауне выбора версий и проверить что активный план в списке ИП обновился'):
        star = plans_registry.find_element(plans_registry.LOCATOR_STAR)
        header.select_plan(plan_uuid=copy_uuid, plan_name=copy_name)
        plans_registry.wait_element_changing(star, plans_registry.LOCATOR_STAR)
        assert plans_registry.get_selected_plan().get('uuid') == copy_uuid, 'Неверный план отображается выбранным'
