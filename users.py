import os
from ast import literal_eval


class PkmUsers:
    def __init__(self, login, password, name=None):
        self.login = login
        self.password = password
        self.name = name


admin_credentials = literal_eval(os.getenv('ADMIN_CREDENTIALS', '("admin", "admin")'))
admin = PkmUsers(*admin_credentials)
system_user = PkmUsers('system', None)

test_users = {
    'eu_user': PkmUsers('eu_user', 'Euuser01', name='Иванов Андрей'),
    'eu_user2': PkmUsers('eu_user2', 'Euuser01', name='Иванов Второй'),
    'eu_user3': PkmUsers('eu_user3', 'Euuser01', name='Иванов Третий')
}
