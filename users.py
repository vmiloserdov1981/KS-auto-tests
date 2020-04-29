class PkmUsers:
    def __init__(self, login, password, name=None):
        self.login = login
        self.password = password
        self.name = name


admin = PkmUsers('admin', 'admin', name='Администратор Не заполнено')
invalid_pass_user = PkmUsers('admin', 'asdf')
invalid_login_user = PkmUsers('asdf', 'admin')
invalid_user = PkmUsers('asdf', 'asdf')
eu_user = PkmUsers('eu_user5', 'eu_user5', name='Иванов5к Андрей5к')
