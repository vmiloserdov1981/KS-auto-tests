from core import BaseApi
from variables import PkmVars as Vars


class ApiDictionaries(BaseApi):

    def api_get_dicts_tree(self):
        resp = self.post('{}dictionaries/get-tree'.format(Vars.PKM_API_URL), self.token, {})
        return resp.get('data') or []

    def create_folder(self, folder_name, parent_uuid=None):
        payload = {
            'name': folder_name,
            'type': 'folder'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}dictionaries/create-node', self.token, payload)
        node_uuid = resp.get('nodeUuid')
        return node_uuid

    def check_test_folder(self, folder_name: str) -> str:
        dictionaries_tree = self.api_get_dicts_tree()
        nodes = self.get_tree_nodes(tree=dictionaries_tree)
        folders = nodes.get('folder')
        if folders:
            test_folder_count = folders.count(folder_name)
        else:
            test_folder_count = 0
        if test_folder_count == 0:
            uuid = self.create_folder(folder_name)
            return uuid
        elif test_folder_count == 1:
            for node in dictionaries_tree:
                if node.get('type') == 'folder' and node.get('name') == folder_name and node.get('parentUuid') is None:
                    return node.get('uuid')
            raise AssertionError(f'Тестовая папка {folder_name} не в корне дерева')
        elif test_folder_count > 1:
            raise AssertionError('Количество тестовых папок > 1')

    def get_dicts_tree(self):
        tree = self.post(f'{Vars.PKM_API_URL}dictionaries/get-tree', self.token, {}).get('data')
        return tree

    def api_get_dicts_names(self, tree=None):
        if not tree:
            tree = self.get_dicts_tree()
        nodes = self.get_tree_nodes(tree=tree)
        dicts = nodes.get('dictionary')
        return dicts

    def create_unique_dict_name(self, basename, subname=None):
        dicts_list = self.api_get_dicts_names()
        count = 0
        newname = basename
        while newname in dicts_list:
            count += 1
            newname = f"{basename}_{count}"
        if subname:
            newname = self.create_unique_dict_name(f'{basename}_{count-1}_{subname}')
        return newname

    def get_tree_nodes(self, tree=None):
        nodes = {}
        if not tree:
            tree = self.get_dicts_tree()
        for node in tree:
            self.add_in_group(node.get('name'), nodes, node.get('type'))
        return nodes

    def get_node_uuid_by_name(self, node_name, tree: list = None):
        if not tree:
            tree = self.get_dicts_tree()
        for node in tree:
            if node.get('name') == node_name:
                return node.get('uuid')

    def get_node_children_names(self, parent_node_name, tree: list = None):
        children = []
        if not tree:
            tree = self.get_dicts_tree()
        parent_uuid = self.get_node_uuid_by_name(parent_node_name, tree)
        assert parent_uuid, 'Невозможно получить uuid родительской ноды'
        for node in tree:
            if node.get('parentUuid') == parent_uuid:
                children.append(node.get('name'))
        return children

    def create_folder_node(self, folder_name, parent_uuid=None):
        payload = {
            'name': folder_name,
            'description': '',
            'type': 'folder'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid

        resp = self.post(f'{Vars.PKM_API_URL}dictionaries/create-node', self.token, payload)
        return resp.get('nodeInserted')

    def create_dictionary_node(self, dictionary_name, parent_uuid=None):
        payload = {
            'name': dictionary_name,
            'description': '',
            'type': 'dictionary'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid

        resp = self.post(f'{Vars.PKM_API_URL}dictionaries/create-node', self.token, payload)
        return resp.get('nodeInserted')

    def delete_node(self, uuid):
        self.post(f'{Vars.PKM_API_URL}dictionaries/delete-node', self.token, payload={'uuid': uuid}, without_project=False)

    def check_test_dictionaries(self, dictionaries: list, parent_node_name: str = None):
        """
        dimensions = [
            {'name': 'Типы данных (автотест)', 'elements': ['Числовые', 'Текстовые']},
            {'name': 'Виды данных (автотест)', 'elements': ['Статистические', 'Эмпирические']}
        ]
        """
        tree = self.get_dicts_tree()
        dict_names = self.api_get_dicts_names(tree=tree)
        test_folder_uuid = self.get_node_uuid_by_name(parent_node_name, tree=tree) if parent_node_name else None

        if parent_node_name and not test_folder_uuid:
            test_folder_uuid = self.create_folder_node(parent_node_name).get('uuid')

        for dictionary in dictionaries:
            if dictionary.get('name') not in dict_names:
                self.create_dictionary_node(dictionary.get('name'), parent_uuid=test_folder_uuid)







