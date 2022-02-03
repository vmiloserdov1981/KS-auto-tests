import allure
import pytest
from variables import PkmVars as Vars
from pages.bpms_po import BpmsPage
from pages.bpms_po import BpmsEventPage
from pages.bpms_po import BpmsTaskPage
from pages.bpms_po import BpmsGatePage
from conditions.clean_factory import BpmsNodeCreator


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево бизнес процессов')
@allure.title('Управление бизнес процессами')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Бизнес процессы',
        'name': 'Управление бизнес процессами'
    })])
def test_admin_bpms_control(parametrized_login_admin_driver, parameters):
    bpms_page = BpmsPage(parametrized_login_admin_driver)
    api = bpms_page.api_creator.get_api_bpms()

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве bpms'):
        bpms_page.tree.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Определить уникальное название бизнес процесса'):
        bpms_name = api.create_unique_bpms_name(Vars.PKM_BASE_BPMS_NAME)
        new_bpms_name = f"{bpms_name}_переименованный"

    with allure.step(f'Создать бизнес процесс {bpms_name} в папке {Vars.PKM_TEST_FOLDER_NAME}'):
        bpms_page.create_bpms(Vars.PKM_TEST_FOLDER_NAME, bpms_name)

    with allure.step(f'Переименовать бизнес процесс {bpms_name} на "{new_bpms_name}" на странице бизнес процесса'):
        bpms_page.tree.rename_node(bpms_name, new_bpms_name)
        # Включить переименование через страницу после исправления PKM-9375
        # bpms_page.rename_title(new_bpms_name)

    with allure.step(f'Проверить изменение названия бизнес процесса в дереве'):
        bpms_page.tree.wait_selected_node_name(new_bpms_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени бизнес процесса на странице бизнес процесса'):
        bpms_page.wait_page_title(new_bpms_name)

    with allure.step(f'Проверить изменение названия бизнес процесса в дереве'):
        bpms_page.tree.wait_selected_node_name(new_bpms_name)

    with allure.step(f'Переименовать бизнес процесс {new_bpms_name} на "{bpms_name}" в дереве'):
        bpms_page.tree.rename_node(new_bpms_name, bpms_name)

    with allure.step('Проверить отображение обновленного имени бизнес процесса на странице бизнес процесса'):
        bpms_page.wait_page_title(bpms_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени бизнес процесса на странице бизнес процесса'):
        bpms_page.wait_page_title(bpms_name)

    with allure.step(f'Проверить изменение названия бизнес процесса в дереве'):
        bpms_page.tree.wait_selected_node_name(bpms_name)

    with allure.step(f'Удалить бизнес процесс "{bpms_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}" в дереве'):
        bpms_page.tree.delete_node(bpms_name, 'Бизнес процесс', parent_node_name=Vars.PKM_TEST_FOLDER_NAME)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить отсутствие бизнес процесса "{bpms_name}" в папке "{Vars.PKM_TEST_FOLDER_NAME}"'):
        assert bpms_name not in bpms_page.tree.get_node_children_names(Vars.PKM_TEST_FOLDER_NAME)

    with allure.step(f'Проверить отсутствие бизнес процесса "{bpms_name}" в дереве'):
        assert bpms_name not in api.get_bpms_names()


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево бизнес процессов')
@allure.title('Управление событиями бизнес процессов')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Бизнес процессы',
        'name': 'Управление событиями бизнес процессов'
    })])
def test_admin_bpms_events_control(parametrized_login_admin_driver, parameters):
    bpms_event_page = BpmsEventPage(parametrized_login_admin_driver)
    api = bpms_event_page.api_creator.get_api_bpms()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    event_name = "Событие BPMS"
    new_event_name = f"{event_name}_переименованное"

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве bpms через API'):
        test_folder_uuid = api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название бизнес процесса'):
        bpms_name = api.create_unique_bpms_name(f"{Vars.PKM_BASE_BPMS_NAME}_события")

    with allure.step(f'Создать бизнес процесс {bpms_name} в папке {test_folder_name} через API'):
        bpms_data = api.create_bpms(bpms_name, parent_uuid=test_folder_uuid)
        bpms_node_uuid = bpms_data.get('nodeUuid')

    with allure.step(f'Добавить бизнес процесс {bpms_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(BpmsNodeCreator(parametrized_login_admin_driver, bpms_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        bpms_event_page.tree.expand_node(test_folder_name)

    with allure.step(f'Создать событие {event_name} в бизнес процессе {bpms_name}'):
        bpms_event_page.create_bpms_event(bpms_name, event_name)

    with allure.step(f'Переименовать событие {event_name} на "{new_event_name}" на странице события'):
        bpms_event_page.tree.rename_node(event_name, new_event_name)
        # Включить переименование через страницу после исправления PKM-9375
        # bpms_page.rename_title(new_bpms_name)

    with allure.step(f'Проверить изменение названия события в дереве'):
        bpms_event_page.tree.wait_selected_node_name(new_event_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного события на странице события'):
        bpms_event_page.wait_page_title(new_event_name)

    with allure.step(f'Проверить изменение названия бизнес процесса в дереве'):
        bpms_event_page.tree.wait_selected_node_name(new_event_name)

    with allure.step(f'Переименовать событие {new_event_name} на "{event_name}" в дереве'):
        bpms_event_page.tree.rename_node(new_event_name, event_name)

    with allure.step('Проверить отображение обновленного имени бизнес процесса на странице бизнес процесса'):
        bpms_event_page.wait_page_title(event_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени бизнес процесса на странице бизнес процесса'):
        bpms_event_page.wait_page_title(event_name)

    with allure.step(f'Проверить изменение названия бизнес процесса в дереве'):
        bpms_event_page.tree.wait_selected_node_name(event_name)

    with allure.step(f'Удалить событие "{event_name}" в бизнес процессе "{bpms_name}" в дереве'):
        bpms_event_page.tree.delete_node(event_name, 'Событие', parent_node_name=bpms_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        bpms_event_page.tree.expand_node(test_folder_name)

    with allure.step(f'Проверить отсутствие события "{event_name}" в бизнес процессе "{bpms_name}"'):
        assert event_name not in bpms_event_page.tree.get_node_children_names(bpms_name)

    with allure.step(f'Проверить отсутствие события "{event_name}" в бизнес процессе {bpms_name} (API)'):
        assert event_name not in api.get_bpms_child_events(bpms_node_uuid)


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево бизнес процессов')
@allure.title('Управление задачами бизнес процессов')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Бизнес процессы',
        'name': 'Управление задачами бизнес процессов'
    })])
def test_admin_bpms_tasks_control(parametrized_login_admin_driver, parameters):
    bpms_task_page = BpmsTaskPage(parametrized_login_admin_driver)
    api = bpms_task_page.api_creator.get_api_bpms()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    task_name = "Задача BPMS"
    new_task_name = f"{task_name}_переименованная"

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве bpms через API'):
        test_folder_uuid = api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название бизнес процесса'):
        bpms_name = api.create_unique_bpms_name(f"{Vars.PKM_BASE_BPMS_NAME}_задачи")

    with allure.step(f'Создать бизнес процесс {bpms_name} в папке {test_folder_name} через API'):
        bpms_data = api.create_bpms(bpms_name, parent_uuid=test_folder_uuid)
        bpms_node_uuid = bpms_data.get('nodeUuid')

    with allure.step(f'Добавить бизнес процесс {bpms_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(BpmsNodeCreator(parametrized_login_admin_driver, bpms_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        bpms_task_page.tree.expand_node(test_folder_name)

    with allure.step(f'Создать задачу {task_name} в бизнес процессе {bpms_name}'):
        bpms_task_page.create_bpms_task(bpms_name, task_name)

    with allure.step(f'Переименовать задачу {task_name} на "{new_task_name}" на странице задачи'):
        bpms_task_page.tree.rename_node(task_name, new_task_name)
        # Включить переименование через страницу после исправления PKM-9375
        # bpms_page.rename_title(new_bpms_name)

    with allure.step(f'Проверить изменение названия задачи в дереве'):
        bpms_task_page.tree.wait_selected_node_name(new_task_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного названия задачи на странице задачи'):
        bpms_task_page.wait_page_title(new_task_name)

    with allure.step(f'Проверить изменение названия задачи в дереве'):
        bpms_task_page.tree.wait_selected_node_name(new_task_name)

    with allure.step(f'Переименовать задачу {new_task_name} на "{task_name}" в дереве'):
        bpms_task_page.tree.rename_node(new_task_name, task_name)

    with allure.step('Проверить отображение обновленного имени задачи на странице задачи'):
        bpms_task_page.wait_page_title(task_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени задачи на странице задачи'):
        bpms_task_page.wait_page_title(task_name)

    with allure.step(f'Проверить изменение названия задачи в дереве'):
        bpms_task_page.tree.wait_selected_node_name(task_name)

    with allure.step(f'Удалить задачу "{task_name}" в бизнес процессе "{bpms_name}" в дереве'):
        bpms_task_page.tree.delete_node(task_name, 'Задача', parent_node_name=bpms_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        bpms_task_page.tree.expand_node(test_folder_name)

    with allure.step(f'Проверить отсутствие задачи "{task_name}" в бизнес процессе "{bpms_name}"'):
        assert task_name not in bpms_task_page.tree.get_node_children_names(bpms_name)

    with allure.step(f'Проверить отсутствие задачи "{task_name}" в бизнес процессе "{bpms_name}" (API)'):
        assert task_name not in api.get_bpms_child_tasks(bpms_node_uuid)


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево бизнес процессов')
@allure.title('Управление шлюзами бизнес процессов')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_PROJECT_NAME,
        'tree_type': 'Бизнес процессы',
        'name': 'Управление шлюзами бизнес процессов'
    })])
def test_admin_bpms_gates_control(parametrized_login_admin_driver, parameters):
    bpms_gate_page = BpmsGatePage(parametrized_login_admin_driver)
    api = bpms_gate_page.api_creator.get_api_bpms()
    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    gate_name = "Шлюз BPMS"
    new_gate_name = f"{gate_name}_переименованный"

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве bpms через API'):
        test_folder_uuid = api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название бизнес процесса'):
        bpms_name = api.create_unique_bpms_name(f"{Vars.PKM_BASE_BPMS_NAME}_шлюзы")

    with allure.step(f'Создать бизнес процесс {bpms_name} в папке {test_folder_name} через API'):
        bpms_data = api.create_bpms(bpms_name, parent_uuid=test_folder_uuid)
        bpms_node_uuid = bpms_data.get('nodeUuid')

    with allure.step(f'Добавить бизнес процесс {bpms_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(BpmsNodeCreator(parametrized_login_admin_driver, bpms_node_uuid, delete_anyway=True))

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        bpms_gate_page.tree.expand_node(test_folder_name)

    with allure.step(f'Создать шлюз {gate_name} в бизнес процессе {bpms_name}'):
        bpms_gate_page.create_bpms_gate(bpms_name, gate_name)

    with allure.step(f'Переименовать шлюз {gate_name} на "{new_gate_name}" на странице шлюза'):
        bpms_gate_page.tree.rename_node(gate_name, new_gate_name)
        # Включить переименование через страницу после исправления PKM-9375
        # bpms_page.rename_title(new_bpms_name)

    with allure.step(f'Проверить изменение названия шлюза в дереве'):
        bpms_gate_page.tree.wait_selected_node_name(new_gate_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного названия шлюза на странице шлюза'):
        bpms_gate_page.wait_page_title(new_gate_name)

    with allure.step(f'Проверить изменение названия шлюза в дереве'):
        bpms_gate_page.tree.wait_selected_node_name(new_gate_name)

    with allure.step(f'Переименовать шлюз {new_gate_name} на "{gate_name}" в дереве'):
        bpms_gate_page.tree.rename_node(new_gate_name, gate_name)

    with allure.step('Проверить отображение обновленного имени шлюза на странице шлюза'):
        bpms_gate_page.wait_page_title(gate_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение обновленного имени шлюза на странице шлюза'):
        bpms_gate_page.wait_page_title(gate_name)

    with allure.step(f'Проверить изменение названия шлюза в дереве'):
        bpms_gate_page.tree.wait_selected_node_name(gate_name)

    with allure.step(f'Удалить шлюз "{gate_name}" в бизнес процессе "{bpms_name}" в дереве'):
        bpms_gate_page.tree.delete_node(gate_name, 'Шлюз', parent_node_name=bpms_name)

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'развернуть тестовую папку {test_folder_name}'):
        bpms_gate_page.tree.expand_node(test_folder_name)

    with allure.step(f'Проверить отсутствие шлюза "{gate_name}" в бизнес процессе "{bpms_name}"'):
        assert gate_name not in bpms_gate_page.tree.get_node_children_names(bpms_name)

    with allure.step(f'Проверить отсутствие шлюза "{gate_name}" в бизнес процессе "{bpms_name}" (API)'):
        assert gate_name not in api.get_bpms_child_gates(bpms_node_uuid)


@allure.feature('Интерфейс Администратора')
@allure.story('Дерево бизнес процессов')
@allure.title('Запуск бизнес процесса')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
    'login': 'eu_user',
    'project': Vars.PKM_PROJECT_NAME,
    'tree_type': 'Бизнес процессы',
    'name': 'Запуск бизнес процесса'
})])
def test_perform_bpms(parametrized_login_admin_driver, parameters):
    bpms_page = BpmsPage(parametrized_login_admin_driver)
    event_page = BpmsEventPage(parametrized_login_admin_driver)
    task_page = BpmsTaskPage(parametrized_login_admin_driver)
    gate_page = BpmsGatePage(parametrized_login_admin_driver)
    api = event_page.api_creator.get_api_bpms()
    tree = event_page.tree

    test_folder_name = Vars.PKM_TEST_FOLDER_NAME
    base_bpms_name = "Тестирование запуска BPMS"
    start_event_name = "Начальное событие"
    finish_event_name = "Завершающее событие"
    start_task_name = "Начальная задача"
    gate_name = "Шлюз процесса"
    gate_task_1_name = "Параллельная задача 1"
    gate_task_2_name = "Параллельная задача 2"

    with allure.step(f'Проверить наличие тестовой папки "{Vars.PKM_TEST_FOLDER_NAME}" в дереве bpms через API'):
        test_folder_uuid = api.check_test_folder(test_folder_name)

    with allure.step(f'Определить уникальное название бизнес процесса'):
        bpms_name = api.create_unique_bpms_name(base_bpms_name)

    with allure.step(f'Создать бизнес процесс {bpms_name} в папке {test_folder_name} через API'):
        bpms_data = api.create_bpms(bpms_name, parent_uuid=test_folder_uuid)
        bpms_node_uuid = bpms_data.get('nodeUuid')

    with allure.step(f'Добавить бизнес процесс {bpms_name} в список на удаление в постусловиях'):
        parametrized_login_admin_driver.test_data['to_delete'].append(
            BpmsNodeCreator(parametrized_login_admin_driver, bpms_node_uuid, delete_anyway=True))

    with allure.step(f'Развернуть тестовую папку {test_folder_name}'):
        tree.expand_node(test_folder_name)

    with allure.step(f'Создать начальное событие {start_event_name} в бизнес процессе {bpms_name}'):
        event_page.create_bpms_event(bpms_name, start_event_name)

    with allure.step(f'Создать начальную задачу {start_task_name} в бизнес процессе {bpms_name}'):
        task_page.create_bpms_task(bpms_name, start_task_name)

    with allure.step(f'Создать задачу шлюза {gate_task_1_name} в бизнес процессе {bpms_name}'):
        task_page.create_bpms_task(bpms_name, gate_task_1_name)

    with allure.step(f'Создать задачу шлюза {gate_task_2_name} в бизнес процессе {bpms_name}'):
        task_page.create_bpms_task(bpms_name, gate_task_2_name)

    with allure.step(f'Создать шлюз {gate_name} в бизнес процессе {bpms_name}'):
        gate_page.create_bpms_gate(bpms_name, gate_name)

    with allure.step(f'Создать завершающее событие {finish_event_name} в бизнес процессе {bpms_name}'):
        event_page.create_bpms_event(bpms_name, finish_event_name)

    with allure.step(f'Перейти к начальному событию {start_event_name}'):
        tree.select_node(start_event_name)

    with allure.step(f'Настроить начальное событие'):
        start_event_data = {
            'event_type': 'Начальное',
            'system_event_type': 'Ручное/внешнее',
            'next_element_type': 'Задача',
            'next_element_name': start_task_name
        }
        event_page.set_event(start_event_data)

    with allure.step(f'Перейти к завершающему событию {finish_event_name}'):
        tree.select_node(finish_event_name)

    with allure.step(f'Настроить завершающее событие'):
        finish_event_data = {
            'event_type': 'Завершающее'
        }
        event_page.set_event(finish_event_data)
