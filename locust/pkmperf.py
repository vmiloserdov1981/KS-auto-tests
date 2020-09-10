from locust import HttpUser, TaskSet, between
import json
from random import randint


class UserOne(TaskSet):
    def __init__(self, parent):
        super(UserOne, self).__init__(parent)
        self.token = None
        self.headers = None

    def on_start(self):
        self.token = self.get_token()
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def get_token(self, retry=False):
        resp = self.client.post("/auth/login", json.dumps({"login": "admin", "password": "admin"}))
        response_data = json.loads(resp.content)
        if retry:
            while response_data.get('token') is None:
                resp = self.client.post("/auth/login", json.dumps({"login": "admin", "password": "admin"}))
                response_data = json.loads(resp.content)
            return response_data.get('token')
        else:
            return response_data.get('token')

    def get_random_indicators(self):
        resp = self.client.post("/classes/get-list", json.dumps({}), headers=self.headers)
        resp_data = json.loads(resp.content)
        list_classes = resp_data.get('data')
        class_index = randint(0, len(list_classes)-1)
        target_class_uuid = list_classes[class_index].get('uuid')
        self.client.post("/indicators/get", json.dumps({"classUuids": [target_class_uuid]}), headers=self.headers)

    def get_random_class(self):
        resp = self.client.post("/classes/get-list", json.dumps({}), headers=self.headers)
        resp_data = json.loads(resp.content)
        list_classes = resp_data.get('data')
        class_index = randint(0, len(list_classes)-1)
        target_class_uuid = list_classes[class_index].get('uuid')
        self.client.post("/classes/get-by-ids", json.dumps({"uuids": [target_class_uuid], 'withRelations': True}), headers=self.headers)

    def get_models_tree(self):
        self.client.post("/models/get-tree", json.dumps({}), headers=self.headers)

    def get_classes_tree(self):
        self.client.post("/classes/get-tree", json.dumps({}), headers=self.headers)

    tasks = {
        get_random_class: 2,
        get_random_indicators: 2,
        get_classes_tree: 2,
        get_models_tree: 4
    }


class UserTwo(TaskSet):
    def __init__(self, parent):
        super(UserTwo, self).__init__(parent)
        self.token = None
        self.headers = None
        self.user_data = None

    def on_start(self):
        self.token = self.get_token()
        self.headers = {'Authorization': 'Bearer ' + self.token}
        self.user_data = self.get_user_data()

    def get_token(self, retry=False):
        resp = self.client.post("/auth/login", json.dumps({"login": "admin", "password": "admin"}))
        response_data = json.loads(resp.content)
        if retry:
            while response_data.get('token') is None:
                resp = self.client.post("/auth/login", json.dumps({"login": "admin", "password": "admin"}))
                response_data = json.loads(resp.content)
            return response_data.get('token')
        else:
            return response_data.get('token')

    def get_user_data(self):
        resp = self.client.post("/users/get-user-by-login", json.dumps({'login': 'system'}), headers=self.headers)
        return json.loads(resp.content)

    def get_gantt_uuid(self):
        return self.user_data.get('user').get('settings').get('ui').get('ganttUuid')

    def get_class_uuid(self):
        return self.user_data.get('user').get('settings').get('planSettings').get('classPersonalUuid')

    def get_gantt(self):
        self.client.post("/gantts/get-by-id", json.dumps({'uuid': self.get_gantt_uuid()}), headers=self.headers)

    def get_objects(self):
        self.client.post("/objects/get", json.dumps({'classUuid': self.get_class_uuid()}), headers=self.headers)

    tasks = {
        get_gantt: 4,
        get_objects: 2
    }


class WebsiteUserOne(HttpUser):
    tasks = {
        UserOne: 1
    }
    weight = 15
    # host = 'localhost'
    wait_time = between(3, 5)


class WebsiteUserTwo(HttpUser):
    tasks = {
        UserTwo: 1
    }
    weight = 5
    # host = 'localhost'
    wait_time = between(5, 10)

# locust -f locust/pkmperf.py --host=http://pkm.andersenlab.com/api
