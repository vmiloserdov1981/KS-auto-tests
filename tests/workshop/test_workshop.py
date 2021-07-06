import allure
import pytest
from variables import PkmVars as Vars
from pages.class_po import ClassPage
from pages.dictionary_po import DictionaryPage


@allure.feature('Воркшоп')
@allure.story('Сценарий воркшопа')
@allure.title('Воркшоп тест')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("parameters", [({
        'login': 'eu_user',
        'project': Vars.PKM_WORKSHOP_PROJECT_NAME,
        'tree_type': 'Классы',
        'name': 'Воркшоп тест'
    })])
def test_workshop(parametrized_login_admin_driver, parameters):
    class_page = ClassPage(parametrized_login_admin_driver)
    dictionary_page = DictionaryPage(parametrized_login_admin_driver)
    class_api = class_page.api_creator.get_api_classes()
    dictionaries_api = class_page.api_creator.get_api_dictionaries()

    classes_tree_nodes = class_api.get_tree_nodes()
    dicts_tree_nodes = dictionaries_api.api_get_dicts_names()

    base_data = {
        'class_1': {
            'name': class_api.create_unique_class_name('Мероприятие', nodes=classes_tree_nodes),
        },
        'class_2': {
            'name': class_api.create_unique_class_name('Скважина', nodes=classes_tree_nodes),
            'indicators': {
                'indicator_1': {
                    'name': 'yo'
                },
                'indicator_2': {
                    'name': 'ye'
                }
            }

        },
        'class_3': {
            'name': class_api.create_unique_class_name('МТР', nodes=classes_tree_nodes),
            'indicators': {
                'indicator_1': {
                    'name': 'yo'
                },
                'indicator_2': {
                    'name': 'ye'
                }
            }

        },
        'class_4': {
            'name': class_api.create_unique_class_name('Персонал', nodes=classes_tree_nodes),
            'indicators': {
                'indicator_1': {
                    'name': 'yo'
                },
                'indicator_2': {
                    'name': 'ye'
                }
            }

        },
        'dictionary_1': {
            'name': dictionaries_api.create_unique_dict_name('Типы персонала', dicts_nodes=dicts_tree_nodes),
            'elements': {
                'element_1': 'Бригады бурения',
                'element_2': 'Бригады ТКРС',
                'element_3': 'Вспомогательный',
                'element_4': 'Управленческий'
            }
        },
        'dictionary_2': {
            'name': dictionaries_api.create_unique_dict_name('Типы МТР', dicts_nodes=dicts_tree_nodes),
            'elements': {
                'element_1': 'Долота',
                'element_2': 'Обсадные трубы',
                'element_3': 'Хим. реагенты',
                'element_4': 'Топливо',
                'element_5': 'ГСМ',
                'element_6': 'Прочие',
            }
        },
        'dictionary_3': {
            'name': dictionaries_api.create_unique_dict_name('Типы скважин (конструкция)', dicts_nodes=dicts_tree_nodes),
            'elements': {
                'element_1': 'Вертикальная',
                'element_2': 'Наклонно-направленная',
                'element_3': 'Горизонтальная'
            }
        },
        'dictionary_4': {
            'name': dictionaries_api.create_unique_dict_name('Типы работ', dicts_nodes=dicts_tree_nodes),
            'elements': {
                'element_1': 'Бурение',
                'element_2': 'ВМР (монтаж)',
                'element_3': 'Вспомогательный',
                'element_4': 'Управленческий'
            }
        },
    }
    base_data['class_1']['relations'] = {
        'relation_1': {
            'name': class_api.create_unique_class_name('Скважина мероприятия', nodes=classes_tree_nodes),
            'target_class_name': base_data['class_2']['name']
        },
        'relation_2': {
            'name': class_api.create_unique_class_name('МТР мероприятия', nodes=classes_tree_nodes),
            'target_class_name': base_data['class_3']['name'],
            'indicators': {
                'indicator_1': {
                    'name': 'График потребления, ед.',
                    'type': 'Число',
                    'can_be_timed': True,
                    'formula': {
                                0: {
                                    "type": "function",
                                    "value": "ЕСЛИ",
                                    "arguments": {
                                        "Условие": {
                                            0: {
                                                "type": "function",
                                                "value": "И",
                                                "arguments": {
                                                    'выражение 1': {
                                                        0: {"type": "indicator", "value": "Дата начала"},
                                                        1: {"type": "text", "value": ">="},
                                                        2: {"type": "function", "value": "НАЧАЛО ПЕРИОДА"}
                                                    },
                                                    'выражение 2': {
                                                        0: {"type": "indicator", "value": "Дата начала"},
                                                        1: {"type": "text", "value": "<"},
                                                        2: {"type": "function", "value": "КОНЕЦ ПЕРИОДА"}
                                                    }
                                                }
                                            }
                                        },
                                        "Истина": {
                                            0: {"type": "indicator", "value": "Потребление"}
                                        },
                                        "Ложь": {
                                            0: {"type": "text", "value": "0"}
                                        },
                                    },
                                }
                            }
                },
                'indicator_2': {
                    'name': 'Потребление',
                    'type': 'Число'
                }
            }
        },
        'relation_3': {
            'name': class_api.create_unique_class_name('Персонал мероприятия', nodes=classes_tree_nodes),
            'target_class_name': base_data['class_4']['name'],
            'indicators': {
                'indicator_1': {
                    'name': 'Требуемая численность, чел.',
                    'type': 'Число'
                },
                'indicator_2': {
                    'name': 'График требуемой численности, чел.',
                    'type': 'Число'
                }
            }
        },

    }

    base_data['class_1']['indicators'] = {
                'indicator_1': {
                    'name': 'Дата начала',
                    'type': 'Дата',
                    'can_be_timed': False
                },
                'indicator_2': {
                    'name': 'Дата окончания',
                    'type': 'Дата',
                    'can_be_timed': False
                },
                'indicator_3': {
                    'name': 'Длительность',
                    'type': 'Число',
                    'can_be_timed': False
                },
                'indicator_4': {
                    'name': 'Тип работ',
                    'type': 'Справочник значений',
                    'dictionary_name': base_data['dictionary_4']['name'],
                    'can_be_timed': False
                },
            }

    base_data['class_2']['indicators'] = {
        'indicator_1': {
            'name': 'Тип',
            'type': 'Справочник значений',
            'dictionary_name': base_data['dictionary_3']['name'],
            'can_be_timed': False
        }
    }

    base_data['class_3']['indicators'] = {
        'indicator_1': {
            'name': 'Тип',
            'type': 'Справочник значений',
            'dictionary_name': base_data['dictionary_2']['name'],
            'can_be_timed': False
        },
        'indicator_2': {
            'name': 'Нормативная стоимость, руб',
            'type': 'Число',
            'format': '0,0.00',
            'can_be_timed': False
        },
        'indicator_3': {
            'name': 'Совокупный график потребности, ед.',
            'type': 'Число',
            'can_be_timed': True
        },
        'indicator_4': {
            'name': 'Совокупные затраты на МТР, руб.',
            'type': 'Число',
            'can_be_timed': True
        }
    }

    base_data['class_4']['indicators'] = {
        'indicator_1': {
            'name': 'Тип',
            'type': 'Справочник значений',
            'dictionary_name': base_data['dictionary_1']['name'],
            'can_be_timed': False
        },
        'indicator_2': {
            'name': 'Ставка, руб',
            'type': 'Число',
            'format': '0,0.00',
            'can_be_timed': False
        },
        'indicator_3': {
            'name': 'Совокупный график требуемой численности, чел.',
            'type': 'Число',
            'can_be_timed': True
        },
        'indicator_4': {
            'name': 'Совокупные затраты на персонал, руб.',
            'type': 'Число',
            'format': '0,0',
            'can_be_timed': True
        },
    }

    with allure.step(f'Создать класс {base_data["class_1"]["name"]}'):
        class_page.create_class(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["class_1"]["name"])

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

    with allure.step(f'Перейти к дереву справочников'):
        class_page.tree.switch_to_tree('Справочники')

    with allure.step('Создать тестовые справочники'):
        with allure.step(f'Создать справочник {base_data["dictionary_1"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_1"]["name"])

        with allure.step(f'Создать справочник {base_data["dictionary_2"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_2"]["name"])

        with allure.step(f'Создать справочник {base_data["dictionary_3"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_3"]["name"])

        with allure.step(f'Создать справочник {base_data["dictionary_4"]["name"]}'):
            dictionary_page.create_dictionary(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME, base_data["dictionary_4"]["name"])

    with allure.step(f'Перейти к дереву классов'):
        class_page.tree.switch_to_tree('Классы')

    with allure.step(f'Развернуть тестовую папку {Vars.PKM_WORKSHOP_TEST_FOLDER_NAME}'):
        class_page.tree.expand_node(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)

    with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
        class_page.tree.select_node(base_data["class_1"]["name"])

    with allure.step('Создать показатели связей'):
        with allure.step(f'Перейти к связи {base_data["class_1"]["relations"]["relation_2"]["name"]} через страницу класса'):
            class_page.select_relation(base_data["class_1"]["relations"]["relation_2"]["name"])

        with allure.step(f'Создать показатель связи {base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_1"]["name"]} через страницу связи'):
            class_page.create_relation_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_1"]["name"])
        with allure.step('Заполнить показатель тестовыми данными'):
            class_page.set_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_1"])

        with allure.step(f'Развернуть класс {base_data["class_1"]["name"]} через дерево'):
            class_page.tree.expand_node(base_data["class_1"]["name"])

        with allure.step(f'Перейти к связи {base_data["class_1"]["relations"]["relation_2"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_1"]["relations"]["relation_2"]["name"])

        with allure.step(f'Создать показатель связи {base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"]["name"]} через страницу связи'):
            class_page.create_relation_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"]["name"])
        with allure.step('Заполнить показатель тестовыми данными'):
            class_page.set_indicator(base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"])

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

    with allure.step(f'Создать показатели класса {base_data["class_1"]["name"]}'):
        with allure.step(f'Перейти к классу {base_data["class_1"]["name"]} через дерево'):
            class_page.tree.select_node(base_data["class_1"]["name"])

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
