from api.api_classes import ApiClasses
from api.api_models import ApiModels
from api.api_dictionaries import ApiDictionaries
from api.api import ApiEu
from variables import PkmVars as Vars
import users
import os
import requests
from lxml import html


class ApiEuPreconditions(ApiEu):

    def prepare_data(self):
        print('start prepare EU test data')
        k6_plan = self.api_get_last_k6_plan()
        k6_plan_comment = k6_plan.get('settings').get('plan').get('comment')
        k6_plan_uuid = k6_plan.get('uuid')

        for username in users.test_users:
            user = users.test_users.get(username)
            self.api_check_user(user.login, ignore_error=False)

        self.check_k6_plan_copy(k6_plan_comment, k6_plan_uuid, ignore_error=True)
        print('prepare EU test data successful')

    @staticmethod
    def clear_videos():
        ip = os.getenv('SELENOID_IP', '127.0.0.1')
        print(f'start clear videos on {ip}')
        page = requests.get(f'http://{ip}:8080/video')
        webpage = html.fromstring(page.content)
        names = webpage.xpath('//a/@href')
        for i in names:
            url = f'http://{ip}:4444/video/{i}'
            requests.delete(url)
        print('finish clear videos')

    def api_check_user(self, user_login, ignore_error=False):
        user = users.test_users[user_login]
        eu_user = self.api_get_user(user.login, user.name)
        if not eu_user:
            eu_user_uuid = self.api_create_user(f'autouser_{user_login}@test.com', user.login, user.password, user.name, {}, ignore_error=ignore_error)
            self.api_set_admin_role(eu_user_uuid)


class ApiAdminPreconditions:

    def __init__(self, project_uuid, login=None, password=None, token=None, api_url=Vars.PKM_API_URL):
        self.model_api = ApiModels(login, password, project_uuid, token=token, api_url=api_url)
        self.classes_api = ApiClasses(login, password, project_uuid, token=token, api_url=api_url)
        self.dictionaries_api = ApiDictionaries(login, password, project_uuid, token=token, api_url=api_url)

    def prepare_data(self):
        print('Check all autotest folders')
        self.check_autotest_folders()

    def prepare_workshop_data(self):
        print('Check all workshop folders')
        self.check_workshop_folders()

    def check_autotest_folders(self):
        self.model_api.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)
        self.classes_api.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)
        self.dictionaries_api.check_test_folder(Vars.PKM_TEST_FOLDER_NAME)

    def check_workshop_folders(self):
        '''
        current_date = self.classes_api.get_utc_date()
        unique_workshop_folder_name = self.classes_api.create_unique_folder_name(f'{Vars.PKM_WORKSHOP_TEST_FOLDER_NAME}_{current_date[0]}-{current_date[1]}-{current_date[2]}')
        os.environ["WORKSHOP_FOLDER_NAME"] = Vars.PKM_WORKSHOP_TEST_FOLDER_NAME = unique_workshop_folder_name
        self.model_api.check_test_folder(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)
        self.classes_api.check_test_folder(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)
        self.dictionaries_api.check_test_folder(Vars.PKM_WORKSHOP_TEST_FOLDER_NAME)
        '''
        os.environ["WORKSHOP_FOLDER_NAME"] = Vars.PKM_WORKSHOP_TEST_FOLDER_NAME = 'workshop_30-08-2021_1'
