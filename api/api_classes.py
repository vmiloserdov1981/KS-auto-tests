from core import BaseApi
from variables import PkmVars as Vars


class ApiClasses(BaseApi):
    def get_tree_nodes(self):
        nodes = {}
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
