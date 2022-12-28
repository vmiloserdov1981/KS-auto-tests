import allure
import pytest
import users
from pages.main.users_po import UsersPage, UserProfilePage
from pages.login_po import LoginPage
from pages.components.modals import ChangePasswordModal
import time
from selenium import webdriver



@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Создание нового проекта')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_create_new_project(driver, parameters):
    #данные
    users_page = UsersPage(driver)
    Project_name = "Test_project_PyCharm"
    User_name = "Иванов Андрей"
    Role_name = "администратор"
    option_name = 'uuu'
#    Source_name = "Global"
    String_filepath = "C:\Autotest\display\_art.png"

    with allure.step('Перейти на вкладку "Проекты"'):
        users_page.click_to_page_project()

    with allure.step('Создать новый проект'):
        users_page.click_to_create_new_project()

    with allure.step('Создаем название проекта'):
        users_page.create_new_name_project(Project_name)

    with allure.step('Добавляем новый доступ проекту'):
        users_page.add_new_access_to_project(User_name, Role_name)

    with allure.step('Открываем доступы для новых ролей и пользователей'):
        users_page.open_access_new_roles_and_users()

    with allure.step('Добавляем новый источник к проекту'):
        users_page.add_new_source_to_project(option_name)

#    with allure.step('Добавляем изображение к проекту'):
#        users_page.add_new_display_to_project(String_filepath)

    with allure.step('Сохраняем проект'):
        users_page.save_new_project()

    with allure.step('Проверка, что проект Test_project_PyCharm успешно создан'):
        users_page.switch_to_page_project(Project_name)
        users_page.should_be_projekt_available2()
        time.sleep(1)

    with allure.step('Удаление проекта'):
        users_page.del_backup_project2()


@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Создание/редактирование нового календаря')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_create_new_calendar(driver, parameters):
    #данные
    users_page = UsersPage(driver)
    Calendar_name = "Test_calendar"
    Calendar_name_2 = "Test_calendar_copy"
    Calendar_comment = "Тестовый день"
    Date_for_copy = "Календарь по умолчанию"

    with allure.step('Перейти на вкладку "Настройки"'):
        users_page.click_to_page_setting()

    with allure.step('Создание нового календаря'):
        users_page.create_new_calendar(Calendar_name)

    with allure.step('Редактирование нового календаря'):
        users_page.edit_new_calendar(Calendar_name_2)
        
    with allure.step('Настроить выходной день для календаря'):
        users_page.set_day_off_for_calendar(Calendar_comment)

    with allure.step('Удаление календаря'):
        users_page.delete_test_calendar()



@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Добавление/редактирование нового шрифта')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_create_new_font(driver, parameters):
    #данные
    users_page = UsersPage(driver)
    Font_name = "Тестовый шрифт"
    System_font_name = "Test_font"
    File_type = "Opentype"
    String_filepath = "C:\Autotest\Type\DynaGroteskLM Bold.otf"

    with allure.step('Перейти на вкладку "Настройки"'):
        users_page.click_to_page_setting()

    with allure.step('Добавление нового шрифта'):
        users_page.create_new_font(Font_name, System_font_name, File_type, String_filepath)

#    with allure.step('Редактирование добавленного шрифта'):
#        users_page.edit_new_font()

    with allure.step('Удаление шрифта'):
        users_page.delete_test_font()
        



@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Добавление/редактирование нового набора иконок')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_create_new_icon_set(driver, parameters):
    #данные
    users_page = UsersPage(driver)
    Icon_set_name = "Тестовый набор2"
    Icon_set_name2 = "Тестовый набор_copy"
    Edit_icon_name = "Тестовая иконка"

    with allure.step('Перейти на вкладку "Настройки"'):
        users_page.click_to_page_setting()
        print('1')

    with allure.step('Создание набора иконок api методом'):
        users_page.create_new_icon_set()

    with allure.step('Перейти на вкладку "Настройки"'):
        users_page.click_to_page_setting()
        print('1')

#    with allure.step('Создание нового набора иконок'):
#        print('5')
#        users_page.add_icon_to_set_icon(Icon_set_name)

#    with allure.step('Добавить иконку к новому набору'):
#        users_page.add_icon_to_new_set(String_filepath1)

    with allure.step('Редактировать набор иконок'):
        users_page.edit_to_new_set_icon(Icon_set_name2, Edit_icon_name)

    with allure.step('Удаление набора иконок'):
        users_page.delete_test_icon_set()



@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Добавление/редактирование тестовой роли')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_create_new_icon_set(driver, parameters):
    #данные
    users_page = UsersPage(driver)
    New_test_role = "autotest_role"
    New_test_role_edit = "autotest_role_copy"
    New_test_description = "autotest_role"

    with allure.step('Перейти на вкладку "Роли"'):
        users_page.click_to_page_roles()
        print('1')

    with allure.step('Создание тестовой роли"'):
        users_page.creating_new_test_role(New_test_role, New_test_description)

    with allure.step('Редактирование новой тестовой роли'):
        users_page.edit_new_test_role(New_test_role, New_test_role_edit)

    with allure.step('Поиск новой роли и удаление'):
        users_page.search_new_test_role_and_delete(New_test_role_edit)



