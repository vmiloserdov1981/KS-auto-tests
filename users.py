import os
from ast import literal_eval


class PkmUsers:
    def __init__(self, login, password, name=None):
        self.login = login
        self.password = password
        self.name = name


admin_credentials = literal_eval(os.getenv('ADMIN_CREDENTIALS', '("admin", "Password2")'))
admin = PkmUsers(*admin_credentials)
system_user = PkmUsers('system', None)

test_users = {
    'eu_user': PkmUsers('eu_user', 'Euuser014', name='Иванов Андрей'),
    'eu_user2': PkmUsers('eu_user2', 'Euuser013', name='Иванов Второй'),
    'eu_user3': PkmUsers('eu_user3', 'Euuser013', name='Иванов Третий'),
    'eu_user4': PkmUsers('eu_user4', 'Euuser012', name='Иванов Четвертый')
}
workshop_user = test_users['eu_user']
