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


