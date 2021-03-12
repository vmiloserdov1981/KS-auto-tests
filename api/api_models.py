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
        folders = nodes.get('folder')
        if folders:
            test_folder_count = folders.count(folder_name)
        else:
            test_folder_count = 0
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

    def create_dataset(self, dataset_name, model_uuid, is_default=False):
        payload = {'name': dataset_name,
                   'default': is_default,
                   'description': '',
                   'modelUuid': model_uuid
                   }

        resp = self.post(f'{Vars.PKM_API_URL}datasets/create', self.token, payload)
        assert not resp.get('error'), f'Ошибка при создании набора данных: \n {resp}'
        return resp

    def delete_dataset(self, uuid):
        payload = {'uuid': uuid}
        resp = self.post(f'{Vars.PKM_API_URL}datasets/delete', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении наборов данных'

    def delete_model_node(self, uuid):
        payload = {'uuid': uuid}
        resp = self.post(f'{Vars.PKM_API_URL}models/delete-node', self.token, payload)
        assert not resp.get('error'), f'Ошибка при удалении ноды модели'

    def create_model_node(self, model_name, parent_uuid=None, create_unique_name=False):
        if create_unique_name:
            model_name = self.create_unique_model_name(model_name)
        payload = {
            'name': model_name,
            'type': 'model'
        }
        if parent_uuid:
            payload['parentUuid'] = parent_uuid
        resp = self.post(f'{Vars.PKM_API_URL}models/create-node', self.token, payload)
        return resp

    def create_object_node(self, object_name, class_uuid, model_uuid, parent_uuid):
        payload = {
            'name': object_name,
            'type': 'object',
            'parentUuid': parent_uuid,
            'modelUuid': model_uuid,
            'classUuid': class_uuid,
        }
        resp = self.post(f'{Vars.PKM_API_URL}models/create-model-node', self.token, payload)
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

    def get_tag_uuid_by_name(self, tag_name):
        tags = self.post(f'{Vars.PKM_API_URL}models/find-tag', self.token, {'tag': tag_name}).get('data')
        for tag in tags:
            if tag.get('tag') == tag_name:
                return tag.get('uuid')

    def get_models_names_by_tag(self, tag_name):
        names = []
        tag_uuid = self.get_tag_uuid_by_name(tag_name)
        resp = self.post(f'{Vars.PKM_API_URL}models/get-by-tag', self.token, {'uuid': tag_uuid})
        for model in resp.get('data'):
            names.append(model.get('name'))
        return names

    def get_model_change_dates(self, model_uuid):
        model_data = self.get_model_data(model_uuid)
        api_created_at = model_data.get('createdAt')
        api_created_date = api_created_at.split('T')[0].split('-')
        api_created_date = api_created_date[::-1]
        api_created_time = api_created_at.split('T')[1].split('.')[0].split(':')[:2]
        api_created_date = f'{api_created_date[0]}.{api_created_date[1]}.{api_created_date[2]} {api_created_time[0]}:{api_created_time[1]}'

        api_updated_at = model_data.get('updatedAt')
        api_updated_date = api_created_at.split('T')[0].split('-')
        api_updated_date = api_updated_date[::-1]
        api_updated_time = api_updated_at.split('T')[1].split('.')[0].split(':')[:2]
        api_updated_date = f'{api_updated_date[0]}.{api_updated_date[1]}.{api_updated_date[2]} {api_updated_time[0]}:{api_updated_time[1]}'
        result = {
            'created_at': api_created_date,
            'updated_at': api_updated_date
        }
        return result

    def get_models_list(self, term=None):
        payload = {'term': term} if term else {}
        resp = self.post(f'{Vars.PKM_API_URL}models/get-list', self.token, payload)
        return resp.get('data')

    def get_model_uuid_by_name(self, model_name):
        models_list = self.get_models_list(term=model_name)
        for model in models_list:
            if model.get('name') == model_name:
                return model.get('uuid')
