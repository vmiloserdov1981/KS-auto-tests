import allure
import pytest
import users
from pages.main.users_po import UsersPage, UserProfilePage
from pages.login_po import LoginPage
from pages.components.modals import ChangePasswordModal
import time


@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Восстанрвить проект из бэкапа')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_restoring_from_backup(driver, parameters):
    #данные
    Project_name = "Autotest_project"
    String_filepath = "C:\Autotest\_backup\_test_backup.json"
    users_page = UsersPage(driver)


    with allure.step(f'Перейти на вкладку "Резервное копирование"'):
        users_page.switch_to_page_backup()

    with allure.step('Нажать на кнопку "Восстановить из копии"'):
        users_page.click_button_restore_backup()

    with allure.step('Заполнить поля карточки и запустить создание бэкапа'):
        users_page.fill_fields_backup_modal(Project_name, String_filepath)
        time.sleep(1)

    with allure.step('Проверка восстановленного проекта'):
        users_page.switch_to_page_project(Project_name)
        users_page.should_be_projekt_available()
        time.sleep(1)

    with allure.step('Удаление проекта'):
        users_page.del_backup_project()
        


@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Создать бэкап проекта')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_creating_backup_project(driver, parameters):
    #данные
    Project_name = "ONLY_AUTOTEST"
    users_page = UsersPage(driver)


    with allure.step(f'Перейти на вкладку "Резервное копирование"'):
        users_page.switch_to_page_backup()
        time.sleep(1)

    with allure.step('Нажать на кнопку "Создать копию"'):
        users_page.click_button_create_copy()

    with allure.step('Выбор проекта для бэкапа"'):
        users_page.select_object_for_backup(Project_name)

    with allure.step('Выделяем сущности для бэкапа"'):
        users_page.mark_entities_for_backup()

    with allure.step('Проверяем, что бэкап успешно создан"'):
        users_page.check_backup_creation()






