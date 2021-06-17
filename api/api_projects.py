from core import BaseApi
from variables import PkmVars as Vars


class ApiProjects(BaseApi):
    def projects_names_generator(self, term=''):
        payload = {'term': term, 'limit': 0}
        projects = self.post(f'{Vars.PKM_API_URL}projects/get-list', self.token, payload).get('data')
        for project in projects:
            yield project.get('name')

    def get_last_k6_project_name(self):
        k6_projects = [name for name in self.projects_names_generator(term=Vars.DEFAULT_PROJECT_NAME)]
        k6_projects.sort(reverse=True)
        project_name = k6_projects[0]
        return project_name

    def create_user_access(self, user_uuid, project_uuid):
        payload = {
            'canEdit': True,
            'canEditUser': True,
            'canRead': True,
            'canReadUser': True,
            'referenceUuid': project_uuid,
            'userUuid': user_uuid
        }
        self.post(f'{Vars.PKM_API_URL}project-access/create', self.token, payload)

    def check_project_access(self, users_logins: list, project_uuid: str):
        users_uuids = [self.api_get_user_by_login(login)['uuid'] for login in users_logins]
        authorized_users = self.post(f'{Vars.PKM_API_URL}project-access/get', self.token, {'referenceUuids': [project_uuid]}).get('users')
        authorized_users_uuids = [user_uuid for user_uuid in authorized_users]
        for user_uuid in users_uuids:
            if user_uuid not in authorized_users_uuids:
                self.create_user_access(user_uuid, project_uuid)

    def create_project(self, name: str) -> dict:
        data = self.post(f'{Vars.PKM_API_URL}projects/create-node', self.token, {'name': name, 'type': 'project'})
        return data

    def check_project(self, project_name: str) -> str:
        for name in self.projects_names_generator(term=project_name):
            if name == project_name:
                uuid = self.get_project_uuid_by_name(name)
                assert uuid, 'Не удалось получить uuid проекта'
                return uuid
        uuid = self.create_project(project_name).get('referenceUuid')
        assert uuid, 'Не удалось получить uuid проекта'
        return uuid

