import time

from pages.components.entity_page import EntityPage
from pages.components.trees import NewTree
from pages.components.modals import Modals
from pages.events_plan_po import EventsPlan
from selenium.webdriver.common.by import By
import allure


class GanttPage(EntityPage):
    LOCATOR_CONSTRUCTOR_CLASS_INPUT = (By.XPATH, "//async-dropdown-search[@formcontrolname='classUuid']//input")
    LOCATOR_ENTITY_PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'gantt__header')]//div[contains(@class, 'title')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)
        self.events_plan_page = EventsPlan(driver)

    def wait_page_title(self, page_title: str, timeout: int = 10):
        self.wait_until_text_in_element(self.LOCATOR_ENTITY_PAGE_TITLE, page_title, time=timeout)

    def create_gantt(self, model_name, gantt_name):
        with allure.step(f'Создать диаграмму Ганта {gantt_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(model_name), time=20)
            self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
            self.find_and_click(self.tree.submenu_option_locator_creator('Диаграмма Ганта'))
        with allure.step(f'Укзать название диаграммы Ганта {gantt_name} и создать ее'):
            self.modal.enter_and_save(gantt_name)
        with allure.step(f'Проверить отображение диаграммы Ганта {gantt_name} в дереве выбранной'):
            self.tree.wait_selected_node_name(gantt_name)
        with allure.step(f'Проверить переход на страницу диаграммы Ганта'):
            self.wait_page_title(gantt_name.upper())

    def set_gantt_class(self, class_name: str):
        self.find_and_enter(self.LOCATOR_CONSTRUCTOR_CLASS_INPUT, class_name)
        item_locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .=' {class_name} ']")
        self.find_and_click(item_locator)
        actual_value = self.find_element(self.LOCATOR_CONSTRUCTOR_CLASS_INPUT).get_attribute('value')
        assert actual_value == class_name

    def set_gantt(self, gantt_data):
        """
                gantt_data = {
                "name": 'План мероприятий',
                "class": 'hi',
                "start_indicator": 'hi',
                "end_indicator": 'hi',
                "duration_indicator": 'hi',
                "anchor_indicator": 'hi',
                "additional_indicators": ['hi'],
                "relations": {
                    0: {
                        "name": "Персонал мероприятия",
                        "class": 'hi',
                        "search_indicators": [],
                        "input_indicators": ['hi']
                    },
                    1: {
                        "name": "МТР мероприятия",
                        "class": 'hi',
                        "search_indicators": ['hi'],
                        "input_indicators": ['hi']
                    }
                }
            }
        """
        class_name = gantt_data.get("class")
        start_indicator = gantt_data.get("start_indicator")
        end_indicator = gantt_data.get("end_indicator")
        duration_indicator = gantt_data.get("duration_indicator")
        anchor_indicator = gantt_data.get("anchor_indicator")
        additional_indicators = gantt_data.get("additional_indicators")
        relations = gantt_data.get("relations")

        assert class_name
        assert start_indicator
        assert end_indicator
        assert duration_indicator
        assert anchor_indicator

        with allure.step("Указать класс"):
            self.set_gantt_class(class_name)

        with allure.step("Настроить показатель старта мероприятий"):
            self.set_gantt_required_indicator('Дата начала*', start_indicator)

        with allure.step("Настроить показатель окончания мероприятий"):
            self.set_gantt_required_indicator('Дата окончания*', end_indicator)

        with allure.step("Настроить показатель длительности мероприятий"):
            self.set_gantt_required_indicator('Длительность*', duration_indicator)

        with allure.step("Настроить якорный показатель"):
            self.set_gantt_required_indicator('Якорное мероприятие', anchor_indicator)

        if additional_indicators:
            with allure.step("Настроить дополнительные показатели"):
                self.set_additional_indicators(additional_indicators)
        if relations:
            with allure.step("Настроить связи"):
                self.set_gantt_relations(relations)

    def set_gantt_relation(self, relation_data: dict):
        '''
        relations_data = {
                "name": "МТР мероприятия",
                "class": 'name',
                "search_indicators": ['name'],
                "input_indicators": ['name']
            }
        '''
        relation_name = relation_data.get('name')
        relation_class_name = relation_data.get('class')
        search_indicators = relation_data.get('search_indicators') or []
        input_indicators = relation_data.get('input_indicators') or []

        add_relation_button_locator = self.add_entity_button_locator_creator('Связи')
        relations_block_xpath = "//div[@class='list' and .//div[@class='list-header' and .='Связи']]"
        name_field_locator = (By.XPATH, f"({relations_block_xpath}//div[@class='form-col' and .//div[.='Имя']]//input)[last()]")
        relation_class_name_field_locator = (By.XPATH, f"({relations_block_xpath}//div[@class='form-col' and .//div[.='Класс-связь']]//input)[last()]")
        search_indicators_field_locator = (By.XPATH, f"({relations_block_xpath}//div[@class='form-col' and .//div[.='Показатели для поиска']]//input)[last()]")
        input_indicators_field_locator = (By.XPATH, f"({relations_block_xpath}//div[@class='form-col' and .//div[.='Показатели для ввода данных']]//input)[last()]")

        if relation_name:
            self.find_and_click(add_relation_button_locator)
            self.find_and_enter(name_field_locator, relation_name)
        if relation_class_name:
            self.find_and_click(relation_class_name_field_locator)
            self.find_and_click(self.dropdown_value_locator_creator(relation_class_name))
        if search_indicators:
            self.find_and_click(search_indicators_field_locator)
            for indicator in search_indicators:
                locator = (By.XPATH, f"//div[contains(@class, 'multi-select__item') and .=' {indicator} ']")
                self.find_and_click(locator)
        if input_indicators:
            self.find_and_click(input_indicators_field_locator)
            for indicator in input_indicators:
                locator = (By.XPATH, f"//div[contains(@class, 'multi-select__item') and .=' {indicator} ']")
                self.find_and_click(locator)

        self.find_and_click((By.XPATH, relations_block_xpath))
        time.sleep(1)

    def set_gantt_relations(self, relations: dict):
        '''
        relations_data = [{
                "name": "МТР мероприятия",
                "class": 'name',
                "search_indicators": ['name'],
                "input_indicators": ['name']
            },
            {
                "name": "МТР мероприятия",
                "class": 'name',
                "search_indicators": ['name'],
                "input_indicators": ['name']
            }]
        '''
        for i in relations:
            self.set_gantt_relation(relations[i])

    def set_gantt_required_indicator(self, indicator_name: str, indicator_value: str):
        input_locator = (By.XPATH, f"//pkm-gant-settings//div[contains(@class, 'form-col') and .//*[.='{indicator_name}']]//input")
        actual_input_value = (By.XPATH, f"//pkm-gant-settings//div[contains(@class, 'form-col') and .//*[.='{indicator_name}']]//div[contains(@class, 'display-value-text')]")
        value_locator = (By.XPATH, f"//div[contains(@class, 'dropdown-item') and .=' {indicator_value} ']")
        self.find_and_click(input_locator)
        self.find_and_click(value_locator)
        time.sleep(2)
        self.wait_until_text_in_element(actual_input_value, indicator_value)

    def set_additional_indicators(self, indicators: list):
        plus_button_locator = self.add_entity_button_locator_creator("Дополнительные показатели")
        indicator_input_locator = (By.XPATH, "//div[@class='list-header' and .//div[contains(@class, 'title') and .='Дополнительные показатели']]//input")
        for indicator in indicators:
            self.find_and_click(plus_button_locator)
            self.find_and_click(indicator_input_locator)
            indicator_locator = self.dropdown_value_locator_creator(indicator)
            self.find_and_click(indicator_locator)
            time.sleep(1)
        actual_indicators_locator = self.list_elements_creator('Дополнительные показатели')
        actual_indicators = [i.text for i in self.elements_generator(actual_indicators_locator)]
        assert self.compare_lists(actual_indicators, indicators)

    def build_gantt(self):
        active_build_button_locator = (By.XPATH, "//gant//button[.=' Построить диаграмму ' and not(contains(@class, 'disabled'))]")
        self.find_and_click(active_build_button_locator)
        self.wait_stable_page()


class DiagramPage(EntityPage):

    LOCATOR_DIAGRAM = (By.XPATH, "//pkm-chart-diagram")

    def __init__(self, driver):
        super().__init__(driver)
        self.tree = NewTree(driver)
        self.modal = Modals(driver)

    def create_diagram(self, parent_name, diagram_name, from_model=True):
        with allure.step(f'Создать диаграмму {diagram_name}'):
            self.find_and_context_click(self.tree.node_locator_creator(parent_name), time=20)
            if from_model:
                self.hover_over_element(self.tree.context_option_locator_creator('Создать'))
                self.find_and_click(self.tree.submenu_option_locator_creator('Диаграмма'))
            else:
                self.find_and_click(self.tree.context_option_locator_creator('Создать диаграмму'))
        with allure.step(f'Укзать название диаграммы {diagram_name} и создать ее'):
            self.modal.enter_and_save(diagram_name)
        with allure.step(f'Проверить отображение диаграммы {diagram_name} в дереве выбранной'):
            self.tree.wait_selected_node_name(diagram_name)
        with allure.step(f'Проверить переход на страницу диаграммы'):
            self.find_element(self.LOCATOR_DIAGRAM)

    def build_diagram(self, model_name, diagram_name, build_action=None, from_model=True):
        with allure.step("Создать диаграмму"):
            self.create_diagram(model_name, diagram_name, from_model=from_model)
        if build_action:
            with allure.step("Построить диаграмму"):
                build_action[0](build_action[1])

    def build_workshop_dictionaries_diagram(self, entities_data: dict):
        """
        entities_data = {
            0: {
                "related_entity_type": "Таблица данных",
                "related_entity_model": "Модель",
                "related_table_name": "МТР"
            },
            1: {"related_entity_type": "Таблица данных",
                "related_entity_model": "Модель",
                "related_table_name": "Персонал"}
        }
        """
        set_figure_locator = (By.XPATH, "//a//*[local-name()='rect' and @ry]")
        diagram_figure_locator = (By.XPATH, "//div[contains(@class, 'geDiagramContainer')]//*[local-name()='g']//*[local-name()='rect' and @ry]")
        prev_diagram_html = self.get_element_html(self.LOCATOR_DIAGRAM)
        with allure.step("Добавить фигуру 1"):
            self.find_and_click(set_figure_locator)
            self.wait_stable_page(3)
            # self.wait_element_changing(prev_diagram_html, self.LOCATOR_DIAGRAM, time=5, ignore_timeout=True)
            # prev_diagram_html = self.get_element_html(self.LOCATOR_DIAGRAM)
            self.drag_and_drop_by_offset(diagram_figure_locator, -300, 0)
            self.wait_stable_page(3)
            # self.wait_element_changing(prev_diagram_html, self.LOCATOR_DIAGRAM, time=5, ignore_timeout=True)
        with allure.step("Добавить фигуру 2"):
            self.find_and_click(set_figure_locator)
        with allure.step("Настроить фигуру 1"):
            self.set_table_entity(entities_data[0])
        with allure.step("Настроить фигуру 2"):
            self.set_table_entity(entities_data[1])

    def build_workshop_menu_diagram(self, events_plan_dashboard: str, diagrams_dashboard: str):
        set_figure_locator = (By.XPATH, "//a//*[local-name()='rect' and @ry]")
        diagram_figure_locator = (By.XPATH,
                                  "//div[contains(@class, 'geDiagramContainer')]//*[local-name()='g']//*[local-name()='rect' and @ry]")
        prev_diagram_html = self.get_element_html(self.LOCATOR_DIAGRAM)
        with allure.step("Добавить фигуру 1"):
            self.find_and_click(set_figure_locator)
            self.wait_element_changing(prev_diagram_html, self.LOCATOR_DIAGRAM, time=3, ignore_timeout=True)
            prev_diagram_html = self.get_element_html(self.LOCATOR_DIAGRAM)
            self.drag_and_drop_by_offset(diagram_figure_locator, -300, 0)
            self.wait_element_changing(prev_diagram_html, self.LOCATOR_DIAGRAM, time=3, ignore_timeout=True)
        with allure.step("Добавить фигуру 2"):
            self.find_and_click(set_figure_locator)

        with allure.step('Настроить фигуру 1'):
            entity_1_data = {
                        "related_dashboard_name": events_plan_dashboard,
                        "entity_order": 1
                    }
            self.set_dashboard_entity(entity_1_data)

        with allure.step('Настроить фигуру 2'):
            entity_2_data = {
                "related_dashboard_name": diagrams_dashboard,
                "entity_order": 2
            }
            self.set_dashboard_entity(entity_2_data)

    def expand_setting_dropdown(self, dropdown_name):
        settings_dropdown_locator = (By.XPATH, f"//div[contains(@class, 'format-title') and .=' {dropdown_name} ']")
        if 'caret-up' not in self.get_element_html(settings_dropdown_locator):
            self.find_and_click(settings_dropdown_locator)

    def set_dashboard_entity(self, entity_data):
        """
                entity_data = {
                        "related_dashboard_name": "МТР"
                        "entity_order": 1
                    }
        """
        entity_name = entity_data.get('related_dashboard_name')
        entity_order = entity_data.get('entity_order')

        assert entity_name
        assert entity_order

        entity_locator = (By.XPATH, f"(//div[contains(@class, 'geDiagramContainer')]//*[local-name()='g']//*[local-name()='rect' and @ry])[{entity_order}]")
        entity_type_dropdown_locator = (By.XPATH, "//div[contains(@class, 'ks-dropdown-placeholder') and .= ' Тип сущности ']")
        entity_type_dropdown_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' Интерфейс ']")
        dashboard_input_locator = (By.XPATH, "//div[contains(@class, 'form-col') and .//div[.='Поиск по сущности']]//input")
        sync_name_checkbox_locator = (By.XPATH, "//div[contains(@class, 'checkbox-label') and .='Синхронизировать название']")
        add_interaction_button_locator = (By.XPATH, "//div[.='Взаимодействия' and contains(@class, 'interact-title-container')]//fa-icon[@icon='plus']")
        interaction_dropdown_locator = (By.XPATH, "//ks-dropdown[.//div[.=' Выберите взаимодействие ']]")
        interaction_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' Клик ']")
        add_action_button_locator = (By.XPATH, "//div[.='Действия' and contains(@class, 'add-interaction-item')]//fa-icon[@icon='plus']")
        action_dropdown_locator = (By.XPATH, "//ks-dropdown[.//div[.=' Выберите действие ']]")
        action_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' Передать сущность ']")
        save_interaction_button_locator = (By.XPATH, "//div[contains(@class, 'SidebarContainer')]//button[.=' Сохранить']")

        with allure.step('Привязать сущность к фигуре'):
            self.find_and_click(entity_locator)
            self.expand_setting_dropdown('Связь с сущностью')
            self.find_and_click(entity_type_dropdown_locator)
            self.find_and_click(entity_type_dropdown_option_locator)
            self.find_and_enter(dashboard_input_locator, entity_name)
            self.find_and_click(self.dropdown_value_locator_creator(entity_name))
            self.find_and_click(sync_name_checkbox_locator)

        with allure.step('Задать передачу сущности при клике'):
            self.expand_setting_dropdown('Взаимодействие')
            self.find_and_click(add_interaction_button_locator)
            self.find_and_click(interaction_dropdown_locator)
            self.find_and_click(interaction_option_locator)
            self.find_and_click(add_action_button_locator)
            self.find_and_click(action_dropdown_locator)
            self.find_and_click(action_option_locator)
            self.find_and_click(save_interaction_button_locator)

            time.sleep(3)

    def set_table_entity(self, entity_data):
        """
        entity_data = {
                "related_entity_model": "Модель",
                "related_table_name": "МТР"
                "entity_order": 1
            }
        """
        entity_model = entity_data.get('related_entity_model')
        entity_name = entity_data.get('related_table_name')
        entity_order = entity_data.get('entity_order')
        assert entity_model
        assert entity_name
        assert entity_order
        entity_locator = (By.XPATH, f"(//div[contains(@class, 'geDiagramContainer')]//*[local-name()='g']//*[local-name()='rect' and @ry])[{entity_order}]")
        entity_type_dropdown_locator = (By.XPATH, "//div[contains(@class, 'ks-dropdown-placeholder') and .= ' Тип сущности ']")
        entity_type_dropdown_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' Таблица данных ']")
        model_input_locator = (By.XPATH, "//div[contains(@class, 'form-col') and .//div[.='Поиск модели']]//input")
        table_dropdown_locator = (By.XPATH, "//div[contains(@class, 'form-col') and .//div[.=' Поиск по сущности ']]//ks-dropdown")
        entity_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' {entity_name} ']")
        sync_name_checkbox_locator = (By.XPATH, "//div[contains(@class, 'checkbox-label') and .='Синхронизировать название']")
        add_interaction_button_locator = (By.XPATH, "//div[.='Взаимодействия' and contains(@class, 'interact-title-container')]//fa-icon[@icon='plus']")
        add_action_button_locator = (By.XPATH, "//div[.='Действия' and contains(@class, 'add-interaction-item')]//fa-icon[@icon='plus']")
        interaction_dropdown_locator = (By.XPATH, "//ks-dropdown[.//div[.=' Выберите взаимодействие ']]")
        action_dropdown_locator = (By.XPATH, "//ks-dropdown[.//div[.=' Выберите действие ']]")
        interaction_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' Клик ']")
        action_option_locator = (By.XPATH, f"//div[contains(@class, 'single-dropdown-item') and .= ' Передать сущность ']")
        save_interaction_button_locator = (By.XPATH, "//div[contains(@class, 'SidebarContainer')]//button[.=' Сохранить']")

        with allure.step('Привязать сущность к фигуре'):
            self.find_and_click(entity_locator)
            self.expand_setting_dropdown('Связь с сущностью')
            self.find_and_click(entity_type_dropdown_locator)
            self.find_and_click(entity_type_dropdown_option_locator)
            self.find_and_enter(model_input_locator, entity_model)
            self.find_and_click(self.dropdown_value_locator_creator(entity_model))
            self.find_and_click(table_dropdown_locator)
            self.find_and_click(entity_option_locator)
            self.find_and_click(sync_name_checkbox_locator)
        with allure.step('Задать передачу сущности при клике'):
            self.expand_setting_dropdown('Взаимодействие')
            self.find_and_click(add_interaction_button_locator)
            self.find_and_click(interaction_dropdown_locator)
            self.find_and_click(interaction_option_locator)
            self.find_and_click(add_action_button_locator)
            self.find_and_click(action_dropdown_locator)
            self.find_and_click(action_option_locator)
            self.find_and_click(save_interaction_button_locator)

        time.sleep(3)
