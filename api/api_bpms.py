from core import BaseApi
from variables import PkmVars as Vars


class ApiBpms(BaseApi):

    def api_get_bpms_tree(self):
        resp = self.post('{}processes/get-tree'.format(Vars.PKM_API_URL), self.token, {})
        return resp.get('data') or []

    def get_tree_nodes(self, tree=None):
        nodes = {}
        if not tree:
            tree = self.api_get_bpms_tree()
        for node in tree:
            self.add_in_group(node.get('name'), nodes, node.get('type'))
        return nodes

    def get_tree_entity_nodes(self, parent_node_uuid):
        nodes = {}
        payload = {
            'nodeNum': 0,
            'parentUuid': parent_node_uuid,
            'perPage': 100,
            'sortBy': 'createdAt',
            'sortDesc': False
        }
        resp = self.post(f'{Vars.PKM_API_URL}processes/tree-get-down', self.token, payload)
        child_nodes = resp.get('data') or []
        for node in child_nodes:
            self.add_in_group(node.get('name'), nodes, node.get('type'))
        return nodes

    def get_bpms_child_events(self, bpms_node_uuid):
        events_names = self.get_tree_entity_nodes(bpms_node_uuid).get('event')
        return events_names or []

    def get_bpms_child_tasks(self, bpms_node_uuid):
        events_names = self.get_tree_entity_nodes(bpms_node_uuid).get('task')
        return events_names or []

    def get_bpms_child_gates(self, bpms_node_uuid):
        events_names = self.get_tree_entity_nodes(bpms_node_uuid).get('gate')
        return events_names or []

    def create_folder(self, folder_name, parent_uuid=None):
        payload = {
            'name': folder_name,
            'type': 'folder'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}processes/create-node', self.token, payload)
        node_uuid = resp.get('nodeUuid')
        return node_uuid

    def check_test_folder(self, folder_name: str) -> str:
        bpms_tree = self.api_get_bpms_tree()
        nodes = self.get_tree_nodes(tree=bpms_tree)
        folders = nodes.get('folder')
        if folders:
            test_folder_count = folders.count(folder_name)
        else:
            test_folder_count = 0
        if test_folder_count == 0:
            uuid = self.create_folder(folder_name)
            return uuid
        elif test_folder_count == 1:
            for node in bpms_tree:
                if node.get('type') == 'folder' and node.get('name') == folder_name and node.get('parentUuid') is None:
                    return node.get('uuid')
            raise AssertionError(f'Тестовая папка {folder_name} не в корне дерева')
        elif test_folder_count > 1:
            raise AssertionError('Количество тестовых папок > 1')

    def create_unique_bpms_name(self, basename):
        bpms_list = self.get_tree_nodes().get('process') or []
        count = 0
        new_name = basename
        while new_name in bpms_list:
            count += 1
            new_name = f"{basename}_{count}"
        return new_name

    def get_bpms_names(self):
        names = self.get_tree_nodes().get('process')
        return names or []

    def get_bpms_entities_name(self):
        names = self.get_tree_nodes().get('event')
        return names or []

    def get_bpms_events_name(self):
        names = self.get_tree_nodes().get('event')
        return names or []

    def get_bpms_tasks_name(self):
        names = self.get_tree_nodes().get('task')
        return names or []

    def get_bpms_gates_name(self):
        names = self.get_tree_nodes().get('gate')
        return names or []

    def create_bpms(self, bpms_name, parent_uuid=None):
        payload = {
            'name': bpms_name,
            'type': 'process'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}processes/create-node', self.token, payload)
        return resp

    def delete_bpms_node(self, uuid: str, force=None):
        payload = {'uuid': uuid}
        if force:
            payload['force'] = force
        resp = self.post(f'{Vars.PKM_API_URL}processes/delete-node', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении ноды bpms \n {resp}'
