from core import BaseApi
from variables import PkmVars as Vars


class ApiDictionaries(BaseApi):

    def get_dicts_tree(self):
        tree = self.post(f'{Vars.PKM_API_URL}dictionaries/get-tree', self.token, {}).get('data')
        return tree

    def api_get_dicts_names(self):
        tree = self.get_tree_nodes()
        dicts = tree.get('dictionary')
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

    def get_tree_nodes(self):
        nodes = {}
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

    def delete_node(self, uuid):
        self.post(f'{Vars.PKM_API_URL}dictionaries/delete-node', self.token, payload={'uuid': uuid}, without_project=False)



