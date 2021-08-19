import allure
import pytest
from variables import PkmVars as Vars
from pages.class_po import ClassPage
from pages.dictionary_po import DictionaryPage
from pages.model_po import ModelPage
from pages.table_po import TablePage
from pages.object_po import ObjectPage
from tests.workshop.base_data_creator import get_workshop_base_data


@allure.feature('Воркшоп')
@allure.story('Сценарий воркшопа')
@allure.title('Воркшоп тест')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_WORKSHOP_PROJECT_NAME,
        'tree_type': 'Справочники',
        'name': 'Воркшоп тест'
    })])
def test_workshop(parametrized_login_admin_driver, parameters):
    class_page = ClassPage(parametrized_login_admin_driver)
    dictionary_page = DictionaryPage(parametrized_login_admin_driver)
    model_page = ModelPage(parametrized_login_admin_driver)
    table_page = TablePage(parametrized_login_admin_driver)
    base_data = get_workshop_base_data(parametrized_login_admin_driver)

    with allure.step('Создать тестовые справочники'):
        with allure.step(f'Создать справочник {base_data["dictionary_1"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_1"]["name"])
        for element in base_data["dictionary_1"]["elements"]:
            with allure.step(f'Создать элемент справочника {base_data["dictionary_1"]["elements"][element]}'):
                dictionary_page.create_dict_element(base_data["dictionary_1"]["elements"][element])

        with allure.step(f'Создать справочник {base_data["dictionary_2"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_2"]["name"])
        for element in base_data["dictionary_2"]["elements"]:
            with allure.step(f'Создать элемент справочника {base_data["dictionary_2"]["elements"][element]}'):
                dictionary_page.create_dict_element(base_data["dictionary_2"]["elements"][element])

        with allure.step(f'Создать справочник {base_data["dictionary_3"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_3"]["name"])
        for element in base_data["dictionary_3"]["elements"]:
            with allure.step(f'Создать элемент справочника {base_data["dictionary_3"]["elements"][element]}'):
                dictionary_page.create_dict_element(base_data["dictionary_3"]["elements"][element])

        with allure.step(f'Создать справочник {base_data["dictionary_4"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_4"]["name"])
        for element in base_data["dictionary_4"]["elements"]:
            with allure.step(f'Создать элемент справочника {base_data["dictionary_4"]["elements"][element]}'):
                dictionary_page.create_dict_element(base_data["dictionary_4"]["elements"][element])

    with allure.step(f'Перейти к дереву классов'):
        class_page.tree.switch_to_tree('Классы')

    with allure.step(f'Создать класс {base_data["class_1"]["name"]}'):
        class_page.create_class(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["class_1"]["name"])

    with allure.step(f'Создать показатели класса {base_data["class_1"]["name"]}'):
        with allure.step(f"Создать показатель {base_data['class_1']['indicators']['indicator_1']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_1']['indicators']['indicator_1']['name'])
        with allure.step(f"Заполнить показатель {base_data['class_1']['indicators']['indicator_1']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_1']['indicators']['indicator_1'])
        with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_1"]["name"])
        with allure.step(f"Создать показатель {base_data['class_1']['indicators']['indicator_2']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_1']['indicators']['indicator_2']['name'])
        with allure.step(f"Заполнить показатель {base_data['class_1']['indicators']['indicator_2']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_1']['indicators']['indicator_2'])
        with allure.step(f"Создать показатель {base_data['class_1']['indicators']['indicator_3']['name']} через дерево"):
            class_page.create_indicator(base_data['class_1']['indicators']['indicator_3']['name'], tree_parent_node=base_data["class_1"]["name"])
        with allure.step(f"Заполнить показатель {base_data['class_1']['indicators']['indicator_3']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_1']['indicators']['indicator_3'])
        with allure.step(f"Создать показатель {base_data['class_1']['indicators']['indicator_4']['name']} через дерево"):
            class_page.create_indicator(base_data['class_1']['indicators']['indicator_4']['name'], tree_parent_node=base_data["class_1"]["name"])
        with allure.step(f"Заполнить показатель {base_data['class_1']['indicators']['indicator_4']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_1']['indicators']['indicator_4'])

    with allure.step(f'Создать класс {base_data["class_2"]["name"]}'):
        class_page.create_class(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["class_2"]["name"])

    with allure.step(f'Создать класс {base_data["class_3"]["name"]}'):
        class_page.create_class(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["class_3"]["name"])

    with allure.step(f'Создать класс {base_data["class_4"]["name"]}'):
        class_page.create_class(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["class_4"]["name"])

    with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_1"]["name"])

    with allure.step(f'Создать новый класс-связь {base_data["class_1"]["relations"]["relation_1"]["name"]} через страницу класса "{base_data["class_1"]["name"]}"'):
        relation_1 = class_page.create_relation(base_data["class_1"]["relations"]["relation_1"]["name"], base_data["class_1"]["relations"]["relation_1"]["target_class_name"])

    with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_1"]["name"])

    with allure.step(f'Создать новый класс-связь {base_data["class_1"]["relations"]["relation_2"]["name"]} через страницу класса "{base_data["class_1"]["name"]}"'):
        relation_2 = class_page.create_relation(base_data["class_1"]["relations"]["relation_2"]["name"], base_data["class_1"]["relations"]["relation_2"]["target_class_name"])

    with allure.step(f'Создать новый класс-связь "{base_data["class_1"]["relations"]["relation_3"]["name"]}" через дерево '):
        relation_3 = class_page.create_relation(base_data["class_1"]["relations"]["relation_3"]["name"], base_data["class_1"]["relations"]["relation_3"]["target_class_name"], tree_parent_node=base_data["class_1"]["name"])

    with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_1"]["name"])

    with allure.step(f'Проверить отображение всех созданных связей на странице класса'):
        actual_relations = class_page.get_class_relations()
        expected_relations = [base_data["class_1"]["relations"]["relation_1"]["name"], base_data["class_1"]["relations"]["relation_2"]["name"], base_data["class_1"]["relations"]["relation_3"]["name"]]
        assert class_page.compare_lists(actual_relations, expected_relations), 'На странице класса отображается некорректный список связей'

    with allure.step('Создать показатели связей'):
        with allure.step(f'Перейти к связи {base_data["class_1"]["relations"]["relation_2"]["name"]} через страницу класса'):
            class_page.select_relation(base_data["class_1"]["relations"]["relation_2"]["name"])

        with allure.step(f'Создать показатель связи {base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"]["name"]} через страницу связи'):
            class_page.create_relation_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"]["name"])
        with allure.step('Заполнить показатель тестовыми данными'):
            class_page.set_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"])

        with allure.step(f'Развернуть класс {base_data["class_1"]["name"]} через дерево'):
            class_page.tree.expand_node(base_data["class_1"]["name"])

        with allure.step(f'Перейти к связи {base_data["class_1"]["relations"]["relation_2"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_1"]["relations"]["relation_2"]["name"])

        with allure.step(f'Создать показатель связи {base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_1"]["name"]} через страницу связи'):
            class_page.create_relation_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_1"]["name"])
        with allure.step('Заполнить показатель тестовыми данными'):
            class_page.set_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_1"])

        with allure.step(f'Перейти к связи {base_data["class_1"]["relations"]["relation_3"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_1"]["relations"]["relation_3"]["name"])

        with allure.step(f'Создать показатель связи {base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_1"]["name"]} через страницу связи'):
            class_page.create_relation_indicator(base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_1"]["name"])
        with allure.step('Заполнить показатель тестовыми данными'):
            class_page.set_indicator(base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_1"])

        with allure.step(f'Перейти к связи {base_data["class_1"]["relations"]["relation_3"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_1"]["relations"]["relation_3"]["name"])

        with allure.step(f'Создать показатель связи {base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_2"]["name"]} через страницу связи'):
            class_page.create_relation_indicator(base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_2"]["name"])
        with allure.step('Заполнить показатель тестовыми данными'):
            class_page.set_indicator(base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_2"])

    with allure.step(f'Перейти к дереву классов'):
        class_page.tree.switch_to_tree('Классы')

    with allure.step(f'Развернуть тестовую папку {Vars.PKM_WORKSHOP_TEST_FOLDER_NAME}'):
        class_page.tree.expand_node(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)

    with allure.step(f'Перейти к классу {base_data["class_2"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_2"]["name"])

    with allure.step(f'Проверить отображение всех созданных связей на странице класса'):
        actual_relations = class_page.get_class_relations()
        expected_relations = [base_data['class_1']['relations']['relation_1']['name']]
        assert class_page.compare_lists(actual_relations, expected_relations), 'На странице класса отображается некорректный список связей'

    with allure.step(f'Создать показатели класса {base_data["class_2"]["name"]}'):
        with allure.step(f"Создать показатель {base_data['class_2']['indicators']['indicator_1']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_2']['indicators']['indicator_1']['name'])
        with allure.step(f"Заполнить показатель {base_data['class_2']['indicators']['indicator_1']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_2']['indicators']['indicator_1'])

    with allure.step(f'Перейти к классу {base_data["class_3"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_3"]["name"])

    with allure.step(f'Проверить отображение всех созданных связей на странице класса'):
        actual_relations = class_page.get_class_relations()
        expected_relations = [base_data['class_1']['relations']['relation_2']['name']]
        assert class_page.compare_lists(actual_relations, expected_relations), 'На странице класса отображается некорректный список связей'

    with allure.step(f'Создать показатели класса {base_data["class_3"]["name"]}'):
        with allure.step(f"Создать показатель {base_data['class_3']['indicators']['indicator_1']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_3']['indicators']['indicator_1']['name'])
        with allure.step(f"Заполнить показатель {base_data['class_3']['indicators']['indicator_1']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_3']['indicators']['indicator_1'])

        with allure.step(f'Перейти к классу {base_data["class_3"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_3"]["name"])

        with allure.step(f"Создать показатель {base_data['class_3']['indicators']['indicator_2']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_3']['indicators']['indicator_2']['name'])
        with allure.step(
                f"Заполнить показатель {base_data['class_3']['indicators']['indicator_2']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_3']['indicators']['indicator_2'])

        with allure.step(f"Создать показатель {base_data['class_3']['indicators']['indicator_3']['name']} через дерево"):
            class_page.create_indicator(base_data['class_3']['indicators']['indicator_3']['name'], tree_parent_node=base_data["class_3"]["name"])
        with allure.step(
                f"Заполнить показатель {base_data['class_3']['indicators']['indicator_3']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_3']['indicators']['indicator_3'])

        with allure.step(f"Создать показатель {base_data['class_3']['indicators']['indicator_4']['name']} через дерево"):
            class_page.create_indicator(base_data['class_3']['indicators']['indicator_4']['name'], tree_parent_node=base_data["class_3"]["name"])
        with allure.step(
                f"Заполнить показатель {base_data['class_3']['indicators']['indicator_4']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_3']['indicators']['indicator_4'])

    with allure.step(f'Перейти к классу {base_data["class_4"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_4"]["name"])

    with allure.step(f'Проверить отображение всех созданных связей на странице класса'):
        actual_relations = class_page.get_class_relations()
        expected_relations = [base_data['class_1']['relations']['relation_3']['name']]
        assert class_page.compare_lists(actual_relations, expected_relations), 'На странице класса отображается некорректный список связей'

    with allure.step(f'Создать показатели класса {base_data["class_4"]["name"]}'):
        with allure.step(
                f"Создать показатель {base_data['class_4']['indicators']['indicator_1']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_4']['indicators']['indicator_1']['name'])
        with allure.step(
                f"Заполнить показатель {base_data['class_4']['indicators']['indicator_1']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_4']['indicators']['indicator_1'])

        with allure.step(f'Перейти к классу {base_data["class_4"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_4"]["name"])

        with allure.step(
                f"Создать показатель {base_data['class_4']['indicators']['indicator_2']['name']} через страницу класса"):
            class_page.create_indicator(base_data['class_4']['indicators']['indicator_2']['name'])
        with allure.step(
                f"Заполнить показатель {base_data['class_4']['indicators']['indicator_2']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_4']['indicators']['indicator_2'])

        with allure.step(
                f"Создать показатель {base_data['class_4']['indicators']['indicator_3']['name']} через дерево"):
            class_page.create_indicator(base_data['class_4']['indicators']['indicator_3']['name'],
                                        tree_parent_node=base_data["class_4"]["name"])
        with allure.step(
                f"Заполнить показатель {base_data['class_4']['indicators']['indicator_3']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_4']['indicators']['indicator_3'])

        with allure.step(
                f"Создать показатель {base_data['class_4']['indicators']['indicator_4']['name']} через дерево"):
            class_page.create_indicator(base_data['class_4']['indicators']['indicator_4']['name'],
                                        tree_parent_node=base_data["class_4"]["name"])
        with allure.step(
                f"Заполнить показатель {base_data['class_4']['indicators']['indicator_4']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_4']['indicators']['indicator_4'])

    with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_1"]["name"])

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step(f'Проверить корректный список вложенных нод класса {base_data["class_1"]["name"]}'):
        expected_nodes = [
            base_data['class_1']['relations']['relation_1']['name'],
            base_data['class_1']['relations']['relation_2']['name'],
            base_data['class_1']['relations']['relation_3']['name'],
            base_data['class_1']['indicators']['indicator_1']['name'],
            base_data['class_1']['indicators']['indicator_2']['name'],
            base_data['class_1']['indicators']['indicator_3']['name'],
            base_data['class_1']['indicators']['indicator_4']['name']
        ]
        actual_nodes = class_page.tree.get_node_children_names(base_data["class_1"]["name"])
        assert class_page.compare_lists(actual_nodes, expected_nodes), 'Список вложенных нод не соответствует ожидаемому'

    with allure.step(f'Проверить корректный список вложенных нод класса {base_data["class_2"]["name"]}'):
        expected_nodes = [
            base_data['class_2']['indicators']['indicator_1']['name']
        ]
        actual_nodes = class_page.tree.get_node_children_names(base_data["class_2"]["name"])
        assert class_page.compare_lists(actual_nodes, expected_nodes), 'Список вложенных нод не соответствует ожидаемому'

    with allure.step(f'Проверить корректный список вложенных нод класса {base_data["class_3"]["name"]}'):
        expected_nodes = [
            base_data['class_3']['indicators']['indicator_1']['name'],
            base_data['class_3']['indicators']['indicator_2']['name'],
            base_data['class_3']['indicators']['indicator_3']['name'],
            base_data['class_3']['indicators']['indicator_4']['name'],
        ]
        actual_nodes = class_page.tree.get_node_children_names(base_data["class_3"]["name"])
        assert class_page.compare_lists(actual_nodes, expected_nodes), 'Список вложенных нод не соответствует ожидаемому'

    with allure.step(f'Проверить корректный список вложенных нод класса {base_data["class_4"]["name"]}'):
        expected_nodes = [
            base_data['class_4']['indicators']['indicator_1']['name'],
            base_data['class_4']['indicators']['indicator_2']['name'],
            base_data['class_4']['indicators']['indicator_3']['name'],
            base_data['class_4']['indicators']['indicator_4']['name'],
        ]
        actual_nodes = class_page.tree.get_node_children_names(base_data["class_4"]["name"])
        assert class_page.compare_lists(actual_nodes, expected_nodes), 'Список вложенных нод не соответствует ожидаемому'

    with allure.step(f'Перейти к дереву моделей'):
        class_page.tree.switch_to_tree('Модели')

    with allure.step(f'Создать модель {base_data["model"]["name"]}'):
        model_page.create_model(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["model"]["name"])

    with allure.step(f'Добавить набор данных {base_data["model"]["datasets"][0]["name"]} в модель'):
        model_page.create_dataset(base_data["model"]["datasets"][0]["name"])
        
    with allure.step(f'Задать тип временного интервала "{base_data["model"]["model_period_type"]}"'):
        model_page.set_model_period_type(f'{base_data["model"]["model_period_type"]}')

    with allure.step(f'Задать начальный период "{base_data["model"]["period_start_value"]}"'):
        model_page.set_start_period_month(base_data["model"]["period_start_value"])

    with allure.step(f'Указать количество периодов {base_data["model"]["periods_amount"]}'):
        model_page.set_period_amount(base_data["model"]["periods_amount"])

    with allure.step(f'Сохранить временной интервал'):
        model_page.save_model_period()
        
    #Убрать создание объектов после исправления PKM-7179
    object_page = ObjectPage(parametrized_login_admin_driver)
    object_page.create_object('1', base_data['model']['name'], base_data['class_1']['name'])
    object_page.create_object('2', base_data['model']['name'], base_data['class_2']['name'])
    object_page.create_object('3', base_data['model']['name'], base_data['class_3']['name'])
    object_page.create_object('4', base_data['model']['name'], base_data['class_4']['name'])

    with allure.step(f'Перейти к дереву моделей'):
        class_page.tree.switch_to_tree('Модели')

    with allure.step('развернуть папку автотестов'):
        model_page.tree.expand_node(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)

    with allure.step("раскрыть модель"):
        model_page.tree.expand_node(base_data['model']['name'])

    with allure.step(f'Создать таблицу {base_data["model"]["tables"][0]["name"]}'):
        table_page.build_table(base_data["model"]["name"], base_data["model"]["tables"][0]["name"], base_data["model"]["tables"][0]['entities'], check_data=base_data["model"]["tables"][0]['check_data'])

    with allure.step(f'Создать таблицу {base_data["model"]["tables"][1]["name"]}'):
        table_page.build_table(base_data["model"]["name"], base_data["model"]["tables"][1]["name"], base_data["model"]["tables"][1]['entities'], check_data=base_data["model"]["tables"][1]['check_data'])

    with allure.step(f'Создать таблицу {base_data["model"]["tables"][2]["name"]}'):
        table_page.build_table(base_data["model"]["name"], base_data["model"]["tables"][2]["name"], base_data["model"]["tables"][2]['entities'], check_data=base_data["model"]["tables"][2]['check_data'])
