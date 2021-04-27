import pytest
from conditions.preconditions_api import ApiEuPreconditions, ApiAdminPreconditions
import users
import os
from variables import PkmVars as Vars

token = ApiEuPreconditions.api_get_token(users.admin.login, users.admin.password, Vars.PKM_API_URL)
project_uuid = ApiEuPreconditions.get_project_uuid_by_name_static(Vars.PKM_PROJECT_NAME, token)
api_eu = ApiEuPreconditions(None, None, project_uuid, token=token)
api_admin = ApiAdminPreconditions(project_uuid, token=token)


def run_all_tests():
    if os.getenv('CLEAR_VIDEOS') == 'true':
        api_eu.clear_videos()

    quantity = os.getenv('QUANTITY', '5')

    api_eu.prepare_data()

    print('run tests from green_group')
    pytest.main([f"-n={quantity}", "-v", "-m", "green_label", "--alluredir=reports"])

    api_admin.prepare_data()

    print('run tests from red_group')
    pytest.main([f"-n={quantity}", "-v", "-m", "red_label", "--alluredir=reports"])


run_all_tests()
