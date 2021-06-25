import allure
import pytest
import users
from pages.main.users_po import UsersPage, UserProfilePage
from pages.login_po import LoginPage
from pages.components.modals import ChangePasswordModal


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
        login_page.login(target_user_login, new_pass, wait_main_page=False)

    with allure.step('Нажать кнопку смены временного пароля'):
        change_pass_modal.accept_changing()

    with allure.step('Сменить пароль на старый'):
        change_pass_modal.change_password(new_pass, target_user_pass)

    with allure.step(f'Войти в систему с логином {target_user_login} и старым паролем'):
        login_page.login(target_user_login, target_user_pass)

    with allure.step('Выйти из системы'):
        profile_page.header.logout()

    with allure.step(f'Войти в систему с логином {target_user_login} и старым паролем'):
        login_page.login(target_user_login, target_user_pass)
