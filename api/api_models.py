from core import BaseApi
from variables import PkmVars as Vars


class ApiModels(BaseApi):

    def api_get_models_tree(self):
        resp = self.post('{}models/get-tree'.format(Vars.PKM_API_URL), self.token, {})
        return resp.get('data')

    def get_tree_nodes(self, tree=None):
        nodes = {}
        if not tree:
            tree = self.api_get_models_tree()
        for node in tree:
            self.add_in_group(node.get('name'), nodes, node.get('type'))
        return nodes

    def create_folder(self, folder_name, parent_uuid=None):
        payload = {
            'name': folder_name,
            'type': 'folder'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}models/create-node', self.token, payload)
        node_uuid = resp.get('nodeUuid')
        return node_uuid


    def check_test_folder(self, folder_name: str) -> str:
        models_tree = self.api_get_models_tree()
        nodes = self.get_tree_nodes(tree=models_tree)
        test_folder_count = nodes.get('folder').count(folder_name)
        if test_folder_count == 0:
            uuid = self.create_folder(folder_name)
            return uuid
        elif test_folder_count == 1:
            for node in models_tree:
                if node.get('type') == 'folder' and node.get('name') == folder_name and node.get('parentUuid') is None:
                    return node.get('uuid')
            raise AssertionError(f'Тестовая папка {folder_name} не в корне дерева')
        elif test_folder_count > 1:
            raise AssertionError('Количество тестовых папок > 1')

        

    def create_unique_model_name(self, basename):
        models_list = self.get_tree_nodes().get('model')
        count = 0
        new_name = basename
        while new_name in models_list:
            count += 1
            new_name = f"{basename}_{count}"
        return new_name

    def get_models_names(self):
        names = self.get_tree_nodes().get('model')
        return names

    def delete_dataset(self, uuid):
        payload = {'uuid': uuid}
        resp = self.post(f'{Vars.PKM_API_URL}datasets/delete', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении наборов данных'

    def delete_model_node(self, uuid):
        payload = {'uuid': uuid}
        resp = self.post(f'{Vars.PKM_API_URL}models/delete-node', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении ноды модели'

    def create_model_node(self, model_name, parent_uuid=None):
        payload = {
            'name': model_name,
            'type': 'model'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}models/create-node', self.token, payload)
        return resp

    def get_datasets_by_model(self, model_uuid):
        payload = {'modelUuid': model_uuid}
        resp = self.post(f'{Vars.PKM_API_URL}datasets/get-by-model-id', self.token, payload)
        data = resp.get('data')
        return data

    def get_datasets_names(self, model_uuid, group_value=None, reverse=None):
        datasets = self.get_datasets_by_model(model_uuid)
        result = []

        if group_value and reverse is not None:
            def sort_function(dataset_data):
                return dataset_data.get(group_value)
            datasets.sort(key=sort_function, reverse=reverse)

        for dataset in datasets:
            result.append({'name': dataset.get('name'), 'is_default': dataset.get('default')})

        return result

    def get_model_data(self, model_uuid: str):
        resp = self.post(f'{Vars.PKM_API_URL}models/get', self.token, {'uuids': [model_uuid]})
        return resp.get('data')[0]

    def get_model_dictionaries(self, model_uuid):
        model_data = self.get_model_data(model_uuid)
        dimensions = model_data.get('dimensions')
        dictionaries_uuids = [i.get('dictionaryUuid') for i in dimensions]
        resp = self.post(f'{Vars.PKM_API_URL}dictionaries/get-by-ids', self.token, {'uuids': dictionaries_uuids})
        dictionaries = [resp.get('data').get(i) for i in resp.get('data')]
        return dictionaries

    def get_model_dictionaries_names(self, model_uuid, group_value=None, reverse=None):
        dictionaries = self.get_model_dictionaries(model_uuid)
        result = []

        if group_value and reverse is not None:
            def sort_function(dictionary_data):
                return dictionary_data.get(group_value)
            dictionaries.sort(key=sort_function, reverse=reverse)

        for dictionary in dictionaries:
            result.append(dictionary.get('name'))

        return result






