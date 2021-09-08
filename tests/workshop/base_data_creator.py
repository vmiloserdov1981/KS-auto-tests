from pages.class_po import ClassPage
from pages.model_po import ModelPage
from pages.table_po import TablePage
from pages.gantt_po import DiagramPage


def get_workshop_base_data(driver):
    class_page = ClassPage(driver)
    model_page = ModelPage(driver)
    table_page = TablePage(driver)
    diagram_page = DiagramPage(driver)
    class_api = class_page.api_creator.get_api_classes()
    dictionaries_api = class_page.api_creator.get_api_dictionaries()
    models_api = model_page.api_creator.get_api_models()
    dashboards_api = model_page.api_creator.get_api_dashboards()
    classes_tree_nodes = class_api.get_tree_nodes()
    dicts_tree_nodes = dictionaries_api.api_get_dicts_names()

    base_data = {
        'class_1': {
            'name': class_api.create_unique_class_name('Мероприятие', nodes=classes_tree_nodes),
        },
        'class_2': {
            'name': class_api.create_unique_class_name('Скважина', nodes=classes_tree_nodes)
        },
        'class_3': {
            'name': class_api.create_unique_class_name('МТР', nodes=classes_tree_nodes)
        },
        'class_4': {
            'name': class_api.create_unique_class_name('Персонал', nodes=classes_tree_nodes)
        },
        'dictionary_1': {
            'name': dictionaries_api.create_unique_dict_name('Типы персонала', dicts_nodes=dicts_tree_nodes),
            'elements': {
                0: 'Бригады бурения',
                1: 'Бригады ТКРС',
                2: 'Вспомогательный',
                3: 'Управленческий'
            }
        },
        'dictionary_2': {
            'name': dictionaries_api.create_unique_dict_name('Типы МТР', dicts_nodes=dicts_tree_nodes),
            'elements': {
                0: 'Долота',
                1: 'Обсадные трубы',
                2: 'Хим. реагенты',
                3: 'Топливо',
                4: 'ГСМ',
                5: 'Прочие',
            }
        },
        'dictionary_3': {
            'name': dictionaries_api.create_unique_dict_name('Типы скважин (конструкция)',
                                                             dicts_nodes=dicts_tree_nodes),
            'elements': {
                0: 'Вертикальная',
                1: 'Наклонно-направленная',
                2: 'Горизонтальная'
            }
        },
        'dictionary_4': {
            'name': dictionaries_api.create_unique_dict_name('Типы работ', dicts_nodes=dicts_tree_nodes),
            'elements': {
                0: 'Бурение',
                1: 'ВМР (монтаж)',
                2: 'Вспомогательный',
                3: 'Управленческий'
            }
        }
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
                                0: {
                                    0: {
                                        "type": "function",
                                        "value": "И",
                                        "arguments": {
                                            0: {
                                                0: {"type": "indicator", "value": "Дата начала"},
                                                1: {"type": "text", "value": ">="},
                                                2: {"type": "function", "value": "НАЧАЛО ПЕРИОДА"}
                                            },
                                            1: {
                                                0: {"type": "indicator", "value": "Дата начала"},
                                                1: {"type": "text", "value": "<"},
                                                2: {"type": "function", "value": "КОНЕЦ ПЕРИОДА"}
                                            }
                                        }
                                    }
                                },
                                1: {
                                    0: {"type": "indicator", "value": "Потребление"}
                                },
                                2: {
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
                    'type': 'Число',
                    'formula': {
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
                                                0: {"type": "function", "value": "КОНЕЦ ПЕРИОДА"},
                                                1: {"type": "text", "value": ">"},
                                                2: {"type": "indicator", "value": "Дата начала"}
                                            },
                                            1: {
                                                0: {"type": "function", "value": "НАЧАЛО ПЕРИОДА"},
                                                1: {"type": "text", "value": "<="},
                                                2: {"type": "indicator", "value": "Дата окончания"}
                                            },
                                        }
                                    }
                                },
                                1: {
                                    0: {"type": "indicator", "value": "Требуемая численность, чел."}
                                },
                                2: {
                                    0: {"type": "text", "value": "0"}
                                },
                            },
                        }
                    }
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
            'can_be_timed': False,
            'formula': {
                0: {"type": "indicator", "value": "Дата окончания"},
                1: {"type": "text", "value": "-"},
                2: {"type": "indicator", "value": "Дата начала"}
            }
        },
        'indicator_4': {
            'name': 'Тип работ',
            'type': 'Справочник значений',
            'dictionary_name': base_data['dictionary_4']['name'],
            'can_be_timed': False
        },
        'indicator_5': {
            'name': 'Якорь',
            'type': 'Логический'
        }
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
            'can_be_timed': True,
            'formula': {0: {"type": "indicator", "value": "График потребления, ед."}}
        },
        'indicator_4': {
            'name': 'Совокупные затраты на МТР, руб.',
            'type': 'Число',
            'can_be_timed': True,
            'formula': {
                0: {"type": "indicator", "value": "Нормативная стоимость, руб"},
                1: {"type": "text", "value": "*"},
                2: {"type": "indicator", "value": "Совокупный график потребности, ед."},
            }
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
            'name': 'Ставка, руб.',
            'type': 'Число',
            'format': '0,0.00',
            'can_be_timed': False
        },
        'indicator_3': {
            'name': 'Совокупный график требуемой численности, чел.',
            'type': 'Число',
            'can_be_timed': True,
            'formula': {0: {"type": "indicator", "value": "График требуемой численности, чел."}}
        },
        'indicator_4': {
            'name': 'Совокупные затраты на персонал, руб.',
            'type': 'Число',
            'format': '0,0',
            'can_be_timed': True,
            'formula': {
                0: {"type": "indicator", "value": "Ставка, руб."},
                1: {"type": "text", "value": "*"},
                2: {"type": "indicator", "value": "Совокупный график требуемой численности, чел."},
            }
        },
    }

    base_data['model'] = {
        "name": models_api.create_unique_model_name("Планирование мероприятий"),
        "datasets": {0: {"name": "План"}},
        "tables": {
            0: {
                "name": "Реестр персонала",
                "entities": [
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": (
                            table_page.objects_modal.set_class_objects, [base_data['class_4']['name']],
                        ),
                    },
                    {
                        "name": "Наборы данных",
                        "entity_type": "Столбцы",
                        "values": ["План"],
                        "children": [
                            {"name": "Показатели", "entity_type": "Столбцы", "values": [base_data['class_4']['indicators']['indicator_1']['name'], base_data['class_4']['indicators']['indicator_2']['name']]},
                            {"name": "Показатели", "entity_type": "Столбцы", "values": [base_data['class_4']['indicators']['indicator_3']['name']],
                             "children": [{"name": "Временные измерения", "entity_type": "Столбцы"}]}
                        ],
                    }
                ],
                "check_data": {
                    "cols": ['План', 'Ставка, руб.', 'Тип', 'Совокупный график требуемой численности, чел.', 'январь 2021', 'февраль 2021', 'март 2021', 'апрель 2021', 'май 2021', 'июнь 2021', 'июль 2021', 'август 2021', 'сентябрь 2021', 'октябрь 2021', 'ноябрь 2021', 'декабрь 2021']
                }
            },
            1: {
                "name": "Реестр МТР",
                "entities": [
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": (
                            table_page.objects_modal.set_class_objects, [base_data['class_3']['name']],
                        ),
                    },
                    {
                        "name": "Наборы данных",
                        "entity_type": "Столбцы",
                        "values": ["План"],
                        "children": [
                            {"name": "Показатели", "entity_type": "Столбцы",
                             "values": [base_data['class_3']['indicators']['indicator_1']['name'],
                                        base_data['class_3']['indicators']['indicator_2']['name']]},
                            {"name": "Показатели", "entity_type": "Столбцы",
                             "values": [base_data['class_3']['indicators']['indicator_3']['name']],
                             "children": [{"name": "Временные измерения", "entity_type": "Столбцы"}]}
                        ],
                    }
                ],
                "check_data": {
                    "cols": ['План', 'Нормативная стоимость, руб', 'Тип', 'Совокупный график потребности, ед.', 'январь 2021', 'февраль 2021', 'март 2021', 'апрель 2021', 'май 2021', 'июнь 2021', 'июль 2021', 'август 2021', 'сентябрь 2021', 'октябрь 2021', 'ноябрь 2021', 'декабрь 2021']
                }
            },
            2: {
                "name": "Расчет затрат",
                "entities": [
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": (table_page.objects_modal.set_class_objects, [base_data['class_4']['name']]),
                        "children": [{"name": "Показатели", "entity_type": "Строки", "alter_parent_name": "Объекты класса",
                                      "values": [base_data['class_4']['indicators']['indicator_4']['name']]}]
                    },
                    {
                        "name": "Настройка объекта",
                        "entity_type": "Строки",
                        "additional_action": (table_page.objects_modal.set_class_objects, [base_data['class_3']['name']]),
                        "children": [{"name": "Показатели", "entity_type": "Строки", "alter_parent_name": "Объекты класса",
                                      "values": [base_data['class_3']['indicators']['indicator_4']['name']]}]
                    },
                    {
                        "name": "Наборы данных",
                        "values": ["План"],
                        "entity_type": "Столбцы",
                        "children": [{"name": "Временные измерения", "entity_type": "Столбцы"}],
                    }
                ],
                "check_data": {
                    "cols": ['План', 'январь 2021', 'февраль 2021', 'март 2021', 'апрель 2021', 'май 2021', 'июнь 2021', 'июль 2021', 'август 2021', 'сентябрь 2021', 'октябрь 2021', 'ноябрь 2021', 'декабрь 2021']
                }
            }
        },
        "gantt": {
        "name": 'План мероприятий',
        "class": base_data['class_1']['name'],
        "start_indicator": base_data['class_1']['indicators']['indicator_1']['name'],
        "end_indicator": base_data['class_1']['indicators']['indicator_2']['name'],
        "duration_indicator": base_data['class_1']['indicators']['indicator_3']['name'],
        "anchor_indicator": base_data['class_1']['indicators']['indicator_5']['name'],
        "additional_indicators": [base_data['class_1']['indicators']['indicator_4']['name']],
        "relations": {
            0: {
                "name": "Персонал мероприятия",
                "class": base_data["class_1"]["relations"]["relation_3"]["name"],
                "input_indicators": [base_data["class_1"]["relations"]["relation_3"]["indicators"]["indicator_1"]["name"]],
                "search_indicators": [base_data['class_4']['indicators']['indicator_1']['name']]
            },
            1: {
                "name": "МТР мероприятия",
                "class": base_data["class_1"]["relations"]["relation_2"]["name"],
                "search_indicators": [base_data['class_3']['indicators']['indicator_1']['name']],
                "input_indicators": [base_data["class_1"]["relations"]["relation_2"]["indicators"]["indicator_2"]["name"]]
            }
        }
    },
        "model_period_type": "Месяц",
        "period_start_value": "Январь",
        "period_start_year": "2021",
        "periods_amount": "12",
        "last_period": "декабрь 2021"
    }

    base_data['model']['diagrams'] = {
        0: {
            "name": model_page.api_creator.get_api_models().create_unique_diagram_name("Справочники. Навигация"),
            "build_action": [
                diagram_page.build_workshop_dictionaries_diagram,
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
        1: {"name": model_page.api_creator.get_api_models().create_unique_diagram_name("Главное меню"),
            "build_action": [
                diagram_page.build_workshop_menu_diagram, None
            ]
            }
    }
    base_data["dashboards"] = {
        0: {
            "name": dashboards_api.create_unique_dashboard_name("Меню")
        },
        1: {
            "name": dashboards_api.create_unique_dashboard_name("Справочники")
        }
    }

    return base_data
