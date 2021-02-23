import pytest
from selenium import webdriver
import allure
from conditions.preconditions_ui import PreconditionsFront
import users as user
from conditions.preconditions_api import ApiPreconditions
from variables import PkmVars as Vars
import os
from webdriver_manager.chrome import ChromeDriverManager
import json
from conditions.clean_factory import delete as delete_entity


def driver_init(maximize=True, impl_wait=3, name=None, project_uuid=None, token=None):
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
            "sessionTimeout": timeout,
            "goog:loggingPrefs": {'browser': 'ALL'}
        }
        driver = webdriver.Remote(
            command_executor=ip,
            desired_capabilities=capabilities)
    driver.test_data = {'to_delete': []}
    driver.is_test_failed = False
    driver.token = token
    driver.project_uuid = project_uuid
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
                        web_driver.is_test_failed = True
                        attachments_creator = AttachmentsCreator(web_driver)
                        attachments_creator.attach_data()
                        return
                print('Fail to take screen-shot')
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))


@pytest.fixture()
def driver(parameters):
    """
       parameters = {
           'name': 'Автотест'
       }
       """
    driver = driver_init(name=parameters.get('name'))
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
    project_name = parameters.get('project')
    token = ApiPreconditions.api_get_token(user.admin.login, user.admin.password, Vars.PKM_API_URL)
    project_uuid = ApiPreconditions.get_project_uuid_by_name_static(project_name, token) if project_name else None
    driver = driver_init(name=parameters.get('name'), project_uuid=project_uuid, token=token)
    preconditions_api = ApiPreconditions(None, None, project_uuid, token)
    preconditions = PreconditionsFront(driver, project_uuid, token=token)
    with AttachmentsCreator(driver):
        preconditions_api.api_check_user(parameters.get('login'))
        eu_user = user.test_users[parameters.get('login')]
        if parameters.get('get_last_k6_plan'):
            data = {'last_k6_plan': preconditions_api.api_get_last_k6_plan()}
            if parameters.get('get_last_k6_plan_copy'):
                k6_plan_comment = data.get('last_k6_plan').get('settings').get('plan').get('comment')
                k6_plan_uuid = data.get('last_k6_plan').get('uuid')
                data['copy_last_k6_plan'] = preconditions_api.check_k6_plan_copy(k6_plan_comment, k6_plan_uuid)
            data['to_delete'] = []
            with allure.step(f'Сохранить тестовые данные {data} в драйвере'):
                driver.test_data = data
            preconditions.login_as_eu(eu_user.login, eu_user.password, parameters.get('project'))
            if parameters.get('select_last_k6_plan'):
                preconditions.view_last_k6_plan()
            elif parameters.get('select_last_k6_plan_copy'):
                preconditions.view_last_k6_plan_copy()
        else:
            preconditions.login_as_eu(eu_user.login, eu_user.password, parameters.get('project'))

    yield driver

    with AttachmentsCreator(driver):
        if driver.test_data.get('to_delete'):
            with allure.step(f'Удалить тестовые данные'):
                for entity in driver.test_data.get('to_delete'):
                    delete_entity(entity)
    driver.quit()


@pytest.fixture()
def parametrized_login_admin_driver(parameters):
    """
    parameters = {
        'login': 'eu_user',
        'use_admin': False,
        'project': 'Шельф. Приразломная',
        'tree_type': 'Справочники',
        'name': 'Автотест'
    }
    """
    project_name = parameters.get('project')
    token = ApiPreconditions.api_get_token(user.admin.login, user.admin.password, Vars.PKM_API_URL)
    project_uuid = ApiPreconditions.get_project_uuid_by_name_static(project_name, token) if project_name else None
    driver = driver_init(name=parameters.get('name'), project_uuid=project_uuid, token=token)
    preconditions_api = ApiPreconditions(None, None, project_uuid, token)
    preconditions_ui = PreconditionsFront(driver, project_uuid, token=token)
    with AttachmentsCreator(driver):
        if not parameters.get('use_admin'):
            preconditions_api.api_check_user(parameters.get('login'))
            ai_user = user.test_users[parameters.get('login')]
            preconditions_ui.login_as_admin(ai_user.login, ai_user.password, parameters.get('project'))
            driver.current_user = ai_user
        else:
            preconditions_ui.login_as_admin(user.admin.login, user.admin.password, parameters.get('project'))
            driver.current_user = user.admin
        if parameters.get('tree_type'):
            preconditions_ui.set_tree(parameters.get('tree_type'))

    yield driver

    with AttachmentsCreator(driver):
        if driver.test_data.get('to_delete'):
            with allure.step(f'Удалить тестовые данные'):
                for entity in driver.test_data.get('to_delete'):
                    delete_entity(entity)

    driver.quit()


class AttachmentsCreator:
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.driver.is_test_failed = True
            self.attach_data()
            self.driver.quit()

    def attach_data(self):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG
        )
        logs = json.dumps(self.driver.get_log('browser'))
        allure.attach(
            logs,
            name='logs',
            attachment_type=allure.attachment_type.JSON
        )
