import pytest
from conditions.preconditions_api import EuPreconditions
import users
import os


api_eu = EuPreconditions(users.admin.login, users.admin.password)


def run_all_tests():
    api_eu.prepare_data()

    if os.getenv('CLEAR_VIDEOS') == 'true':
        api_eu.clear_videos()

    pytest.main(["-n=5", "-v", "-m", "green_label", "--alluredir=reports"])
    pytest.main(["-n=5", "-v", "-m", "red_label", "--alluredir=reports"])


run_all_tests()
