from locust import HttpUser
import json
from core import BaseApi
from locust import between
from locust import events


api_host = "http://pkm.andersenlab.com/api"
user_login = 'admin'
user_password = 'admin'
project_uuid = '01eb0e06-136f-b9d4-784e-00b15c0c4000'
diagram_uuid = '01eb299c-f8a4-f4bb-417e-00b15c0c4000'
check_data = {}


@events.test_start.add_listener
def on_test_start(**kwargs):
    global check_data
    api = BaseApi(user_login, user_password, project_uuid)
    check_data['diagram'] = api.post(f'{api_host}/diagrams/get-by-id', api.token, {'uuid': diagram_uuid})
    check_data['shapes'] = api.post(f'{api_host}/shapes/get', api.token, {'diagramUuid': diagram_uuid})
    check_data['sets'] = api.post(f'{api_host}/sets/get-list', api.token, {})


class WebsiteUser(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None
        self.headers = None

    def on_start(self):
        self.token = self.get_token(user_login, user_password)
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'x-project-uuid': project_uuid
        }

    def get_token(self, login, password, retry=False):
        resp = self.client.post("/auth/login", json.dumps({"login": login, "password": password}))
        response_data = json.loads(resp.content)
        if retry:
            while response_data.get('token') is None:
                resp = self.client.post("/auth/login", json.dumps({"login": login, "password": password}))
                response_data = json.loads(resp.content)
            return response_data.get('token')
        else:
            return response_data.get('token')

    def open_diagram(self):
        self.client.post("/diagrams/get-by-id", json.dumps({'uuid': diagram_uuid}), headers=self.headers)

        self.client.post("/shapes/get", json.dumps({'diagramUuid': diagram_uuid}), headers=self.headers)

        self.client.post("/sets/get-list", json.dumps({}), headers=self.headers)

    def check_diagram(self):
        with self.client.post("/diagrams/get-by-id", json.dumps({'uuid': diagram_uuid}), headers=self.headers, catch_response=True) as response:
            if 'error' in response.text:
                response.failure("Ошибка в полученных данных")
            elif json.loads(response.text) != check_data['diagram']:
                response.failure("Полученные данные не совпадают с ожидаемыми")

        '''
        with self.client.post("/shapes/get", json.dumps({'diagramUuid': diagram_uuid}), headers=self.headers, catch_response=True) as response:
            if 'error' in response.text:
                response.failure("Ошибка в полученных данных")
            elif json.loads(response.text) != check_data['shapes']:
                response.failure("Полученные данные не совпадают с ожидаемыми")
        '''

        self.client.post("/shapes/get", json.dumps({'diagramUuid': diagram_uuid}), headers=self.headers)

        with self.client.post("/sets/get-list", json.dumps({}), headers=self.headers, catch_response=True) as response:
            if 'error' in response.text:
                response.failure("Ошибка в полученных данных")
            elif json.loads(response.text) != check_data['sets']:
                response.failure("Полученные данные не совпадают с ожидаемыми")

    wait_time = between(3, 10)
    tasks = {
        check_diagram: 1
        # open_diagram: 1
    }
    weight = 1
    host = api_host

# locust -f locust/locustfile.py --host=http://pkm.andersenlab.com/api
