import allure
import pytest
import users
from pages.main.users_po import UsersPage, UserProfilePage
from pages.login_po import LoginPage
from pages.components.modals import ChangePasswordModal
import time

'''
@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Сброс пароля пользователя')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])
def test_password_recovery(driver, parameters):
    users_page = UsersPage(driver)
    profile_page = UserProfilePage(driver)
    login_page = LoginPage(driver)
    change_pass_modal = ChangePasswordModal(driver)

    target_user_login = users.test_users["eu_user4"].login
    target_user_pass = users.test_users["eu_user4"].password

    with allure.step(f'Перейти на вкладку "Списки пользователей"'):
        users_page.switch_to_page()

    with allure.step(f'Перейти в профиль пользователя с логином {target_user_login}'):
        users_page.select_user(target_user_login)

    with allure.step('Сгенерировать новый пароль пользователя'):
        new_pass = profile_page.change_password()

    with allure.step('Выйти из системы'):
        profile_page.header.logout()

    with allure.step(f'Войти в систему с логином {target_user_login} и новым паролем'):
        login_page.login(target_user_login, new_pass, wait_main_page=False, check_password_expiration=False)

    with allure.step('Нажать кнопку смены временного пароля'):
        change_pass_modal.accept_changing()

    with allure.step('Сменить пароль на старый'):
        change_pass_modal.change_password(new_pass, target_user_pass)

    with allure.step(f'Попробовать войти в систему с логином {target_user_login} и новым паролем'):
        login_page.login(target_user_login, new_pass, wait_main_page=False)

    with allure.step('Проверить недоступность логина'):
        users_page.not_find_element(users_page.sidebar.LOCATOR_SIDEBAR, timeout=5)

    with allure.step(f'Войти в систему с логином {target_user_login} и старым паролем'):
        login_page.login(target_user_login, target_user_pass)



@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Создание нового пользователя')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_creating_new_user(driver, parameters):
    #данные

    users_page = UsersPage(driver)
    First_name = "Иван"
    Last_name = "Иванов"
    Middle_name = "Пятый"
    Login = "eu_user5"
    Email = "test01@yandex.ru"
    Password_user = "Euuser01"


    with allure.step(f'Перейти на вкладку "Списки пользователей"'):
        users_page.switch_to_page()

    with allure.step('Добавить нового пользователя'):
        users_page.click_add_user()

    with allure.step('Заполнение данных нового пользователя'):
        users_page.filling_new_user_data(First_name, Last_name, Middle_name, Login, Email, Password_user)

    with allure.step('Перейти в профиль пользователя с логином eu_user5'):
        users_page.select_new_user()

    with allure.step('Удаление нового пользователя eu_user5'):
        users_page.deleting_new_user()

    with allure.step('Проверить, что пользователь eu_user5 действительно удален'):
        users_page.should_be_user_deleting()

'''
@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Регистрация нового пользователя')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Сброс пароля пользователя'
    })])

def test_registering_new_user(driver, parameters):
    #данные
    users_page = UsersPage(driver)
    login_page = LoginPage(driver)
    profile_page = UserProfilePage(driver)
    First_name = "Петр"
    Last_name = "Петров"
    Login = "registrationuser1"
    Email = "test02@yandex.ru"
    Password_user = "Euuser01"

    with allure.step('Выйти из системы'):
        profile_page.header.logout()

    with allure.step('Нажать на кнопку регистрация пользователя'):
        login_page.registering()
        time.sleep(1)

    with allure.step('Заполнение данных для регистрации'):
        login_page.filling_regirstration_data_new_user(First_name, Last_name, Login, Email, Password_user)

    with allure.step('Войти под новым пользователем'):
        login_page.registered_user_login(Login, Password_user)

