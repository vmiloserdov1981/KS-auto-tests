import allure
import pytest
from variables import PkmVars as Vars
from pages.class_po import ClassPage
from pages.dictionary_po import DictionaryPage
from pages.model_po import ModelPage
from pages.table_po import TablePage
from pages.object_po import ObjectPage
from pages.gantt_po import GanttPage, DiagramPage
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
    gantt_page = GanttPage(parametrized_login_admin_driver)
    diagram_page = DiagramPage(parametrized_login_admin_driver)
    #base_data = get_workshop_base_data(parametrized_login_admin_driver)
    base_data = {
    "class_1": {
        "name": "Мероприятие_4",
        "relations": {
            "relation_1": {
                "name": "Скважина мероприятия_4",
                "target_class_name": "Скважина_4",
            },
            "relation_2": {
                "name": "МТР мероприятия_4",
                "target_class_name": "МТР_4",
                "indicators": {
                    "indicator_1": {
                        "name": "График потребления, ед.",
                        "type": "Число",
                        "can_be_timed": True,
                        "formula": {
                            0: {
                                "type": "function",
                                "value": "ЕСЛИ",
                                "arguments": {
                                    0: {
                                        0: {
                                            "type": "function",
                                            "value": "И",
                                            "arguments": {
                                                0: {
                                                    0: {
                                                        "type": "indicator",
                                                        "value": "Дата начала",
                                                    },
                                                    1: {"type": "text", "value": ">="},
                                                    2: {
                                                        "type": "function",
                                                        "value": "НАЧАЛО ПЕРИОДА",
                                                    },
                                                },
                                                1: {
                                                    0: {
                                                        "type": "indicator",
                                                        "value": "Дата начала",
                                                    },
                                                    1: {"type": "text", "value": "<"},
                                                    2: {
                                                        "type": "function",
                                                        "value": "КОНЕЦ ПЕРИОДА",
                                                    },
                                                },
                                            },
                                        }
                                    },
                                    1: {
                                        0: {"type": "indicator", "value": "Потребление"}
                                    },
                                    2: {0: {"type": "text", "value": "0"}},
                                },
                            }
                        },
                    },
                    "indicator_2": {"name": "Потребление", "type": "Число"},
                },
            },
            "relation_3": {
                "name": "Персонал мероприятия_4",
                "target_class_name": "Персонал_4",
                "indicators": {
                    "indicator_1": {
                        "name": "Требуемая численность, чел.",
                        "type": "Число",
                    },
                    "indicator_2": {
                        "name": "График требуемой численности, чел.",
                        "type": "Число",
                        "formula": {
                            0: {
                                "type": "function",
                                "value": "ЕСЛИ",
                                "arguments": {
                                    0: {
                                        0: {
                                            "type": "function",
                                            "value": "И",
                                            "arguments": {
                                                0: {
                                                    0: {
                                                        "type": "function",
                                                        "value": "КОНЕЦ ПЕРИОДА",
                                                    },
                                                    1: {"type": "text", "value": ">"},
                                                    2: {
                                                        "type": "indicator",
                                                        "value": "Дата начала",
                                                    },
                                                },
                                                1: {
                                                    0: {
                                                        "type": "function",
                                                        "value": "НАЧАЛО ПЕРИОДА",
                                                    },
                                                    1: {"type": "text", "value": "<="},
                                                    2: {
                                                        "type": "indicator",
                                                        "value": "Дата окончания",
                                                    },
                                                },
                                            },
                                        }
                                    },
                                    1: {
                                        0: {
                                            "type": "indicator",
                                            "value": "Требуемая численность, чел.",
                                        }
                                    },
                                    2: {0: {"type": "text", "value": "0"}},
                                },
                            }
                        },
                    },
                },
            },
        },
        "indicators": {
            "indicator_1": {
                "name": "Дата начала",
                "type": "Дата",
                "can_be_timed": False,
            },
            "indicator_2": {
                "name": "Дата окончания",
                "type": "Дата",
                "can_be_timed": False,
            },
            "indicator_3": {
                "name": "Длительность",
                "type": "Число",
                "can_be_timed": False,
                "formula": {
                    0: {"type": "indicator", "value": "Дата окончания"},
                    1: {"type": "text", "value": "-"},
                    2: {"type": "indicator", "value": "Дата начала"},
                },
            },
            "indicator_4": {
                "name": "Тип работ",
                "type": "Справочник значений",
                "dictionary_name": "Типы работ_4",
                "can_be_timed": False,
            },
            "indicator_5": {"name": "Якорь", "type": "Логический"},
        },
    },
    "class_2": {
        "name": "Скважина_4",
        "indicators": {
            "indicator_1": {
                "name": "Тип",
                "type": "Справочник значений",
                "dictionary_name": "Типы скважин (конструкция)_4",
                "can_be_timed": False,
            }
        },
    },
    "class_3": {
        "name": "МТР_4",
        "indicators": {
            "indicator_1": {
                "name": "Тип",
                "type": "Справочник значений",
                "dictionary_name": "Типы МТР_4",
                "can_be_timed": False,
            },
            "indicator_2": {
                "name": "Нормативная стоимость, руб",
                "type": "Число",
                "format": "0,0.00",
                "can_be_timed": False,
            },
            "indicator_3": {
                "name": "Совокупный график потребности, ед.",
                "type": "Число",
                "can_be_timed": True,
                "formula": {
                    0: {"type": "indicator", "value": "График потребления, ед."}
                },
            },
            "indicator_4": {
                "name": "Совокупные затраты на МТР, руб.",
                "type": "Число",
                "can_be_timed": True,
                "formula": {
                    0: {"type": "indicator", "value": "Нормативная стоимость, руб"},
                    1: {"type": "text", "value": "*"},
                    2: {
                        "type": "indicator",
                        "value": "Совокупный график потребности, ед.",
                    },
                },
            },
        },
    },
    "class_4": {
        "name": "Персонал_4",
        "indicators": {
            "indicator_1": {
                "name": "Тип",
                "type": "Справочник значений",
                "dictionary_name": "Типы персонала_5",
                "can_be_timed": False,
            },
            "indicator_2": {
                "name": "Ставка, руб.",
                "type": "Число",
                "format": "0,0.00",
                "can_be_timed": False,
            },
            "indicator_3": {
                "name": "Совокупный график требуемой численности, чел.",
                "type": "Число",
                "can_be_timed": True,
                "formula": {
                    0: {
                        "type": "indicator",
                        "value": "График требуемой численности, чел.",
                    }
                },
            },
            "indicator_4": {
                "name": "Совокупные затраты на персонал, руб.",
                "type": "Число",
                "format": "0,0",
                "can_be_timed": True,
                "formula": {
                    0: {"type": "indicator", "value": "Ставка, руб."},
                    1: {"type": "text", "value": "*"},
                    2: {
                        "type": "indicator",
                        "value": "Совокупный график требуемой численности, чел.",
                    },
                },
            },
        },
    },
    "dictionary_1": {
        "name": "Типы персонала_5",
        "elements": {
            0: "Бригады бурения",
            1: "Бригады ТКРС",
            2: "Вспомогательный",
            3: "Управленческий",
        },
    },
    "dictionary_2": {
        "name": "Типы МТР_4",
        "elements": {
            0: "Долота",
            1: "Обсадные трубы",
            2: "Хим. реагенты",
            3: "Топливо",
            4: "ГСМ",
            5: "Прочие",
        },
    },
    "dictionary_3": {
        "name": "Типы скважин (конструкция)_4",
        "elements": {
            0: "Вертикальная",
            1: "Наклонно-направленная",
            2: "Горизонтальная",
        },
    },
    "dictionary_4": {
        "name": "Типы работ_4",
        "elements": {
            0: "Бурение",
            1: "ВМР (монтаж)",
            2: "Вспомогательный",
            3: "Управленческий",
        },
    },
    "model": {
        "name": "Планирование мероприятий_3",
        "datasets": {0: {"name": "План"}},
        "tables": {
            0: {
                "name": "Реестр персонала",
                "entities": [
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": (None, ["Персонал_4"]),
                    },
                    {
                        "name": "Наборы данных",
                        "entity_type": "Столбцы",
                        "values": ["План"],
                        "children": [
                            {
                                "name": "Показатели",
                                "entity_type": "Столбцы",
                                "values": ["Тип", "Ставка, руб."],
                                "parent_entity_name": "Наборы данных",
                            },
                            {
                                "name": "Показатели",
                                "entity_type": "Столбцы",
                                "values": [
                                    "Совокупный график требуемой численности, чел."
                                ],
                                "children": [
                                    {
                                        "name": "Временные измерения",
                                        "entity_type": "Столбцы",
                                        "parent_entity_name": "Показатели",
                                    }
                                ],
                                "parent_entity_name": "Наборы данных",
                            },
                        ],
                    },
                ],
                "check_data": {
                    "cols": [
                        "План",
                        "Ставка, руб.",
                        "Тип",
                        "Совокупный график требуемой численности, чел.",
                        "январь 2021",
                        "февраль 2021",
                        "март 2021",
                        "апрель 2021",
                        "май 2021",
                        "июнь 2021",
                        "июль 2021",
                        "август 2021",
                        "сентябрь 2021",
                        "октябрь 2021",
                        "ноябрь 2021",
                        "декабрь 2021",
                    ]
                },
            },
            1: {
                "name": "Реестр МТР",
                "entities": [
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": None,
                    },
                    {
                        "name": "Наборы данных",
                        "entity_type": "Столбцы",
                        "values": ["План"],
                        "children": [
                            {
                                "name": "Показатели",
                                "entity_type": "Столбцы",
                                "values": ["Тип", "Нормативная стоимость, руб"],
                                "parent_entity_name": "Наборы данных",
                            },
                            {
                                "name": "Показатели",
                                "entity_type": "Столбцы",
                                "values": ["Совокупный график потребности, ед."],
                                "children": [
                                    {
                                        "name": "Временные измерения",
                                        "entity_type": "Столбцы",
                                        "parent_entity_name": "Показатели",
                                    }
                                ],
                                "parent_entity_name": "Наборы данных",
                            },
                        ],
                    },
                ],
                "check_data": {
                    "cols": [
                        "План",
                        "Нормативная стоимость, руб",
                        "Тип",
                        "Совокупный график потребности, ед.",
                        "январь 2021",
                        "февраль 2021",
                        "март 2021",
                        "апрель 2021",
                        "май 2021",
                        "июнь 2021",
                        "июль 2021",
                        "август 2021",
                        "сентябрь 2021",
                        "октябрь 2021",
                        "ноябрь 2021",
                        "декабрь 2021",
                    ]
                },
            },
            2: {
                "name": "Расчет затрат",
                "entities": [
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": None,
                        "children": [
                            {
                                "name": "Показатели",
                                "entity_type": "Строки",
                                "alter_parent_name": "Объекты класса",
                                "values": ["Совокупные затраты на персонал, руб."],
                                "parent_entity_name": "Объекты класса",
                            }
                        ],
                    },
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": None,
                        "children": [
                            {
                                "name": "Показатели",
                                "entity_type": "Строки",
                                "alter_parent_name": "Объекты класса",
                                "values": ["Совокупные затраты на МТР, руб."],
                                "parent_entity_name": "Объекты класса",
                            }
                        ],
                    },
                    {
                        "name": "Наборы данных",
                        "values": ["План"],
                        "entity_type": "Столбцы",
                        "children": [
                            {
                                "name": "Временные измерения",
                                "entity_type": "Столбцы",
                                "parent_entity_name": "Наборы данных",
                            }
                        ],
                    },
                ],
                "check_data": {
                    "cols": [
                        "План",
                        "январь 2021",
                        "февраль 2021",
                        "март 2021",
                        "апрель 2021",
                        "май 2021",
                        "июнь 2021",
                        "июль 2021",
                        "август 2021",
                        "сентябрь 2021",
                        "октябрь 2021",
                        "ноябрь 2021",
                        "декабрь 2021",
                    ]
                },
            },
        },
        "gantt": {
            "name": "План мероприятий",
            "class": "Мероприятие_4",
            "start_indicator": "Дата начала",
            "end_indicator": "Дата окончания",
            "duration_indicator": "Длительность",
            "anchor_indicator": "Якорь",
            "additional_indicators": ["Тип работ"],
            "relations": {
                0: {
                    "name": "Персонал мероприятия",
                    "class": "Персонал мероприятия_4",
                    "search_indicators": None,
                    "input_indicators": ["Требуемая численность, чел."],
                },
                1: {
                    "name": "МТР мероприятия",
                    "class": "МТР мероприятия_4",
                    "search_indicators": None,
                    "input_indicators": ["Потребление"],
                },
            },
        },
        "model_period_type": "Месяц",
        "period_start_value": "Январь",
        "period_start_year": "2021",
        "periods_amount": "12",
        "last_period": "декабрь 2021",
    },
}
    base_data['model']['diagrams'] = {
            0: {
                "name": "Справочники. Навигация",
                "build_action": [
                    diagram_page.build_workshop_diagram_1,
                    {
                        0: {
                            "related_entity_type": "Таблица данных",
                            "related_entity_model": base_data["model"]["name"],
                            "related_table_name": base_data["model"]["tables"][0]["name"],
                            "entity_order": 1
                        },
                        1: {"related_entity_type": "Таблица данных",
                            "related_entity_model": base_data["model"]["name"],
                            "related_table_name": base_data["model"]["tables"][1]["name"],
                            "entity_order": 2
                            }
                    }
                ]
            },
            1: {"name": "Главное меню",
                "build_action": [
                    diagram_page.build_workshop_diagram_1
                ]
                }
        }
    base_data['model']['gantt']['relations'][0]['search_indicators'] = [base_data['class_4']['indicators']['indicator_1']['name']]
    base_data['model']['gantt']['relations'][1]['search_indicators'] = [base_data['class_3']['indicators']['indicator_1']['name']]

    '''
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
        with allure.step(f"Создать показатель {base_data['class_1']['indicators']['indicator_5']['name']} через дерево"):
            class_page.create_indicator(base_data['class_1']['indicators']['indicator_5']['name'], tree_parent_node=base_data["class_1"]["name"])
        with allure.step(f"Заполнить показатель {base_data['class_1']['indicators']['indicator_5']['name']} тестовыми данными"):
            class_page.set_indicator(base_data['class_1']['indicators']['indicator_5'])

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
            base_data['class_1']['indicators']['indicator_4']['name'],
            base_data['class_1']['indicators']['indicator_5']['name']
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

        
    with allure.step("Создать диаграмму Ганта"):
        gantt_page.create_gantt(base_data['model']['name'], base_data['model']['gantt']['name'])

    with allure.step("Настроить диаграмму Ганта"):
        gantt_page.set_gantt(base_data['model']['gantt'])

    with allure.step("Построить диаграмму Ганта"):
        gantt_page.build_gantt()

    with allure.step("Проверить отображение корректного набора данных на диаграмме"):
        assert gantt_page.events_plan_page.get_active_version_name() == 'По умолчанию'

    with allure.step('Создать мероприятие "Бурение" на диаграмме Ганта'):
        event_data = {
            'event_name': "Бурение",
            'start_day': '15',
            'duration': '3',
            'works_type': 'Бурение'
        }
        gantt_page.events_plan_page.create_event(event_data, check=False)

    with allure.step('Проверить отображение созданного мероприятия на диаграмме Ганта'):
        assert gantt_page.events_plan_page.get_events(names_only=True) == [event_data['event_name']]

    with allure.step('Проверить отображение созданного мероприятия в дереве'):
        gantt_page.tree.wait_child_node(base_data['model']['name'], event_data['event_name'])

    with allure.step('Обновить страницу'):
        parametrized_login_admin_driver.refresh()

    with allure.step('Проверить отображение созданного мероприятия на диаграмме Ганта'):
        assert gantt_page.events_plan_page.get_events(names_only=True) == [event_data['event_name']]

    with allure.step('Проверить отображение созданного мероприятия в дереве'):
        gantt_page.tree.wait_child_node(base_data['model']['name'], event_data['event_name'])
    '''
    dictionary_page.tree.switch_to_tree('Модели')
    gantt_page.tree.expand_node(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)

    with allure.step(f"Создать диаграмму {base_data['model']['diagrams'][0]['name']}"):
        diagram_page.build_diagram(base_data['model']['name'], base_data['model']['diagrams'][0]["name"], base_data['model']['diagrams'][0]["build_action"])
