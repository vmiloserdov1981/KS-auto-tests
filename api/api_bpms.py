from core import BaseApi
from core import BasePage
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

    def get_bpms_by_uuid(self, uuid: str):
        payload = {'uuids': [uuid]}
        resp = self.post(f'{Vars.PKM_API_URL}processes/get-by-ids', self.token, payload)
        bpms_data = resp['data'][uuid]
        return bpms_data

    def get_bpms_diagram_elements(self, bpms_uuid: str):
        bpms_data = self.get_bpms_by_uuid(bpms_uuid)
        diagram_uuid = bpms_data['diagramUuid']
        diagram_entities = self.post(f'{Vars.PKM_API_URL}processes/get-elements-by-diagram-uuid', self.token, {'uuid': diagram_uuid})
        uuids_names = {}
        result = {}
        for entity_type in diagram_entities:
            entities = diagram_entities[entity_type]
            for i in entities:
                uuids_names[i['uuid']] = i['name']

        for entity_type in diagram_entities:
            entities = diagram_entities[entity_type]
            result[entity_type] = []
            if entity_type == 'gates':
                for i in entities:
                    figure = {
                        'name': i['name'],
                        'next_elements': [],
                    }
                    for next_element in i['nextElements']:
                        figure['next_elements'].append(
                            {
                                'next_element_type': next_element['nextElementType'],
                                'next_element_name': uuids_names[next_element['nextElementUuid']]
                            }
                        )
                    result[entity_type].append(figure)
            else:
                for i in entities:
                    figure = {
                        'name': i['name'],
                        'next_element_type': i.get('nextElementType')
                    }
                    if i.get('nextElementUuid'):
                        figure['next_element_name'] = uuids_names[i.get('nextElementUuid')]
                    else:
                        figure['next_element_name'] = None
                    result[entity_type].append(figure)

        return result

    def get_event_by_bpms_uuid(self, bpms_uuid, event_name):
        events_list = self.post(f'{Vars.PKM_API_URL}process-events/get-list', self.token, {"processUuid": bpms_uuid}).get('data') or []
        for event in events_list:
            if event.get('name') == event_name:
                return event

    def get_task_by_bpms_uuid(self, bpms_uuid, task_name):
        tasks_list = self.post(f'{Vars.PKM_API_URL}tasks/get-list', self.token, {"processUuid": bpms_uuid}).get('data') or []
        for task in tasks_list:
            if task.get('name') == task_name:
                return task

    @staticmethod
    def compare_bpms_diagram_elements(entities_1, entities_2):
        for i in entities_1:
            BasePage.compare_dicts_lists(entities_1[i], entities_2[i])
