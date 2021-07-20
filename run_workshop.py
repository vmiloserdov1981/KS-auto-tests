import pytest
from conditions.preconditions_api import ApiEuPreconditions, ApiAdminPreconditions
import users
import os
from variables import PkmVars as Vars
from api.api_projects import ApiProjects

token = ApiEuPreconditions.api_get_token(users.admin.login, users.admin.password, Vars.PKM_API_URL)
project_api = ApiProjects(None, None, None, token=token)
os.environ["PROJECT_NAME"] = Vars.PKM_WORKSHOP_PROJECT_NAME
project_uuid = project_api.check_project(Vars.PKM_WORKSHOP_PROJECT_NAME)
api_eu = ApiEuPreconditions(None, None, project_uuid, token=token)

api_eu.api_check_user(users.workshop_user.login)

project_api.check_project_access([users.workshop_user.login], project_uuid)

api_admin = ApiAdminPreconditions(project_uuid, token=token)


def run_workshop_tests():
    api_admin.prepare_workshop_data()

    print('run workshop test')
    pytest.main(["-v", "tests/workshop/test_workshop.py", "--alluredir=reports"])


run_workshop_tests()
