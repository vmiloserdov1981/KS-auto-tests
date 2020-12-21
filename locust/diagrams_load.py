from locust import HttpUser
import json
from core import BaseApi
from locust import between


api_host = "http://ks1.im.systems/api/"
user_login = 'admin'
user_password = 'admin'
project_uuid = '01eb0f9f-b855-0377-9c33-00b15c0c4000'
diagram_uuid = '01eb1a8a-a0bb-b51b-6423-00b15c0c4000'


api = BaseApi(user_login, user_password, project_uuid, api_url=api_host)
check_data = {
    'diagram': api.post(f'{api_host}/diagrams/get-by-id', api.token, {'uuid': diagram_uuid}),
    'shapes': api.post(f'{api_host}/shapes/get', api.token, {'diagramUuid': diagram_uuid}),
    'sets': api.post(f'{api_host}/sets/get-list', api.token, {})
}


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
            if '"error"' in response.text:
                response.failure(f"Ошибка в полученных данных: \n {response.text}")
            elif (resp := json.loads(response.text)) != check_data['diagram']:
                response.failure(f"Полученные данные не совпадают с ожидаемыми: \n Ожидаемые: {check_data['diagram']} \n Фактические: {resp}")

        '''
        with self.client.post("/shapes/get", json.dumps({'diagramUuid': diagram_uuid}), headers=self.headers, catch_response=True) as response:
            if '"error"' in response.text:
                response.failure(f"Ошибка в полученных данных: \n {response.text}")
            elif (resp := json.loads(response.text)) != check_data['shapes']:
                response.failure(f"Полученные данные не совпадают с ожидаемыми: \n Ожидаемые: {check_data['shapes']} \n Фактические: {resp}")
        '''

        self.client.post("/shapes/get", json.dumps({'diagramUuid': diagram_uuid}), headers=self.headers)

        with self.client.post("/sets/get-list", json.dumps({}), headers=self.headers, catch_response=True) as response:
            if '"error"' in response.text:
                response.failure(f"Ошибка в полученных данных: \n {response.text}")
            elif (resp := json.loads(response.text)) != check_data['sets']:
                response.failure(f"Полученные данные не совпадают с ожидаемыми: \n Ожидаемые: {check_data['sets']} \n Фактические: {resp}")

    wait_time = between(1, 4)
    tasks = {
        check_diagram: 1,
        open_diagram: 0
    }
    weight = 1
    host = api_host

# locust -f locust/diagrams_load.py ------------> запускать в корне для стандартного запуска
# locust -f locust/diagrams_load.py --master ------------> запускать в корне для многопоточного запуска (хаб)
# locust -f locust/diagrams_load.py --worker --master-port=8089 ------------> запускать в корне для многопоточного запуска (нода)
