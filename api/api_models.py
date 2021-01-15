from core import BaseApi
from variables import PkmVars as Vars


class ApiModels(BaseApi):

    """
    def api_get_nodes(self):
        return self.post('{}models/get-tree'.format(Vars.PKM_API_URL), self.token, {})

    def api_get_models_list(self):
        return self.post('{}models/get-list'.format(Vars.PKM_API_URL), self.token, {})

    def api_get_models_names(self):
        models_list = self.api_get_models_list()
        list = []
        for i in models_list.get('data'):
            list.append(i.get('name'))
        return list

    def api_get_models_folders_names(self):
        nodes_list = ApiModels.api_get_nodes(self)
        list = []
        for i in nodes_list.get('data'):
            if i.get('type') == 'folder':
                list.append(i.get('name'))
        return list

    def model_name_is_exists(self, name):
        models_names = self.api_get_models_names()
        return name in models_names

    def folder_name_is_exists(self, name):
        folders_names = self.api_get_models_folders_names()
        return name in folders_names

    def create_unique_model_name(self, basename):
        models_list = self.api_get_models_names()
        count = 0
        newname = basename
        while newname in models_list:
            count += 1
            newname = f"{basename}_{count}"
        return newname
    """

    def api_get_models_tree(self):
        resp = self.post('{}models/get-tree'.format(Vars.PKM_API_URL), self.token, {})
        return resp.get('data')

    def get_tree_nodes(self):
        nodes = {}
        tree = self.api_get_models_tree()
        for node in tree:
            self.add_in_group(node.get('name'), nodes, node.get('type'))
        return nodes

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
