from api.api import ApiClasses, ApiEu
from variables import PkmVars as Vars


class ClassesPostconditions(ApiClasses):
    def delete_node(self, node_uuid, check=False):
        payload = {
            'uuid': node_uuid
        }
        url = f'{Vars.PKM_API_URL}/classes/delete-node'
        resp = self.post(url, self.token, payload)
        assert resp == {}, "/classes/delete-node. Нода класса не удалилась"
        if check:
            nodes = self.api_get_nodes().get('data')
            assert nodes is not None, 'Не удалось получить список нод'
            for node in nodes:
                assert node.get('uuid') != node_uuid, 'api возвращает ноду, после ее удаления'


class EuPostconditions(ApiEu):

    def test_data_cleaner(self, test_data):
        if test_data.get('to_delete'):
            if test_data.get('to_delete').get('datasets'):
                for dataset in test_data.get('to_delete').get('datasets'):
                    self.delete_dataset(dataset)

    def delete_dataset(self, dataset_uuid):
        payload = {'uuid': dataset_uuid}
        resp = self.post(f'{Vars.PKM_API_URL}datasets/delete', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении наборов данных'
