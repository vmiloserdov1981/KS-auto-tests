import json
import time
from api.api_projects import ApiProjects
import requests
from pages.main.new_po import NewPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



from selenium import webdriver
from selenium.webdriver import ActionChains


class UsersPage(NewPage):
    LOCATOR_USERS_PAGE = (By.XPATH, "//ks-users")
    LOCATOR_BACKUP_PAGE = (By.XPATH, "//ks-backup")
    LOCATOR_PROJECT_PAGE = (By.XPATH, "//ks-project")
    LOCATOR_PAGINATION_NEXT_PAGE_BUTTON = (By.XPATH, "(//ks-pagination//li[.//*[local-name()='svg' and contains(@data-icon, 'chevron-right')]])[not (contains(@class, 'disabled'))]")
    LOCATOR_ADD_USER = (By.XPATH, "//pkm-app-root//*[text()='Пользователь']")
    FIRST_NAME_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите имя')]")
    LAST_NAME_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите фамилию')]")
    MIDLE_NAME_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите отчество')]")
    LOGIN_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите логин')]")
    EMAIL_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите e-mail')]")
    PASSWORD_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Создайте пароль')]")
    PASSWORD_CONFIRM_FIELD = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Подтвердить пароль')]")
    SAVE_BUTTON = (By.XPATH, "//ks-button//*[text()=' Сохранить ' or text()='Сохранить']")
    DEL_USER_BUTTON = (By.XPATH, "//ks-button//*[text()='Удалить пользователя']")
    CONFIRM_BUTTON = (By.XPATH, "//pkm-modal-window//*[text()=' Принять ' or text()='Принять']")
    target_locator = (By.XPATH, "//tr[(.//td[2])[.='eu_user5']]")
    RESTORE_BACKUP_BTN = (By.XPATH, "//div[contains(@class, 'ks-button__container') and .=' Восстановить из копии ' or  .='Восстановить из копии']")
    LOCATOR_BACKUP_MODAL_PAGE = (By.XPATH, "//div[contains(@class, 'modal-window-title') and .='Восстановление из копии']")
    LOCATOR_PROJECT_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Введите название проекта')]")
    LOCATOR_FILE_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Выберите файл')]")
    LOCATOR_PASSWORD_FIELD = (By.XPATH, "//pkm-modal-window//input[contains(@type, 'password')]")
    LOCATOR_NEXT_BTN = (By.XPATH, "//div[contains(@class, 'ks-button__container') and .='Далее']")
    LOCATOR_CREATE_COPY_BTN = (By.XPATH, "//div[contains(@class, 'ks-button__container') and .='Создать копию']")
    LOCATOR_SUCCESSFUL_BACKUP = (By.XPATH, "//pkm-modal-window//*[text()=' Данные из копии ' or text()='Данные из копии']")
    LOCATOR_CONTINUE_BTN = (By.XPATH, "//pkm-modal-window//*[text()=' Продолжить ' or text()='Продолжить' or text()='Далее']")
    project_locator = (By.XPATH, "//div[contains(@class, 'project__info-name') and .=' Autotest_project ' or .='Autotest_project']")
    project_locator2 = (By.XPATH, "//div[contains(@class, 'project__info-name') and .=' Test_project_PyCharm ' or .='Test_project_PyCharm']")
    locator_successfully_backup = (By.XPATH, "//pkm-modal-window//*[text()=' успешно создана ' or text()='успешно создана']")
    DEL_PROJECT_BUTTON = (By.XPATH, "//ks-button//*[text()='Удалить проект']")
    PROJECT_SEARCH_FIELD = (By.XPATH, "//ks-filter-input/div/input")
    CREATE_BACKUP_BTN = (By.XPATH, "//div[contains(@class, 'ks-button__container') and .=' Создать копию ' or  .='Создать копию']")
    LOCATOR_CREATE_BACKUP_MODAL_PAGE = (By.XPATH, "//div[contains(@class, 'modal-window-title') and .='Создать резервную копию']")
    LOCATOR_DROPDOWN_CHOICE_PROJECT = (By.XPATH, "//pkm-modal-window//*[text()=' Выберите проект ']")
    INPUT_PROJECT_NAME = (By.XPATH, "//div[contains(@class, 'overlay')]//input")
    LOCATOR_ONLY_AUTOTEST_PROJECT = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='ONLY_AUTOTEST']")

    LOCATOR_BACKUP_TAB = (By.XPATH, "//div[contains(@class, 'sidebar__nav-item') and .//span[.='Резервное копирование']]")
    LOCATOR_BACKUP_CHECK = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Справочники ']")
    LOCATOR_BACKUP_CHECK_CLASSES = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Классы ']")
    LOCATOR_BACKUP_CHECK_MODELS = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Модели ']")
    LOCATOR_BACKUP_CHECK_DIAGRAM = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Диаграммы ']")
    LOCATOR_BACKUP_CHECK_TEMPLATES = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Шаблоны ']")
    LOCATOR_BACKUP_CHECK_RESTRICTIONS = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Ограничения ']")
    LOCATOR_BACKUP_CHECK_INTERFACE = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Интерфейсы ']")
    LOCATOR_BACKUP_CHECK_APPLICATION = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Приложения ']")
    LOCATOR_BACKUP_CHECK_INTEGRATION = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Интеграции ']")
    LOCATOR_BACKUP_CHECK_BPMS = (By.XPATH, "//div[contains(@class, 'tab-title') and .=' Бизнес-процессы ']")

    LOCATOR_CHECKBOX_REFERENCES = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Справочники']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_CLASSES = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Классы']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_MODELS = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Модели']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_DIAGRAM = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Диаграммы']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_TEMPLATES = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Шаблоны']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_RESTRICTIONS = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Ограничения']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_INTERFACE = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Интерфейсы']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_APPLICATION = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Приложения']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_INTEGRATION = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Интеграции']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_CHECKBOX_BPMS = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Бизнес-процессы']//div[contains(@class, 'checkbox-container')]")

    CREATE_NEW_PROJECT_BTN = (By.XPATH, "//ks-button//*[text()=' Проект ']")
    LOCATOR_INPUT_NAME_PROJECT = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Введите название проекта')]")
    LOCATOR_ADD_PROJECT_BTN = (By.XPATH, "//ks-button//*[text()=' Добавить проект ']")
    LOCATOR_ACCESS_BTN = (By.XPATH, "//pkm-app-root//*[text()=' Доступы ']")
    LOCATOR_ADD_USER_BTN = (By.XPATH, "//pkm-app-root//*[text()=' Пользователь / роль ']")
    LOCATOR_SEARCH_BY_USER = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Поиск по пользователям')]")
    LOCATOR_CHECKBOX_USER = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='Иванов Андрей']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_ADD_BTN = (By.XPATH, "//pkm-modal-window//*[text()=' Добавить ' or text()='Добавить']")
    LOCATOR_ROLE_BTN = (By.XPATH, "//pkm-modal-window//*[text()='Роли' or text()=' Роли ']")
    LOCATOR_SEARCH_BY_ROLE = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Поиск по ролям')]")
    LOCATOR_CHECKBOX_ROLE = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='администратор']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_ACCESS1 = (By.XPATH, "//div[contains(@class, 'not-selected')]/following::div[1]")
    LOCATOR_ACCESS2 = (By.XPATH, "//div[contains(@class, 'not-selected')]/following::div[5]")
    LOCATOR_ACCESS3 = (By.XPATH, "//div[contains(@class, 'not-selected')]/following::div[7]")
#    LOCATOR_FULL_ACCESS2 = (By.XPATH, "//pkm-app-root//*[text()='Полный доступ']/following::div[37]/span")
    LOCATOR_SOURCE_BTN = (By.XPATH, "//pkm-app-root//*[text()=' Источники ']")
    LOCATOR_ADD_SOURCE_BTN = (By.XPATH, "//ks-button//*[text()=' Источник ']")
    LOCATOR_CHECKBOX_SOURCE = (By.XPATH, "//pkm-modal-window//ks-checkbox[.='uuu']//div[contains(@class, 'checkbox-container')]")
    LOCATOR_DISPLAY_BTN = (By.XPATH, "//pkm-app-root//*[text()=' Отображение ']")
    LOCATOR_ADD_IMAGE = (By.XPATH, "//div[contains(@class, 'container__config')]")
    LOCATOR_CALENDAR_TAB = (By.XPATH, "//pkm-app-root//*[text()=' Календари ']")
    LOCATOR_ADD_CALENDAR_BTN = (By.XPATH, "//pkm-app-root//*[text()='Календарь']")
#    LOCATOR_INPUT_CALENDAR_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@class, 'ng-pristine ng-valid ng-touched')]")
    LOCATOR_INPUT_CALENDAR_NAME = (By.XPATH, "/html/body/pkm-modal-window-outlet/ks-add-calendar/pkm-modal-window/div/div/div[3]/div/div[1]/div/ks-input/div/input")
    LOCATOR_INPUT_WORKING_DAY = (By.XPATH, "/html/body/pkm-modal-window-outlet/ks-add-calendar/pkm-modal-window/div/div/div[3]/div/div[4]/div/ks-input/div/input")
    LOCATOR_INPUT_WEEKEND_DAY = (By.XPATH, "/html/body/pkm-modal-window-outlet/ks-add-calendar/pkm-modal-window/div/div/div[3]/div/div[5]/div/ks-input/div/input")
    LOCATOR_COPY_DATA_FROM_CALENDAR = (By.XPATH, "//div[contains(@class, 'ks-dropdown-text-field__placeholder')]")
    LOCATOR_CALENDAR_DEFAULT = (By.XPATH, "//div[contains(@class, 'single-dropdown-item__name') and .='Календарь по умолчанию']")
    LOCATOR_COUNTDOWN = (By.XPATH, "//pkm-modal-window//ks-datepicker/div/input")
    LOCATOR_CALENDAR_NUMBER = (By.XPATH, "//div[contains(@class, 'mat-calendar-body') and .=' 1 ']")
#    LOCATOR_CALENDAR_TEST = (By.XPATH, "/html/body/pkm-app-root/div/pkm-main/div/div/ks-settings/div/ks-tabs-group/div[2]/ks-calendar-settings/div/div[1]/div[2]/div[2]/div")
    LOCATOR_CALENDAR_TEST = (By.XPATH, "//pkm-app-root//*[text()='Test_calendar']")
    LOCATOR_CALENDAR_TEST_AFTER_EDIT = (By.XPATH, "//pkm-app-root//*[text()='Test_calendar_copy']")
    LOCATOR_CALENDAR_TEST_EDIT = (By.XPATH, "/html/body/pkm-app-root/div/pkm-main/div/div/ks-settings/div/ks-tabs-group/div[2]/ks-calendar-settings/div/div[1]/div[2]/div[6]/div/fa-icon[1]")
    LOCATOR_CALENDAR_TEST_DEL = (By.XPATH, "/html/body/pkm-app-root/div/pkm-main/div/div/ks-settings/div/ks-tabs-group/div[2]/ks-calendar-settings/div/div[1]/div[2]/div[6]/div/fa-icon[2]")
    LOCATOR_SET_CALENDAR_DAY = (By.XPATH, "//ks-button//*[text()='Настроить день' or text()=' Настроить день ']")
    LOCATOR_RADIOBUTTON_DAYOFF = (By.XPATH, "//pkm-modal-window//ks-radio-item[2]//label/div/div")
    LOCATOR_ADD_COMMENT_FOR_CALENDAR_DAY = (By.XPATH, "//pkm-modal-window//textarea[contains(@placeholder, 'Введите комментарий')]")
    CONFIRM_BUTTON_DEL_CALENDAR = (By.XPATH, "//pkm-modal-window//*[text()=' Удалить ' or text()='Удалить']")
    LOCATOR_FONT_TAB = (By.XPATH, "//pkm-app-root//*[text()=' Шрифты ']")
    LOCATOR_ADD_FONT = (By.XPATH, "//pkm-app-root//*[text()=' Добавить шрифт ']")
    LOCATOR_INPUT_FONT_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@formcontrolname, 'fontName')]")
    LOCATOR_INPUT_SYSTEM_FONT_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@formcontrolname, 'fontSystemName')]")
    LOCATOR_FILE_TYPE = (By.XPATH, "//pkm-modal-window//div[contains(@class, 'ks-dropdown-text-field__placeholder')]")
    LOCATOR_FILE_TYPE_SEARCH = (By.XPATH, "//div//input[contains(@placeholder, 'Поиск')]")
    LOCATOR_FILE_TYPE_OPENTYPE = (By.XPATH, "//*[text()='opentype']")
    LOCATOR_INPUT_ADD_FONT = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Выберите файл')]")
    SAVE_BUTTON_MODAL_WINDOW = (By.XPATH, "//pkm-modal-window//*[text()=' Сохранить ' or text()='Сохранить']")
    LOCATOR_FONT_TEST_DEL = (By.CSS_SELECTOR, "body > pkm-app-root > div > pkm-main > div > div > ks-settings > div > ks-tabs-group > div.tab-body > ks-global-fonts-settings > ks-fonts-list > div > div:nth-child(6) > div.fonts__cell.flex-1.flex.flex-justify-end.mr-r-20 > fa-icon > svg")
    LOCATOR_FONT_TEST_AFTER_EDIT = (By.XPATH, "//pkm-app-root//*[text()=' Тестовый шрифт ' or text()='Тестовый шрифт']")
    LOCATOR_ICON_TAB = (By.XPATH, "//pkm-app-root//*[text()=' Иконки ']")
    LOCATOR_ADD_ICON_SET = (By.XPATH, "//pkm-app-root//*[text()=' Набор иконок ']")
    LOCATOR_NEW_SET_ICON_NAME = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Введите название набора')]")
    LOCATOR_ADD_ICON_SET2 = (By.XPATH, "//pkm-modal-window//*[text()=' Добавить иконки ']")
    ADD_ICON_TO_SET = (By.XPATH, "/html/body/pkm-app-root/div/pkm-main/div/div/ks-settings/div/ks-tabs-group/div[2]/ks-global-icons-settings/div[1]/ks-icons-set[4]/div/div/div[2]/ks-button/button/div")
    ADD_ICON_TO_SET_INPUT = (By.XPATH, "/html/body/pkm-modal-window-outlet/ks-icon-add/pkm-modal-window/div/div/div[3]/div/div/span")
    LOCATOR_EDIT_ICON_SET = (By.CSS_SELECTOR, "body > pkm-app-root > div > pkm-main > div > div > ks-settings > div > ks-tabs-group > div.tab-body > ks-global-icons-settings > div.wrapper > ks-icons-set:nth-child(5) > div > div > div:nth-child(2) > fa-icon.ng-fa-icon.icons-set__configuration-panel__icon.mr-r-9.ng-star-inserted > svg")
    LOCATOR_FIRST_ICON = (By.XPATH, "//pkm-modal-window//img")
    LOCATOR_INPUT_NAME_ICON = (By.XPATH, "//pkm-modal-window//input[contains(@placeholder, 'Введите название иконки')]")
    LOCATOR_TWO_ICON = (By.XPATH, "//pkm-modal-window//img/following::img[1]")
    LOCATOR_DEL_ICON = (By.XPATH, "//pkm-modal-window//*[text()=' Удалить иконку ' or text()='Удалить иконку']")
    LOCATOR_DEL_ICON_SET = (By.CSS_SELECTOR, "body > pkm-app-root > div > pkm-main > div > div > ks-settings > div > ks-tabs-group > div.tab-body > ks-global-icons-settings > div.wrapper > ks-icons-set:nth-child(5) > div > div > div:nth-child(2) > fa-icon.ng-fa-icon.icons-set__configuration-panel__icon.mr-l-9.ng-star-inserted > svg")
    LOCATOR_ICON_SET_AFTER_EDIT = (By.XPATH, "//pkm-app-root//*[text()=' Тестовый набор_copy (2) ']")

    LOCATOR_ADD_NEW_ROLE = (By.XPATH, "//pkm-app-root//*[text()='Роль']")
    LOCATOR_INPUT_ROLE_NAME = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Название роли')]")
    LOCATOR_INPUT_ROLE_DESCRIPTION = (By.XPATH, "//pkm-app-root//textarea[contains(@placeholder, 'Описание роли')]")
    LOCATOR_CREATE_NEW_ROLE = (By.XPATH, "//pkm-app-root//*[text()='Создать роль']")
    LOCATOR_SEARCH_ROLE_NAME = (By.XPATH, "//pkm-app-root//input[contains(@placeholder, 'Поиск')]")
    LOCATOR_AUTOTEST_ROLE = (By.XPATH, "//pkm-app-root//*[text()='autotest_role']")
    LOCATOR_RADIO_BUTTON_ALLOW_ALL = (By.XPATH, "//pkm-app-root//ks-radio//ks-radio-item[3]/div/label/div/div")
    LOCATOR_RADIO_BUTTON_INDICATORS = (By.XPATH, "//pkm-app-root//ks-tabs-group//ks-switch/div/div[1]/div")
    LOCATOR_SAVE_EDIT_ROLE = (By.XPATH, "//pkm-app-root//ks-roles-edit//button/div[contains(@class, 'ks-button__container') and .='']")
    LOCATOR_DEL_TEST_ROLE = (By.XPATH, "//pkm-app-root//*[text()='Удалить роль']")



    def __init__(self, driver):
        super().__init__(driver),
        self.profile_page = UserProfilePage(driver)

    def switch_to_page(self):
        self.sidebar.select_page('Пользователи')
        self.wait_element_stable(self.LOCATOR_USERS_PAGE, 3)

    def switch_to_page_backup(self):
        self.sidebar.select_page('Резервное копирование')
        self.wait_element_stable(self.LOCATOR_BACKUP_PAGE, 3)

    def click_button_restore_backup(self):
        self.find_and_click(self.RESTORE_BACKUP_BTN)
        self.wait_element_stable(self.LOCATOR_BACKUP_MODAL_PAGE, 3)

    def click_button_create_copy(self):
        self.find_and_click(self.CREATE_BACKUP_BTN)
        self.wait_element_stable(self.LOCATOR_CREATE_BACKUP_MODAL_PAGE, 3)

    def select_object_for_backup(self, Project_name):
        self.find_and_click(self.LOCATOR_DROPDOWN_CHOICE_PROJECT)
        time.sleep(2)
        self.find_element(self.INPUT_PROJECT_NAME).send_keys(Project_name)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ONLY_AUTOTEST_PROJECT)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CONTINUE_BTN)
        time.sleep(2)
        self.wait_element_stable(self.LOCATOR_BACKUP_CHECK, 14)
        time.sleep(2)

    def mark_entities_for_backup(self):
        self.find_and_click(self.LOCATOR_CHECKBOX_REFERENCES)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_CLASSES)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_CLASSES)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_CLASSES)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_MODELS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_MODELS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_DIAGRAM)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_DIAGRAM)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_TEMPLATES)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_TEMPLATES)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_RESTRICTIONS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_RESTRICTIONS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_INTERFACE)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_INTERFACE)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_APPLICATION)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_APPLICATION)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_INTEGRATION)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_INTEGRATION)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_CHECK_BPMS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_BPMS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_NEXT_BTN)
        time.sleep(1)
        self.find_element(self.LOCATOR_PASSWORD_FIELD).clear()
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CREATE_COPY_BTN)
        time.sleep(7)

    def check_backup_creation(self):
        self.wait_element_stable(self.locator_successfully_backup, 12)
        assert self.find_element(self.locator_successfully_backup), "Ошибка в создании бэкапа проета ONLY_AUTOTEST!!!"
        time.sleep(1)


    def fill_fields_backup_modal(self, Project_name, String_filepath):
        self.find_element(self.LOCATOR_PROJECT_NAME).send_keys(Project_name)
        self.find_element(self.LOCATOR_FILE_NAME).send_keys(String_filepath)
        self.find_element(self.LOCATOR_PASSWORD_FIELD).clear()
        time.sleep(1)
        self.find_and_click(self.LOCATOR_NEXT_BTN)
        self.wait_element_stable(self.LOCATOR_SUCCESSFUL_BACKUP, 8)
        self.find_and_click(self.LOCATOR_CONTINUE_BTN)

    def switch_to_page_project(self, Project_name):
        self.sidebar.select_page('Проекты')
        time.sleep(2)
        self.find_element(self.PROJECT_SEARCH_FIELD).send_keys(Project_name)
        time.sleep(2)

    def del_backup_project(self):
        self.find_and_click(self.project_locator)
        self.find_and_click(self.DEL_PROJECT_BUTTON)
        self.find_and_click(self.CONFIRM_BUTTON)
#        self.find_and_click(self.PROJECT_SEARCH_FIELD)
#        self.find_element(self.PROJECT_SEARCH_FIELD).send_keys('Autotest_project')
        time.sleep(1)
        assert self.find_element_disabled(self.project_locator), "Проект Autotest_project не удалось удалить !!!"

    def del_backup_project2(self):
        self.find_and_click(self.project_locator2)
        self.find_and_click(self.DEL_PROJECT_BUTTON)
        self.find_and_click(self.CONFIRM_BUTTON)
        time.sleep(1)
        assert self.find_element_disabled(self.project_locator2), "Проект Autotest_project не удалось удалить !!!"

    def should_be_projekt_available(self):
        assert self.find_element(self.project_locator), "Проект не удалось восстановить!!!"
        time.sleep(1)

    def should_be_projekt_available2(self):
        time.sleep(1)
        assert self.find_element(self.project_locator2), "Проект не удалось создать!!!"
        time.sleep(1)

    def click_add_user(self):
        self.find_and_click(self.LOCATOR_ADD_USER)
        time.sleep(1)
        print('1')

    def filling_new_user_data(self, First_name, Last_name, Middle_name, Login, Email, Password_user):
        self.find_element(self.FIRST_NAME_FIELD).send_keys(First_name)
        self.find_element(self.LAST_NAME_FIELD).send_keys(Last_name)
        self.find_element(self.MIDLE_NAME_FIELD).send_keys(Middle_name)
        self.find_element(self.LOGIN_FIELD).send_keys(Login)
        self.find_element(self.EMAIL_FIELD).send_keys(Email)
        self.find_element(self.PASSWORD_FIELD).send_keys(Password_user)
        self.find_element(self.PASSWORD_CONFIRM_FIELD).send_keys(Password_user)
        time.sleep(2)
        self.find_and_click(self.SAVE_BUTTON)


    def select_user(self, login: str):
        User = 'Иванов Четвертый'
        self.sidebar.search_user(User)
        target_locator = (By.XPATH, f"//tr[(.//td[2])[.='{login}']]")
        target_row = self.find_element(target_locator, time=4)
        time.sleep(2)
        target_row.click()

    def select_new_user(self):
        User = 'Иван Иванов'
        self.sidebar.search_user(User)
        self.find_and_click(self.target_locator)
        time.sleep(2)


    def deleting_new_user(self):
        self.find_and_click(self.DEL_USER_BUTTON)
        time.sleep(1)
        self.find_and_click(self.CONFIRM_BUTTON)
        time.sleep(1)

    def should_be_user_deleting(self):
        self.sidebar.search_user()
        assert self.find_element_disabled(self.target_locator), "Пользователя eu_user5 не удалось удалить !!!"

    def click_to_page_project(self):
        self.sidebar.select_page('Проекты')
        time.sleep(2)

    def click_to_create_new_project(self):
        self.find_and_click(self.CREATE_NEW_PROJECT_BTN)

    def create_new_name_project(self, Project_name):
        self.find_element(self.LOCATOR_INPUT_NAME_PROJECT).send_keys(Project_name)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_PROJECT_BTN)

    def add_new_access_to_project(self, User_name, Role_name):
        self.find_and_click(self.LOCATOR_ACCESS_BTN)
        self.find_and_click(self.LOCATOR_ADD_USER_BTN)
        self.find_element(self.LOCATOR_SEARCH_BY_USER).send_keys(User_name)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_USER)
        self.find_and_click(self.LOCATOR_ROLE_BTN)
        self.find_element(self.LOCATOR_SEARCH_BY_ROLE).send_keys(Role_name)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CHECKBOX_ROLE)
        self.find_and_click(self.LOCATOR_ADD_BTN)
        time.sleep(1)

    def open_access_new_roles_and_users(self):
        self.find_and_click(self.LOCATOR_ACCESS1)
        self.find_and_click(self.LOCATOR_ACCESS2)
        self.find_and_click(self.LOCATOR_ACCESS3)
        time.sleep(2)

    def add_new_source_to_project(self, option_name: str):
        self.find_and_click(self.LOCATOR_SOURCE_BTN)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_SOURCE_BTN)
        time.sleep(2)
#        self.is_element_clickable(self.LOCATOR_CHECKBOX_SOURCE)
#        time.sleep(2)
        checkbox_locator = self.displaying_option_checkbox_locator_creator(option_name)
        if "checkbox-icon_hidden" in self.get_element_html(checkbox_locator):
            self.find_and_click(checkbox_locator)

        self.find_and_click(self.LOCATOR_CHECKBOX_SOURCE)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_BTN)

    def add_new_display_to_project(self, String_filepath):
        self.find_and_click(self.LOCATOR_DISPLAY_BTN)
        time.sleep(1)
        self.find_element(self.LOCATOR_ADD_IMAGE).send_keys(String_filepath)
        time.sleep(3)

    def save_new_project(self):
        self.find_and_click(self.SAVE_BUTTON)
        time.sleep(1)

    def click_to_page_setting(self):
        self.sidebar.select_page('Настройки')
        time.sleep(2)

    def click_to_page_roles(self):
        self.sidebar.select_page('Роли')
        time.sleep(2)

    def create_new_calendar(self, Calendar_name):
        self.find_and_click(self.LOCATOR_CALENDAR_TAB)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_CALENDAR_BTN)
        time.sleep(1)
        self.find_element(self.LOCATOR_INPUT_CALENDAR_NAME).send_keys(Calendar_name)
        self.find_element(self.LOCATOR_INPUT_WORKING_DAY).send_keys('6')
        self.find_element(self.LOCATOR_INPUT_WEEKEND_DAY).send_keys('1')
        self.find_and_click(self.LOCATOR_COPY_DATA_FROM_CALENDAR)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CALENDAR_DEFAULT)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_COUNTDOWN)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CALENDAR_NUMBER)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_BTN)
        time.sleep(1)

    def edit_new_calendar(self, Calendar_name_2):
        self.hover_over_element(self.LOCATOR_CALENDAR_TEST)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CALENDAR_TEST_EDIT)
        time.sleep(1)
        self.find_element(self.LOCATOR_INPUT_CALENDAR_NAME).clear()
        time.sleep(1)
        self.find_element(self.LOCATOR_INPUT_CALENDAR_NAME).send_keys(Calendar_name_2)
        self.find_element(self.LOCATOR_INPUT_WORKING_DAY).clear()
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_WORKING_DAY).send_keys('5')
        self.find_element(self.LOCATOR_INPUT_WEEKEND_DAY).clear()
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_WEEKEND_DAY).send_keys('2')
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON)
        time.sleep(1)

    def set_day_off_for_calendar(self, Calendar_comment):
        self.find_and_click(self.LOCATOR_SET_CALENDAR_DAY)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_COUNTDOWN)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CALENDAR_NUMBER)
        self.find_and_click(self.LOCATOR_RADIOBUTTON_DAYOFF)
        time.sleep(1)
        self.find_element(self.LOCATOR_ADD_COMMENT_FOR_CALENDAR_DAY).send_keys(Calendar_comment)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_BTN)

    def delete_test_calendar(self):
        self.hover_over_element(self.LOCATOR_CALENDAR_TEST_AFTER_EDIT)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_CALENDAR_TEST_DEL)
        time.sleep(2)
        self.find_and_click(self.CONFIRM_BUTTON_DEL_CALENDAR)
        assert self.find_element_disabled(self.LOCATOR_CALENDAR_TEST_AFTER_EDIT), "Каледнарь Test_calendar_copy не удалось удалить!!!"

    def create_new_font(self, Font_name, System_font_name, File_type, String_filepath):
        self.find_and_click(self.LOCATOR_FONT_TAB)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_FONT)
        time.sleep(1)
        self.find_element(self.LOCATOR_INPUT_FONT_NAME).send_keys(Font_name)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_SYSTEM_FONT_NAME).send_keys(System_font_name)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_FILE_TYPE)
        time.sleep(1)
        self.find_element(self.LOCATOR_FILE_TYPE_SEARCH).send_keys(File_type)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_FILE_TYPE_OPENTYPE)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_ADD_FONT).send_keys(String_filepath)
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON)

    def delete_test_font(self):
        self.hover_over_element(self.LOCATOR_FONT_TEST_DEL)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_FONT_TEST_DEL)
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON)
        time.sleep(0.5)
        assert self.find_element_disabled(self.LOCATOR_FONT_TEST_AFTER_EDIT), "Тестовый шрифт не удалось удалить!!!"

    def create_new_icon_set(self):
        self.find_and_click(self.LOCATOR_ICON_TAB)
        time.sleep(1)
        payload = {"login":"admin","password":"Password2"}
        resp = requests.post('https://dev.ks.works/api/auth/login', data=json.dumps(payload))
        result = json.loads(resp.text)
        result2 = result.get('token')

        token = {"Authorization": f"Bearer {result2}"}
        print(token)

#        token = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlcyI6WyJmNjEwZGZkZC0wN2Y2LTQzNmMtYjIxOS0zZDU3ZDBkNWU4MDUiLCJiMTRlYjVmNi1iOTlkLTRjMWQtYTE3Ni1hYjQyZTQ2OWZlMDAiLCIwMWVkNzQ3OS04NGJiLWZiOWQtOTc2YS0wMGIxNWMwYzQwMDAiLCI5MmY5YjRjNi01OWRjLTQzMGUtOWU1ZS1lMjRkMWY0MDYwNDgiLCIxNzZkZWMwMS00NjM3LTRjNTktODBkMS1kOTY3ZWYyN2RhMTQiLCJkYTY1OGYzYS1lZjE1LTQ5ZDktOTlmNi04MGMwNjdiZDM0Y2YiLCIwMWVkMmE3ZC1kOTYzLTFmZWYtNDRlNi0wMGIxNWMwYzQwMDAiLCIwMWVkMWM5Mi04ZDRmLTIwYTgtZDg1Yy0wMGIxNWMwYzQwMDAiLCIwMWVjZWUwOC1lMDczLTBlMGItNTU2Ni0wMGIxNWMwYzQwMDAiLCIwMWVjOTYyNC00ODJlLTU2MmYtYWM1NS0wMGIxNWMwYzQwMDAiLCIwMWVkMzhiMi1iZDY4LTc5MmMtZmIwYi0wMGIxNWMwYzQwMDAiLCIzYmJiMWFiOC0wZWVmLTExZWItYTkxMS0wMjQyYWMxNzExMDIiLCIwMWVkNzQ1ZC1iM2ViLTQ0YjUtOTc2Mi0wMGIxNWMwYzQwMDAiLCIwMWViZTg3OS0zZWVkLWQ1MmQtZDBjYy0wMGIxNWMwYzQwMDAiLCI4YjBmNmJjYy05MjI5LTQ3ZjAtOGNjYy1iNjc0MTBhYmJhYmIiLCIwMWVjNTM1Yy01NWYyLTA0MTYtMmJjNC0wMGIxNWMwYzQwMDAiLCIzYmJiMTRiZS0wZWVmLTExZWItYTkxMS0wMjQyYWMxNzExMDIiLCIzYmJiMTk4Mi0wZWVmLTExZWItYTkxMS0wMjQyYWMxNzExMDIiXSwiZG9tYWluIjoiIiwibG9naW4iOiJhZG1pbiIsInRtcF90b2tlbiI6ZmFsc2UsImV4cCI6MTY3MTAxMDA4MSwianRpIjoiMDFlYjBlZWYtM2NlMC0xZTgwLWE4YjktMDAwMDAwMDAwMDAwIn0.J4uYYegIsDB70k0yFKt1YmHkQz5V4aTsMyOf-yHOJ_M"}
        payload = {
    "iconsSet": [
        {
            "iconFileUuid": "01ed707c-d27b-e74b-b934-00b15c0c4000",
            "iconName": "one.png",
            "projectIconsSetUuid": ""
        },
        {
            "iconFileUuid": "01ed707c-d3cc-4adc-b934-00b15c0c4000",
            "iconName": "three.png",
            "projectIconsSetUuid": ""
        },
        {
            "iconFileUuid": "01ed707c-d501-f222-b934-00b15c0c4000",
            "iconName": "two.png",
            "projectIconsSetUuid": ""
        }
    ],
    "setName": "Тестовый набор"
        }
        response = requests.post('https://dev.ks.works/api/project-icons-set/create', headers=token, json=payload)
        print(response.text)

        time.sleep(1)
        self.find_and_click(self.LOCATOR_BACKUP_TAB)
        time.sleep(1)

    def add_icon_to_set_icon(self, Icon_set_name):

        self.find_and_click(self.LOCATOR_ICON_TAB)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_ADD_ICON_SET)
        time.sleep(1)
        self.find_element(self.LOCATOR_NEW_SET_ICON_NAME).send_keys(Icon_set_name)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON)

    def add_icon_to_new_set(self, String_filepath1):
        self.find_and_click(self.ADD_ICON_TO_SET)
        time.sleep(0.5)
        self.find_element(self.ADD_ICON_TO_SET_INPUT).send_keys(String_filepath1)
        self.find_and_click(self.LOCATOR_ADD_BTN)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON)

    def edit_to_new_set_icon(self, Icon_set_name2, Edit_icon_name):
        self.find_and_click(self.LOCATOR_ICON_TAB)
        time.sleep(1)
        self.hover_over_element(self.LOCATOR_EDIT_ICON_SET)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_EDIT_ICON_SET)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_NEW_SET_ICON_NAME).clear()
        self.find_element(self.LOCATOR_NEW_SET_ICON_NAME).send_keys(Icon_set_name2)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_FIRST_ICON)
        self.find_element(self.LOCATOR_INPUT_NAME_ICON).clear()
        self.find_element(self.LOCATOR_INPUT_NAME_ICON).send_keys(Edit_icon_name)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_TWO_ICON)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_DEL_ICON)
        time.sleep(0.5)
        self.find_and_click(self.SAVE_BUTTON_MODAL_WINDOW)
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON)

    def delete_test_icon_set(self):
        self.hover_over_element(self.LOCATOR_DEL_ICON_SET)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_DEL_ICON_SET)
        time.sleep(1)
        self.find_and_click(self.SAVE_BUTTON)
        time.sleep(0.5)
        assert self.find_element_disabled(self.LOCATOR_ICON_SET_AFTER_EDIT), "Тестовый набор иконок не удалось удалить!!!"

    def creating_new_test_role(self, New_test_role, New_test_description):
        self.find_and_click(self.LOCATOR_ADD_NEW_ROLE)
        time.sleep(1)
        self.find_element(self.LOCATOR_INPUT_ROLE_NAME).send_keys(New_test_role)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_ROLE_DESCRIPTION).send_keys(New_test_description)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_CREATE_NEW_ROLE)
        time.sleep(1)

    def edit_new_test_role(self, New_test_role, New_test_role_edit):
        self.find_element(self.LOCATOR_SEARCH_ROLE_NAME).send_keys(New_test_role)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_AUTOTEST_ROLE)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_ROLE_NAME).clear()
        time.sleep(0.5)
        self.find_element(self.LOCATOR_INPUT_ROLE_NAME).send_keys(New_test_role_edit)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_RADIO_BUTTON_ALLOW_ALL)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_RADIO_BUTTON_INDICATORS)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_SAVE_EDIT_ROLE)
        time.sleep(1)

    def search_new_test_role_and_delete(self, New_test_role_edit):
        self.find_element(self.LOCATOR_SEARCH_ROLE_NAME).send_keys(New_test_role_edit)
        time.sleep(0.5)
        self.find_and_click(self.LOCATOR_AUTOTEST_ROLE)
        time.sleep(1)
        self.find_and_click(self.LOCATOR_DEL_TEST_ROLE)
        time.sleep(0.5)
        self.find_element(self.LOCATOR_SEARCH_ROLE_NAME).send_keys(New_test_role_edit)
        time.sleep(0.5)
        assert self.find_element_disabled(self.LOCATOR_AUTOTEST_ROLE), "Тестовую роль не удалось удалить!!!"





'''
    def select_user(self, login: str):
         target_locator = (By.XPATH, f"//tr[(.//td[2])[.='{login}']]")
         target_row = None
         while not target_row:
             try:
                 target_row = self.find_element(target_locator, time=3)
             except TimeoutException:
                 self.find_and_click(self.LOCATOR_PAGINATION_NEXT_PAGE_BUTTON)
         target_row.click()
'''

class UserProfilePage(NewPage):
    LOCATOR_EDIT_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'edit-password')]")
    LOCATOR_GENERATE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'generate-password')]")
    LOCATOR_SHOW_PASSWORD_BUTTON = (By.XPATH, "//fa-icon[contains(@class, 'eye-password-icon')]")
    LOCATOR_PASSWORD_FIELD = (By.XPATH, "//ks-input[@type='password']//input[@placeholder='Создайте пароль']")
    LOCATOR_CHANGE_PASSWORD_BUTTON = (By.XPATH, "//ks-button[.=' Изменить пароль ']")
    LOCATOR_EDIT_USER_PROFILE_BUTTON = (By.XPATH, "//div[contains(@class,'user-details-form')]//button[.='Редактировать']")




    def change_password(self, new_password: str = None):
        try:
            self.find_and_click(self.LOCATOR_EDIT_PASSWORD_BUTTON)
        except TimeoutException:
            self.find_and_click(self.LOCATOR_EDIT_USER_PROFILE_BUTTON)
            self.find_and_click(self.LOCATOR_EDIT_PASSWORD_BUTTON)
        if new_password:
            pass
        else:
            self.find_and_click(self.LOCATOR_GENERATE_PASSWORD_BUTTON)
            self.find_and_click(self.LOCATOR_SHOW_PASSWORD_BUTTON)
            time.sleep(3)
            actual_password = self.get_input_value(self.LOCATOR_PASSWORD_FIELD)
            assert actual_password
            self.find_and_click(self.LOCATOR_CHANGE_PASSWORD_BUTTON)
            self.modal.accept_modal()
            self.is_element_disappearing(self.LOCATOR_CHANGE_PASSWORD_BUTTON, wait_display=False)
            return actual_password


