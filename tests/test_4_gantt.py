from pages.login_po import LoginPage
from pages.main_po import MainPage
from pages.components.trees import UserBlock
from variables import PkmVars as Vars
from pages.components.modals import Modals
import users as user
import allure


@allure.feature('Интерфейс КП')
@allure.story('План мероприятий')
@allure.title('Создание мероприятия')
@allure.severity(allure.severity_level.CRITICAL)
def test_eu_create_gantt_event(driver_eu_login):
    login_page = LoginPage(driver_eu_login, Vars.PKM_MAIN_URL)
    main_page = MainPage(driver_eu_login, "{}#/main".format(Vars.PKM_MAIN_URL))
    user_block = UserBlock(driver_eu_login)

    with allure.step('Перейти на сайт'):
        pass