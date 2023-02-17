from pages.main.new_po import NewPage
from selenium.webdriver.common.by import By
from core import retry
import requests
import json
import time

class ProjectsPage(NewPage):
    LOCATOR_PROJECTS_PAGE = (By.XPATH, "//ks-projects")
    LOCATOR_PROJECT_NAME_INPUT = (By.XPATH, "//div[contains(@class,'project-details__row') and ./div[.='Название проекта']]//input")
    LOCATOR_PROJECT_SEARCH_INPUT = (By.XPATH, "//div[contains(@class,'projects-header')]//input")
    PROJECT_SEARCH_FIELD = (By.XPATH, "//ks-filter-input/div/input")
    LOCATOR_PROJECT_AUTOTEST = (By.XPATH, "//div[contains(@class, 'project-card__info-name') and .='AUTOTEST BASIC']")
    LOCATOR_PROJECT_CONSTRUCTOR_TAB = (By.XPATH, "//div[contains(@class, 'publication-view__name__text') and .='Конструктор']")

    LOCATOR_CLASSES_TAB = (By.XPATH, "//div[contains(@class, 'admin-sidebar__item') and .//div[.=' Классы ']]")
    LOCATOR_MODELS_TAB = (By.XPATH, "//div[contains(@class, 'admin-sidebar__item') and .//div[.=' Модели ']]")
    LOCATOR_INTERFACES_TAB = (By.XPATH, "//div[contains(@class, 'admin-sidebar__item') and .//div[.=' Интерфейсы ']]")

    LOCATOR_ADD_CLASSES_TAB = (By.XPATH, "//pkm-app-root//ks-button/button")
    LOCATOR_EXPAND_TABLE = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[1]/div/pkm-ks-tree/div[3]/virtual-scroller/div[2]/pkm-tree-item/div/div[1]")
    LOCATOR_CREATE_CLASS = (By.XPATH, "//div[contains(@class, '') and .=' Создать класс ']")
    LOCATOR_TABLE1_TAB = (By.XPATH, "//pkm-app-root//*[text()='Сводная по команде 1']")
    LOCATOR_TABLE2_TAB = (By.XPATH, "//pkm-app-root//*[text()='Сводная по команде 2']")
    LOCATOR_ADD_STRING = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-table-page/div/div[2]/pkm-admin-table-constructor/ks-table-constructor/div[1]/div[1]/div[3]/ks-add-field-button/ks-button/button/div")
    LOCATOR_ADD_STRING_ATTACH = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-table-page/div/div[2]/pkm-admin-table-constructor/ks-table-constructor/div[1]/div[2]/pkm-structure-list/div/div/div[5]/ks-add-field-button/ks-button/button/div")
    LOCATOR_ADD_COLUMN = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-table-page/div/div[2]/pkm-admin-table-constructor/ks-table-constructor/div[2]/div[1]/div[3]/ks-add-field-button/ks-button/button/div")
    LOCATOR_OBJECT_SETUP = (By.XPATH, "//div[contains(@class, 'overlay-item') and .='Настройка объекта']")
    LOCATOR_INDICATORS = (By.XPATH, "//div[contains(@class, 'overlay-item') and .='Показатели']")
    LOCATOR_DATA_SET = (By.XPATH, "//div[contains(@class, 'overlay-item') and .='Наборы данных']")
    LOCATOR_INPUT_OBJECT = (By.XPATH, "//pkm-modal-window//async-dropdown-pagination/div/input")

    LOCATOR_CHECKBOX_OBJECT1 = (By.XPATH, "//div[contains(@class, '') and .='Иванов']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_OBJECT2 = (By.XPATH, "//div[contains(@class, '') and .='Петров']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_OBJECT3 = (By.XPATH, "//div[contains(@class, '') and .='Сидоров']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_OBJECT4 = (By.XPATH, "//div[contains(@class, '') and .='Abramson']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_OBJECT5 = (By.XPATH, "//div[contains(@class, '') and .='Bishop']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_OBJECT6 = (By.XPATH, "//div[contains(@class, '') and .='Cloud']//div[contains(@class, 'checkbox-container')]")

    SAVE_BUTTON_MODAL_WINDOW = (By.XPATH, "//pkm-modal-window//*[text()=' Сохранить ' or text()='Сохранить' or text()=' Сохранить']")
    SAVE_BUTTON_MODAL_CONTAINER = (By.XPATH, "//pkm-modal-container//*[text()=' Сохранить ' or text()='Сохранить' or text()=' Сохранить']")

    LOCATOR_BLANK_AREA = (By.XPATH, "//pkm-modal-window//*[text()='Настройка объекта']")
    LOCATOR_TABLE_TAB = (By.XPATH, "//pkm-app-root//*[text()=' Таблица ']")

    LOCATOR_ADD_INTERFACE = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[1]/div/pkm-ks-tree/div[1]/div[2]/ks-button/button/div")
    LOCATOR_CREATE_INTERFACE = (By.XPATH, "//*[text()=' Создать интерфейс ']")
    INPUT_INTERFACE_NAME = (By.XPATH, "//pkm-modal-window//textarea[contains(@placeholder, 'Введите название')]")
    CREATE_BUTTON = (By.XPATH, "//div[contains(@class, 'ks-button') and .='Создать']")
    SPLIT_ICON_BUTTON = (By.CSS_SELECTOR, "body > pkm-app-root > div > pkm-admin > div.admin-main > div > div > div.router-outlet > ks-admin-dashboard > div > ks-dashboard > div > div > ks-dashboard-cells-grid > div > div > ks-dashboard-cell > div > div > div.edit-cell-content-buttons > fa-icon > svg > path")
    SPLIT_ICON_BUTTON_HORIZON2 = (By.CSS_SELECTOR, "body > div > div > div:nth-child(2) > fa-icon > svg")
    RELATED_ENTITY_ICON = (By.CSS_SELECTOR, "body > pkm-app-root > div > pkm-admin > div.admin-main > div > div > div.router-outlet > ks-admin-dashboard > div > div > ks-dashboard-toolbar > div > div:nth-child(1) > div:nth-child(2) > ks-button > button > div")
    RELATED_ENTITY_DROPDOWN = (By.XPATH, "//ks-dashboard-toolbar-linked-entity/div/div[2]/div/ks-dropdown/div/div[2]")
    LOCATOR_CHOICE_TABLE_DROPDOWN = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='Таблица']")
    LOCATOR_CHOICE_BUTTON_DROPDOWN = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='Кнопки']")
    LOCATOR_EDIT_RELATED_ENTITY = (By.CSS_SELECTOR, "#cdk-overlay-0 > ks-dashboard-toolbar-linked-entity > div > div.dashboard-linked-entity__body > div > div.dashboard-linked-entity__edit > fa-icon > svg")
    TAB_INPUT_MODEL_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Модель')]")
    LOCATOR_TAB_NAME_COMMANDS = (By.XPATH, "//div[contains(@class, 'dropdown-item-default') and .=' Команды ']")

    TAB_INPUT_TABLE_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Таблица')]")
    LOCATOR_TAB_NAME_SUMMARY = (By.XPATH, "//div[contains(@class, 'dropdown-item-default') and .=' Сводная по команде 1 ']")
    LOCATOR_CLICK_ONE_CELL = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-admin-dashboard/div/ks-dashboard/div/div/ks-dashboard-cells-grid/div/div/ks-dashboard-cell[1]/div/div/div[1]")
    LOCATOR_CLICK_TWO_CELL = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-admin-dashboard/div/ks-dashboard/div/div/ks-dashboard-cells-grid/div/div/ks-dashboard-cell[2]/div/div/div[2]")
    LOCATOR_CLICK_TWO_CELL2 = (By.XPATH, "//div[contains(@class, 'item-name') and .='Передача по событию']")

    LOCATOR_CELL_EVENTS = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-admin-dashboard/div/div/ks-dashboard-toolbar/div/div[1]/div[3]/ks-button/button/div")
    LOCATOR_ADD_CELL_EVENTS = (By.XPATH, "//div[contains(@class, 'ks-button__container') and .='Добавить ' or .='Добавить']")

    LOCATOR_EVENT_TYPE_DROPDOWN = (By.XPATH, "/html/body/div/div[4]/div/pkm-modal-container/div/div/div[3]/pkm-dashboard-cell-event/div/ks-dashboard-cell-event-settings/div[1]/div/ks-dropdown/div/div[2]")
    LOCATOR_ACTION_DROPDOWN = (By.XPATH, "/html/body/div/div[4]/div/pkm-modal-container/div/div/div[3]/pkm-dashboard-cell-event/div/ks-dashboard-cell-event-settings/div[2]/div/ks-dropdown/div/div[2]")
    LOCATOR_SOURCE_DROPDOWN = (By.XPATH, "/html/body/div/div[4]/div/pkm-modal-container/div/div/div[3]/pkm-dashboard-cell-event/div/ks-dashboard-cell-event-settings/div[3]/div/ks-dropdown/div/div[2]")

    LOCATOR_EVENT_TYPE_CHOICE_TAB = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='Получение таблицы']")
    LOCATOR_ACTION_CHOICE_PUT = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='Поместить']")
    LOCATOR_CHOICE_ONE_CELL = (By.XPATH, "/html/body/div/div/div/div/div/cdk-virtual-scroll-viewport/div[1]/ks-default-item[1]/div/ks-multiple-item/div/div")
    LOCATOR_CHOICE_TWO_CELL = (By.XPATH, "/html/body/div/div/div/div/div/cdk-virtual-scroll-viewport/div[1]/ks-default-item[2]/div/ks-multiple-item/div")

    LOCATOR_EVENT_TAG_INPUT = (By.XPATH, "//div//input[contains(@class, 'ng-pristine ng-valid input')]")


    LOCATOR_CLICK_EMPTY = (By.XPATH, "//span[contains(@class, '') and .='Настройка входящего события']")
    TAB_INPUT_BUTTON_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@formcontrolname, 'name')]")
    LOCATOR_ACTION_TAB = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Действия ']")
    LOCATOR_PLUS_ICON = (By.XPATH, "/html/body/pkm-modal-window-outlet/pkm-dashboard-button-settings/pkm-modal-window/div/div/div[3]/ks-tabs-group/div[2]/ks-actions-list/div/div[1]/div[1]/ks-button/button/div")
    LOCATOR_ACTION_TYPE = (By.XPATH, "//div[contains(@class, 'ks-dropdown-text-field__content') and .='Добавить объект']")
    LOCATOR_SEARCH_TYPE_ACTION_SEARCH = (By.XPATH, "//div//ks-dropdown-search//input[contains(@placeholder, 'Поиск')]")
    LOCATOR_ACTION_TYPE_TRANSFER_ENTITY = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__content') and .='Передать сущность']")
    LOCATOR_ENTITY_TYPE = (By.XPATH, "//div[contains(@class, 'ks-dropdown-text-field__content') and .='Класс']")
    LOCATOR_ENTITY_TYPE_TABLE = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='Таблица данных']")
    LOCATOR_ENTITY_INPUT = (By.XPATH, "//div//input[contains(@class, 'async')]")
    LOCATOR_SUMMARY_ON_COMMAND_TWO = (By.XPATH, "//div[contains(@class, 'dropdown-item-default') and .=' Сводная по команде 2 ']")
    SAVE2_BUTTON_MODAL_WINDOW = (By.XPATH, "/html/body/pkm-modal-window-outlet/pkm-dashboard-button-settings/pkm-modal-window/div/div/div[4]/ks-button[2]/button/div")

    LOCATOR_OUTGOING_EVENTS = (By.XPATH, "//div[contains(@class, 'ks-button') and .='Исходящее событие']")
    LOCATAR_ADD_NEW_TAG = (By.XPATH, "//span[contains(@class, 'ks-tag__') and .=' Новый тег ']")
    LOCATAR_ADD_NEW_TAG_INPUT = (By.XPATH, "//input[contains(@class, 'ks-tag__create-input')]")
    LOCATAR_PLAY_INTERFACE = (By.XPATH, "/html/body/pkm-app-root/div/pkm-admin/div[2]/div/div/div[2]/ks-admin-dashboard/div/div/ks-dashboard-toolbar/div/div[2]/ks-button[3]/button/div")
    LOCATOR_TRANSFER_ENTITY_BUTTON = (By.XPATH, "//div[contains(@class, 'buttons-row') and .=' Передать сущность ']")
    CONFIRM_BUTTON = (By.XPATH, "//pkm-modal-window//*[text()=' Принять ' or text()='Принять']")


    @retry
    def switch_to_publication(self, project_name, publication_name):
        self.select_project(project_name)
        self.select_publication(publication_name)

    def click_to_page_project(self):
        self.sidebar.select_page('Проекты')
        time.sleep(1)

    def search_test_project(self, Project_name):
        self.find_element(self.PROJECT_SEARCH_FIELD).send_keys(Project_name)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_PROJECT_AUTOTEST)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_PROJECT_CONSTRUCTOR_TAB)
        time.sleep(1)

    def create_first_table(self):
#        self.find_and_click(self.LOCATOR_MODELS_TAB)
        time.sleep(3)
        payload = {"login": "admin", "password": "Password2"}
        resp = requests.post('https://dev.ks.works/api/auth/login', data=json.dumps(payload))
        result = json.loads(resp.text)
        result2 = result.get('token')
        token = {"Authorization": f"Bearer {result2}"}
        print(token)

        payload = {
            "name": "Сводная по команде 4",
            "modelUuid": "01ed82a6-521b-020b-969e-00b15c0c4000",
            "type": "table",
            "parentUuid": "01ed82a6-521b-7bd1-969e-00b15c0c4000",
            "dataTableType": "table",
            "diagramType": 1
        }
        response = requests.post('https://dev.ks.works/api/models/create-model-node', headers=token, json=payload)
        print(response.text)


    def made_first_table(self):
        self.find_and_click(self.LOCATOR_EXPAND_TABLE)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_TABLE1_TAB)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ADD_STRING)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_OBJECT_SETUP)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_INPUT_OBJECT)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHECKBOX_OBJECT1)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHECKBOX_OBJECT2)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHECKBOX_OBJECT3)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BLANK_AREA)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(1)

        self.find_and_click(self.LOCATOR_ADD_STRING_ATTACH)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_INDICATORS)
        time.sleep(1)

        self.find_and_click(self.LOCATOR_ADD_COLUMN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_DATA_SET)
        time.sleep(1)

        self.find_and_click(self.LOCATOR_TABLE_TAB)
        time.sleep(1)

    def made_two_table(self):
        self.find_and_click(self.LOCATOR_TABLE2_TAB)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ADD_STRING)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_OBJECT_SETUP)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_INPUT_OBJECT)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHECKBOX_OBJECT4)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHECKBOX_OBJECT5)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHECKBOX_OBJECT6)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BLANK_AREA)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(1)

        self.find_and_click(self.LOCATOR_ADD_STRING_ATTACH)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_INDICATORS)
        time.sleep(1)

        self.find_and_click(self.LOCATOR_ADD_COLUMN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_DATA_SET)
        time.sleep(1)

        self.find_and_click(self.LOCATOR_TABLE_TAB)
        time.sleep(1)

    def create_interface(self, Interface_name):
        self.find_and_click(self.LOCATOR_INTERFACES_TAB)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_INTERFACE)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CREATE_INTERFACE)
        time.sleep(0.5)
        self.find_element(self.INPUT_INTERFACE_NAME).send_keys(Interface_name)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(0.5)
        self.find_and_click(self.CREATE_BUTTON)
        time.sleep(0.5)
        self.find_and_click(self.SPLIT_ICON_BUTTON)
        time.sleep(0.5)
        self.find_and_click(self.SPLIT_ICON_BUTTON_HORIZON2)
        time.sleep(0.5)

    def create_related_entity_table(self, Model_name, Table_name1):
        self.find_and_click(self.LOCATOR_CLICK_ONE_CELL)
        time.sleep(0.5)
        self.find_and_click(self.RELATED_ENTITY_ICON)
        time.sleep(0.5)
        self.find_and_click(self.RELATED_ENTITY_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHOICE_TABLE_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_EDIT_RELATED_ENTITY)
        time.sleep(0.5)

        self.find_element(self.TAB_INPUT_MODEL_NAME).send_keys(Model_name)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_TAB_NAME_COMMANDS)
        time.sleep(0.5)
        self.find_element(self.TAB_INPUT_TABLE_NAME).send_keys(Table_name1)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_TAB_NAME_SUMMARY)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(0.5)

    def set_events_for_table(self, Event_tag):
#        self.find_and_click(self.LOCATOR_CLICK_ONE_CELL)
#        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CELL_EVENTS)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ADD_CELL_EVENTS)
        time.sleep(0.5)

        self.find_and_click(self.LOCATOR_EVENT_TYPE_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_EVENT_TYPE_CHOICE_TAB)
        time.sleep(0.5)

        self.find_and_click(self.LOCATOR_ACTION_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ACTION_CHOICE_PUT)
        time.sleep(0.5)

        self.find_and_click(self.LOCATOR_SOURCE_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHOICE_ONE_CELL)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHOICE_TWO_CELL)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CLICK_EMPTY)

        self.find_element(self.LOCATOR_EVENT_TAG_INPUT).send_keys(Event_tag)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_CONTAINER)
        time.sleep(1)

    def create_related_entity_button(self, Button_name, Entity_name):
#        self.hover_over_element(self.LOCATOR_CLICK_TWO_CELL)
#        time.sleep(1)
        self.find_and_click(self.LOCATOR_CLICK_TWO_CELL2)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CLICK_TWO_CELL2)
        time.sleep(0.5)
        self.find_and_click(self.RELATED_ENTITY_ICON)
        time.sleep(0.5)
        self.find_and_click(self.RELATED_ENTITY_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CHOICE_BUTTON_DROPDOWN)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_EDIT_RELATED_ENTITY)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ADD_CELL_EVENTS)
        time.sleep(0.5)
        self.find_element(self.TAB_INPUT_BUTTON_NAME).send_keys(Button_name)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ACTION_TAB)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_PLUS_ICON)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ACTION_TYPE)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_SEARCH_TYPE_ACTION_SEARCH).send_keys(Button_name)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ACTION_TYPE_TRANSFER_ENTITY)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ENTITY_TYPE)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_ENTITY_TYPE_TABLE)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_ENTITY_INPUT).send_keys(Entity_name)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_SUMMARY_ON_COMMAND_TWO)
        time.sleep(1)
        self.find_and_click(self.SAVE2_BUTTON_MODAL_WINDOW)
        time.sleep(2)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(2)


    def set_events_for_button(self, Event_tag):
        self.find_and_click(self.LOCATOR_CLICK_TWO_CELL)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CELL_EVENTS)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_OUTGOING_EVENTS)
        time.sleep(0.5)
        self.find_and_click(self.LOCATAR_ADD_NEW_TAG)
        time.sleep(0.5)
        self.find_element(self.LOCATAR_ADD_NEW_TAG_INPUT).send_keys(Event_tag)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_OUTGOING_EVENTS)
        time.sleep(0.5)
        self.find_and_click(self.LOCATAR_PLAY_INTERFACE)
        time.sleep(2)
        self.find_and_click(self.LOCATOR_TRANSFER_ENTITY_BUTTON)
        time.sleep(1)
        self.find_and_click(self.CONFIRM_BUTTON)
        time.sleep(4)


    def create_class_and_metrics(self, Class_name, Index1, Index2, Index3):
        self.find_and_click(self.LOCATOR_CLASSES_TAB)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_CLASSES_TAB)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CREATE_CLASS)
        time.sleep(3)


    def switch_to_page(self):
        self.sidebar.select_page('Проекты')
        self.wait_element_stable(self.LOCATOR_PROJECTS_PAGE, 3)

    def search_project(self, project_name):
        self.find_and_enter(self.LOCATOR_PROJECT_SEARCH_INPUT, project_name)
        time.sleep(1)

    def select_project(self, project_name):
        self.search_project(project_name)
        project_locator = (By.XPATH, f"//div[@routerlink='project-details' and .//div[@class='project__info-name' and .=' {project_name} ']]")
        self.find_and_click(project_locator)
        selected_project_title_locator = (By.XPATH, "//div[contains(@class,'project-details')]//div[contains(@class, 'project-title')]")
        self.wait_until_text_in_element(selected_project_title_locator, project_name)

    def select_publication(self, publication_name):
#        pub_locator = (By.XPATH, f"//div[contains(@class, 'publication-view__name-container') and .//span[.='{publication_name}']]")
        pub_locator = (By.XPATH, f"//div[contains(@class, 'publication-view__name__text') and .='{publication_name}']")
        self.find_and_click(pub_locator)
