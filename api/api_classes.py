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
        classes_nodes = self.api_get_classes_tree()
        if parent_uuid:
            for node in classes_nodes:
                if node.get('name') == node_name and node.get('type') == node_type and node.get('parentUuid') == parent_uuid:
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
        classes = resp.get('data')
        return classes

    def create_unique_class_name(self, basename):
        classes_list = self.get_tree_nodes().get('class')
        count = 0
        newname = basename
        while newname in classes_list:
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

    def create_class_node(self, class_name, parent_uuid=None):
        payload = {
            'name': class_name,
            'type': 'class'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}classes/create-node', self.token, payload)
        return resp

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

    def create_indicator_node(self, name, class_uuid, parent_node_uuid, indicator_type):
        payload = {
            'classUuid': class_uuid,
            'dataType': indicator_type,
            'name': name,
            'parentUuid': parent_node_uuid,
            'type': "indicator"
        }
        resp = self.post(f'{Vars.PKM_API_URL}classes/create-class-node', self.token, payload)
        return resp

    def delete_class_node(self, uuid: str):
        payload = {'uuid': uuid}
        resp = self.post(f'{Vars.PKM_API_URL}classes/delete-node', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении ноды класса \n {resp}'
