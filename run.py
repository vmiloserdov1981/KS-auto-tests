import pytest
from conditions.preconditions_api import ApiEuPreconditions, ApiAdminPreconditions
import users
import os
from variables import PkmVars as Vars
from api.api_projects import ApiProjects

token = ApiEuPreconditions.api_get_token(users.admin.login, users.admin.password, Vars.PKM_API_URL)
project_api = ApiProjects(None, None, None, token=token)
if not os.environ["PROJECT_NAME"]:
    os.environ["PROJECT_NAME"] = Vars.PKM_PROJECT_NAME = project_api.get_last_k6_project_name()
else:
    Vars.PKM_PROJECT_NAME = os.environ["PROJECT_NAME"]
project_uuid = ApiEuPreconditions.get_project_uuid_by_name_static(Vars.PKM_PROJECT_NAME, token)
api_eu = ApiEuPreconditions(None, None, project_uuid, token=token)

for user in users.test_users:
    api_eu.api_check_user(users.test_users[user].login)

project_api.check_project_access([users.test_users[i].login for i in users.test_users], project_uuid)

api_admin = ApiAdminPreconditions(project_uuid, token=token)


def run_all_tests():
    if os.getenv('CLEAR_VIDEOS') == 'true':
        api_eu.clear_videos()

    quantity = os.getenv('QUANTITY', '5')

    # api_eu.prepare_data()

    # print('run tests from green_group')
    # pytest.main([f"-n={quantity}", "-v", "-m", "green_label", "--alluredir=reports"])

    api_admin.prepare_data()

    print('run tests from red_group')
    pytest.main([f"-n={quantity}", "-v", "-m", "red_label", "--alluredir=reports"])


run_all_tests()
