import pytest
from selenium import webdriver
import allure
from conditions.preconditions_ui import PreconditionsFront
import users as user
from conditions.preconditions_api import ClassesPreconditions
from conditions.postconditions_api import ClassesPostconditions
from conditions.preconditions_api import ApiPreconditions
from conditions.postconditions_api import EuPostconditions
from variables import PkmVars as Vars
import os
from webdriver_manager.chrome import ChromeDriverManager


def driver_init(maximize=True, impl_wait=3, name=None):
    if name is None:
        name = 'autotest'
    if os.getenv('IS_LOCAL') == 'true':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        ip = os.getenv('SELENOID_IP', '127.0.0.1')
        ip = f'http://{ip}:4444/wd/hub'
        enable_video = True if os.getenv('ENABLE_VIDEO') == 'true' else False
        timeout = os.getenv('TIMEOUT', '90s')
        capabilities = {
            "browserName": "chrome",
            # "version": "83.0",
            "enableVNC": True,
            "enableVideo": enable_video,
            'videoName': f'{name}.mp4',
            "name": name,
            "sessionTimeout": timeout
        }
        driver = webdriver.Remote(
            command_executor=ip,
            desired_capabilities=capabilities)
    driver.test_data = {}
    driver.token = None
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
    preconditions.login_as_admin(user.admin.login, user.admin.password, Vars.PKM_PROJECT_NAME)
    yield driver
    driver.quit()


@pytest.fixture()
def parametrized_login_driver(parameters):
    """
    parameters = {
        'login': 'eu_user',
        'get_last_k6_plan': True,
        'get_last_k6_plan_copy': False,
        'select_last_k6_plan': True,
        'select_last_k6_plan_copy': False,
        'project': 'Шельф. Приразломная'
        'name': 'test_name'
    }
    """
    driver = driver_init(name=parameters.get('name'))
    preconditions_api = ApiPreconditions(user.admin.login, user.admin.password)
    preconditions = PreconditionsFront(driver, login=user.admin.login, password=user.admin.password)
    preconditions_api.api_check_user(parameters.get('login'))
    eu_user = user.test_users[parameters.get('login')]
    if parameters.get('get_last_k6_plan'):
        data = {'last_k6_plan': preconditions_api.api_get_last_k6_plan()}
        if parameters.get('get_last_k6_plan_copy'):
            k6_plan_comment = data.get('last_k6_plan').get('settings').get('plan').get('comment')
            k6_plan_uuid = data.get('last_k6_plan').get('uuid')
            data['copy_last_k6_plan'] = preconditions_api.check_k6_plan_copy(k6_plan_comment, k6_plan_uuid)
        data['to_delete'] = {}
        with allure.step(f'Сохранить тестовые данные {data} в драйвере'):
            driver.test_data = data
        preconditions.login_as_eu(eu_user.login, eu_user.password, parameters.get('project'))
        if parameters.get('select_last_k6_plan'):
            preconditions.view_last_k6_plan()
        elif parameters.get('select_last_k6_plan_copy'):
            preconditions.view_last_k6_plan_copy()
    else:
        preconditions.login_as_eu(eu_user.login, eu_user.password)
    yield driver
    if driver.test_data.get('to_delete') != {} and driver.test_data.get('to_delete'):
        with allure.step(f'Удалить тестовые данные'):
            postconditions_api = EuPostconditions(login=user.admin.login, password=user.admin.password)
            postconditions_api.test_data_cleaner(driver.test_data)
    driver.quit()


@pytest.fixture()
def parametrized_login_admin_driver(parameters):
    """
    parameters = {
        'login': 'eu_user',
        'project': 'Шельф. Приразломная',
        'tree_type': 'Справочники',
        'name': 'Автотест'
    }
    """
    driver = driver_init(name=parameters.get('name'))
    preconditions_api = ApiPreconditions(user.admin.login, user.admin.password)
    preconditions_ui = PreconditionsFront(driver, login=user.admin.login, password=user.admin.password)
    preconditions_api.api_check_user(parameters.get('login'))
    ai_user = user.test_users[parameters.get('login')]
    preconditions_ui.login_as_admin(ai_user.login, ai_user.password, parameters.get('project'))
    if parameters.get('tree_type'):
        preconditions_ui.set_tree(parameters.get('tree_type'))
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
