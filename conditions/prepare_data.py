import users
from conditions.preconditions_api import EuPreconditions


preconditions = EuPreconditions(users.admin.login, users.admin.password)
k6_plan = preconditions.api_get_last_k6_plan()
k6_plan_comment = k6_plan.get('settings').get('plan').get('comment')
k6_plan_uuid = k6_plan.get('uuid')

for username in users.test_users:
    user = users.test_users.get(username)
    preconditions.api_check_user(user.login, ignore_error=False)

preconditions.check_k6_plan_copy(k6_plan_comment, k6_plan_uuid, ignore_error=True)
