import pytest
from selenium import webdriver
import allure
from conditions.preconditions_ui import PreconditionsFront
import users as user
from conditions.preconditions_api import ClassesPreconditions
from conditions.postconditions_api import ClassesPostconditions
from conditions.preconditions_api import EuPreconditions
import os
from webdriver_manager.chrome import ChromeDriverManager

'''
первая версия инита


def driver_init_local(headless=False, size=None, maximize=True, impl_wait=3):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    if size:
        options.add_argument(f"window-size={size[0]},{size[1]}")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.test_data = {}
    driver.implicitly_wait(impl_wait)
    driver.set_window_position(0, 0)
    if maximize:
        driver.maximize_window()
    return driver
'''


def driver_init(maximize=True, impl_wait=3):
    if os.getenv('IS_LOCAL'):
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        ip = os.getenv('SELENOID_IP', 'http://127.0.0.1:4444/wd/hub')
        capabilities = {
            "browserName": "chrome",
            # "version": "80.0",
            "enableVNC": True,
            "enableVideo": False
        }
        driver = webdriver.Remote(
            command_executor=ip,
            desired_capabilities=capabilities)
    driver.test_data = {}
    driver.implicitly_wait(impl_wait)
    driver.set_window_position(0, 0)
    if maximize:
        driver.maximize_window()
    return driver


# Фикстура для создания скриншотов при фейле теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                for fixturename in item.fixturenames:
                    if 'driver' in fixturename:
                        web_driver = item.funcargs[fixturename]
                        allure.attach(
                            web_driver.get_screenshot_as_png(),
                            name='screenshot',
                            attachment_type=allure.attachment_type.PNG
                        )
                        return
                print('Fail to take screen-shot')
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))


@pytest.fixture()
def driver():
    driver = driver_init()
    yield driver
    driver.quit()


@pytest.fixture()
def driver_login():
    driver = driver_init()
    preconditions = PreconditionsFront(driver)
    preconditions.login_as_admin(user.admin.login, user.admin.password)
    yield driver
    driver.quit()


@pytest.fixture()
def driver_eu_login():
    driver = driver_init()
    preconditions_api = EuPreconditions(user.admin.login, user.admin.password)
    preconditions = PreconditionsFront(driver)
    preconditions_api.api_check_eu_user()
    data = preconditions_api.create_test_data()
    with allure.step(f'Сохранить тестовые данные {data} в драйвере'):
        driver.test_data = data
    preconditions.login_as_eu(user.eu_user.login, user.eu_user.password)
    yield driver
    driver.quit()


@pytest.fixture(scope='module')
def driver_session():
    driver = driver_init()
    preconditions_api = ClassesPreconditions(user.admin.login, user.admin.password)
    postconditions_api = ClassesPostconditions(user.admin.login, user.admin.password)
    preconditions_ui = PreconditionsFront(driver)
    data = preconditions_api.create_test_data()
    with allure.step(f'Сохранить тестовые данные {data} в драйвере'):
        driver.test_data = data
    preconditions_ui.login_as_admin(user.admin.login, user.admin.password)
    yield driver
    with allure.step(f'Удалить тестовые данные через api'):
        for element in driver.test_data:
            created_node_uuid = driver.test_data.get(element).get('node_uuid')
            try:
                postconditions_api.delete_node(created_node_uuid, check=False)
            except AssertionError:
                pass
        driver.quit()