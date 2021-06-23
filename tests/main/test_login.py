import allure
import pytest
from variables import PkmVars as Vars
import users
from pages.main_po import MainPage


@allure.feature('Главная страница')
@allure.story('Логин/Логаут')
@allure.title('Сброс пароля пользователя')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.red_label
@pytest.mark.parametrize("parameters", [({
        'use_admin': True,
        'name': 'Управление сущностями дерева классов'
    })])
def test_password_recovery(driver, parameters):
    main_page = MainPage(driver)
    profile_page = main_page.users_page.profile_page
    target_user_login = users.test_users["eu_user4"].login

    with allure.step(f'Перейти на вкладку "Списки пользователей"'):
        main_page.switch_to_users_page()

    with allure.step(f'Перейти в профиль пользователя с логином {target_user_login}'):
        main_page.users_page.select_user(target_user_login)

    with allure.step('Сгенерировать новый пароль поьзователя'):
        new_pass = profile_page.change_password()

