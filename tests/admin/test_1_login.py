from pages.login_po import LoginPage
from pages.main_po import MainPage
from pages.components.trees import UserBlock
from variables import PkmVars as Vars
from pages.components.modals import Modals
import users as user
import allure
import pytest


@allure.feature('Логин/Логаут')
@allure.story('Логин админом')
@allure.title('Логин (валидный логин и пароль)')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.run(order=1)
def test_pkm_login_valid(driver):
    login_page = LoginPage(driver, Vars.PKM_MAIN_URL)
    main_page = MainPage(driver, "{}#/main".format(Vars.PKM_MAIN_URL))
    user_block = UserBlock(driver)

    with allure.step('Перейти на сайт'):
        login_page.go_to_site()

    with allure.step('Ввести логин {} в поле лонина'.format(user.admin.login)):
        login_page.enter_login(user.admin.login)

    with allure.step('Ввести пароль {} в поле пароля'.format(user.admin.password)):
        login_page.enter_pass(user.admin.password)

    with allure.step('Нажать кнопку "Войти как администратор"'):
        login_page.login_as_admin()

    with allure.step('Проверить, что вошли как пользователь "{}" в режим администратора'.format(user.admin.name)):
        user_block.check_username(user.admin.name)

    with allure.step('Проверить, что перешли на главную страницу по правильному URL'):
        main_page.check_url(driver)


@allure.feature('Логин/Логаут')
@allure.story('Логин админом')
@allure.title('Логин с невалидными данными')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.run(order=2)
def test_pkm_login_invalid(driver):
    login_page = LoginPage(driver, Vars.PKM_MAIN_URL)
    modal = Modals(driver)

    with allure.step('Перейти на сайт'):
        login_page.go_to_site()

    with allure.step('Ввести валидный логин "{}" в поле лонина'.format(user.invalid_pass_user.login)):
        login_page.enter_login(user.invalid_pass_user.login)

    with allure.step('Ввести невалидный пароль {} в поле пароля'.format(user.invalid_pass_user.password)):
        login_page.enter_pass(user.invalid_pass_user.password)

    with allure.step('Нажать кнопку "Войти как администратор"'):
        login_page.login_as_admin()

    with allure.step('Проверить, отображение окна с ошибкой'):
        modal.check_error_displaying(wait_disappear=True)

    with allure.step('Ввести невалидный логин "{}" в поле лонина'.format(user.invalid_login_user.login)):
        login_page.enter_login(user.invalid_login_user.login)

    with allure.step('Ввести валидный пароль {} в поле пароля'.format(user.invalid_login_user.password)):
        login_page.enter_pass(user.invalid_login_user.password)

    with allure.step('Нажать кнопку "Войти как администратор"'):
        login_page.login_as_admin()

    with allure.step('Проверить, отображение окна с ошибкой'):
        modal.check_error_displaying(wait_disappear=True)

    with allure.step('Ввести невалидный логин "{}" в поле лонина'.format(user.invalid_user.login)):
        login_page.enter_login(user.invalid_user.login)

    with allure.step('Ввести невалидный пароль {} в поле пароля'.format(user.invalid_user.password)):
        login_page.enter_pass(user.invalid_user.password)

    with allure.step('Нажать кнопку "Войти как администратор"'):
        login_page.login_as_admin()

    with allure.step('Проверить, отображение окна с ошибкой'):
        modal.check_error_displaying(wait_disappear=True)


@allure.feature('Логин/Логаут')
@allure.story('Логаут админа')
@allure.title('Логаут')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.run(order=3)
def test_pkm_logout(driver_login):
    login_page = LoginPage(driver_login, f'{Vars.PKM_MAIN_URL}#/login')
    user_block = UserBlock(driver_login)

    with allure.step('Нажать кнопку выхода'):
        user_block.logout()

    with allure.step('Проверить переход на страницу логина'):
        login_page.check_page()

    with allure.step('Проверить отсутствие токена'):
        assert login_page.get_local_token() is None or login_page.get_local_token() == 'null', 'Неверный токен'
