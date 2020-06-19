class PkmUsers:
    def __init__(self, login, password, name=None):
        self.login = login
        self.password = password
        self.name = name


admin = PkmUsers('admin', 'admin', name='Администратор Не заполнено')
invalid_pass_user = PkmUsers('admin', 'asdf')
invalid_login_user = PkmUsers('asdf', 'admin')
invalid_user = PkmUsers('asdf', 'asdf')
eu_user = PkmUsers('eu_user', 'Euuser01', name='Иванов Андрей')
system_user = PkmUsers('system', None)

all_users = {
    'admin': PkmUsers('admin', 'admin', name='Администратор Не заполнено'),
    'invalid_pass_user': PkmUsers('admin', 'asdf'),
    'invalid_login_user': PkmUsers('asdf', 'admin'),
    'invalid_user': PkmUsers('asdf', 'asdf'),
    'eu_user': PkmUsers('eu_user', 'Euuser01', name='Иванов Андрей'),
    'eu_user2': PkmUsers('eu_user2', 'Euuser01', name='Иванов Второй'),
    'system_user': PkmUsers('system', None)
}
