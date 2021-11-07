from core import BaseApi
from variables import PkmVars as Vars


class ApiClasses(BaseApi):
    def get_tree_nodes(self, tree=None):
        nodes = {}
        if not tree:
            tree = self.api_get_classes_tree()
        for node in tree:
            self.add_in_group(node.get('name'), nodes, node.get('type'))
        return nodes

    def get_node_uuid(self, node_name, node_type):
        nodes = self.api_get_classes_tree()
        for node in nodes:
            if node.get('name') == node_name and node.get('type') == node_type:
                return node.get('uuid')
        return

    def is_node_exists(self, node_name, node_type, parent_folder_name=None):
        parent_uuid = None
        if parent_folder_name:
            parent_uuid = self.get_node_uuid(parent_folder_name, 'folder')
        classes_nodes = self.api_get_classes_list(term_value=node_name)
        if parent_uuid:
            for node in classes_nodes:
                if node.get('name') == node_name:
                    return True
                else:
                    continue
        else:
            for node in classes_nodes:
                if node.get('name') == node_name and node.get('type') == node_type:
                    return True
        return False

    def api_get_classes_tree(self):
        resp = self.post('{}classes/get-tree'.format(Vars.PKM_API_URL), self.token, {})
        classes = resp.get('data') or []
        return classes

    def api_get_classes_list(self, term_value):
        payload = {'term': term_value} if term_value else {}
        resp = self.post('{}classes/get-list'.format(Vars.PKM_API_URL), self.token, payload)
        classes = resp.get('data') or []
        return classes

    def create_unique_class_name(self, basename, nodes=None):
        if not nodes:
            nodes = self.get_tree_nodes()
        classes_list = nodes.get('class') or []
        count = 0
        newname = basename
        while newname in classes_list:
            count += 1
            newname = f"{basename}_{count}"
        return newname

    def create_unique_folder_name(self, basename, nodes=None):
        if not nodes:
            nodes = self.get_tree_nodes()
        folders_list = nodes.get('folder') or []
        count = 0
        newname = basename
        while newname in folders_list:
            count += 1
            newname = f"{basename}_{count}"
        return newname

    def get_classes_names(self):
        names = self.get_tree_nodes().get('class')
        return names

    def create_folder(self, folder_name, parent_uuid=None):
        payload = {
            'name': folder_name,
            'type': 'folder'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}classes/create-node', self.token, payload)
        node_uuid = resp.get('nodeUuid')
        return node_uuid

    def check_test_folder(self, folder_name: str) -> str:
        classes_tree = self.api_get_classes_tree()
        nodes = self.get_tree_nodes(tree=classes_tree)
        folders = nodes.get('folder')
        if folders:
            test_folder_count = folders.count(folder_name)
        else:
            test_folder_count = 0
        if test_folder_count == 0:
            uuid = self.create_folder(folder_name)
            return uuid
        elif test_folder_count == 1:
            for node in classes_tree:
                if node.get('type') == 'folder' and node.get('name') == folder_name and node.get('parentUuid') is None:
                    return node.get('uuid')
            raise AssertionError(f'Тестовая папка {folder_name} не в корне дерева')
        elif test_folder_count > 1:
            raise AssertionError('Количество тестовых папок > 1')

    def create_class_node(self, class_name, parent_uuid=None, create_unique_name=False):
        if create_unique_name:
            class_name = self.create_unique_class_name(class_name)

        payload = {
            'name': class_name,
            'type': 'class',
            'parentUuid': None
        }

        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}classes/create-node', self.token, payload)
        resp['name'] = class_name
        return resp

    def rename_class_node(self, class_node_uuid, class_name):
        payload = {
            'name': class_name,
            'nodeUuid': class_node_uuid
        }
        resp = self.post(f'{Vars.PKM_API_URL}classes/update-node', self.token, payload)
        return resp

    def get_class_data(self, class_uuid):
        payload = {
            'uuids': [class_uuid],
            'withRelations': True
        }
        resp = self.post(f'{Vars.PKM_API_URL}classes/get-by-ids', self.token, payload)
        return resp

    def get_class_name(self, class_uuid):
        class_data = self.get_class_data(class_uuid)
        name = class_data.get('data').get(class_uuid).get('name')
        return name

    def get_node_by_reference_uuid(self, reference_uuid):
        nodes = self.api_get_classes_tree()
        for node in nodes:
            if node.get('referenceUuid') == reference_uuid:
                return node
        return {}

    def create_classes_relation_node(self, relation_name, parent_node_uuid, source_class_uuid, destination_class_uuid):
        payload = {
            'name': relation_name,
            'parentUuid': parent_node_uuid,
            'relatedDestinationUuid': destination_class_uuid,
            'relatedSourceUuid': source_class_uuid,
            'type': 'class'
        }
        resp = self.post(f'{Vars.PKM_API_URL}classes/create-node', self.token, payload)
        return resp

    def create_indicator_node(self, name, class_uuid, parent_node_uuid, indicator_type, data_format=None):
        payload = {
            'classUuid': class_uuid,
            'dataType': indicator_type,
            'name': name,
            'parentUuid': parent_node_uuid,
            'type': "indicator"
        }
        if format:
            payload['dataFormat'] = data_format

        resp = self.post(f'{Vars.PKM_API_URL}classes/create-class-node', self.token, payload)
        assert not resp.get('error'), f'Ошибка при создании показателя: \n {resp}'
        return resp

    def delete_class_node(self, uuid: str, force=None):
        payload = {'uuid': uuid}
        if force:
            payload['force'] = force
        resp = self.post(f'{Vars.PKM_API_URL}classes/delete-node', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении ноды класса \n {resp}'

    def delete_formula(self, uuid: str):
        payload = {'uuid': uuid}
        resp = self.post(f'{Vars.PKM_API_URL}formulas/delete', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении формулы \n {resp}'

    def create_simple_formula(self, formula_data: dict):
        """
        formula_data = {
            'class_uuid': '01eb8565-43a6-7dbd-a10a-00b15c0c4000',
            'indicator_uuid': '01eb8588-44cf-00cb-a10a-00b15c0c4000',
            'formula_name': 'test_formula',
            'calc_indicator_1_uuid': '01eb8588-44cf-00cb-a10a-00b15c0c4000',
            'calc_indicator_2_uuid': '01eb8588-44cf-00cb-a10a-00b15c0c4000',
            'modifier_type': '-'
        }
        """

        payload = {
            'classUuid': formula_data.get('class_uuid'),
            'description': '',
            'indicatorUuid': formula_data.get('indicator_uuid'),
            'name': formula_data.get('formula_name'),
            'elements': [
                {'elementNumber': 1, 'indicatorUuid': formula_data.get('calc_indicator_1_uuid')},
                {'elementNumber': 3, 'indicatorUuid': formula_data.get('calc_indicator_2_uuid')}
            ],
            'resultElement': {
                'consolidations': None,
                'dimensionsElements': {},
                'elementNumber': 0,
                'forceMatchEqualElements': True,
                'includeNewMeasurementsElements': 'ignore',
                'indicatorUuid': formula_data.get('indicator_uuid'),
                'measurementsAreSet': True,
                'omitNonMatchingElements': False,
                'parentPlaceholderId': None,
                'relations': None,
                'result': True,
                'timePeriodsLag': 0
            },
            'tokens': [
                {'value': "1", 'kind': "VARIABLE"},
                {'value': formula_data.get('modifier_type'), 'kind': "MODIFIER"},
                {'value': "3", 'kind': "VARIABLE"}
            ]
        }
        resp = self.post(f'{Vars.PKM_API_URL}formulas/create', self.token, payload)
        assert not resp.get('error'), f'Ошибка при создании формулы: \n {resp}'
        result = {'uuid': resp.get('uuid'), 'name': formula_data.get('formula_name')}
        return result
