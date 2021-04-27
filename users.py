class PkmUsers:
    def __init__(self, login, password, name=None):
        self.login = login
        self.password = password
        self.name = name


admin = PkmUsers('admin', 'Password1', name='админ новый админ новый')
invalid_pass_user = PkmUsers('admin', 'asdf')
invalid_login_user = PkmUsers('asdf', 'admin')
invalid_user = PkmUsers('asdf', 'asdf')
system_user = PkmUsers('system', None)

test_users = {
    'eu_user': PkmUsers('eu_user', 'Euuser01', name='Иванов Андрей'),
    'eu_user2': PkmUsers('eu_user2', 'Euuser01', name='Иванов Второй'),
    'eu_user3': PkmUsers('eu_user3', 'Euuser01', name='Иванов Третий')
}
