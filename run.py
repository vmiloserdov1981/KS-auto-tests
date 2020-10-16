import pytest
from conditions.preconditions_api import ApiPreconditions
import users
import os
from variables import PkmVars as Vars


api_eu = ApiPreconditions(users.admin.login, users.admin.password)


def run_all_tests():
    os.environ['PROJECT_UUID'] = api_eu.get_project_uuid_by_name(Vars.PKM_PROJECT_NAME)
    try:
        api_eu.prepare_data()

        if os.getenv('CLEAR_VIDEOS') == 'true':
            api_eu.clear_videos()
    finally:
        quantity = os.getenv('QUANTITY', '5')

        #print('run tests from green_group')
        #pytest.main([f"-n={quantity}", "-v", "-m", "green_label", "--alluredir=reports"])

        print('run tests from red_group')
        pytest.main([f"-n={quantity}", "-v", "-m", "red_label", "--alluredir=reports"])


run_all_tests()
