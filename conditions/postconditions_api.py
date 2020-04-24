from api.api import ApiClasses
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
