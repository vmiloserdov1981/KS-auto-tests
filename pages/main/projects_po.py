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
    LOCATOR_PROJECT_AUTOTEST = (By.XPATH, "//div[contains(@class, 'project__info-name') and .=' AUTOTEST BASIC ']")
    LOCATOR_PROJECT_CONSTRUCTOR_TAB = (By.XPATH, "//div[contains(@class, 'publication-view__name__text') and .='Конструктор']")

    LOCATOR_CLASSES_TAB = (By.XPATH, "//div[contains(@class, 'admin-sidebar__item') and .//div[.=' Классы ']]")
    LOCATOR_MODELS_TAB = (By.XPATH, "//div[contains(@class, 'admin-sidebar__item') and .//div[.=' Модели ']]")

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

    SAVE_BUTTON_MODAL_WINDOW = (By.XPATH, "//pkm-modal-window//*[text()=' Сохранить ' or text()='Сохранить']")
    LOCATOR_BLANK_AREA = (By.XPATH, "//pkm-modal-window//*[text()='Настройка объекта']")
    LOCATOR_TABLE_TAB = (By.XPATH, "//pkm-app-root//*[text()=' Таблица ']")


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
        time.sleep(3)



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
