from core import BaseApi
from variables import PkmVars as Vars


class ApiDashboards(BaseApi):
    def api_get_dashboards_tree(self):
        resp = self.post('{}dashboards/get-tree'.format(Vars.PKM_API_URL), self.token, {})
        return resp.get('data') or []

    def get_tree_nodes(self, tree=None):
        nodes = {}
        if not tree:
            tree = self.api_get_dashboards_tree()
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
        resp = self.post(f'{Vars.PKM_API_URL}dashboards/create-node', self.token, payload)
        node_uuid = resp.get('nodeUuid')
        return node_uuid

    def check_test_folder(self, folder_name: str) -> str:
        dashboards_tree = self.api_get_dashboards_tree()
        nodes = self.get_tree_nodes(tree=dashboards_tree)
        folders = nodes.get('folder')
        if folders:
            test_folder_count = folders.count(folder_name)
        else:
            test_folder_count = 0
        if test_folder_count == 0:
            uuid = self.create_folder(folder_name)
            return uuid
        elif test_folder_count == 1:
            for node in dashboards_tree:
                if node.get('type') == 'folder' and node.get('name') == folder_name and node.get('parentUuid') is None:
                    return node.get('uuid')
            raise AssertionError(f'Тестовая папка {folder_name} не в корне дерева')
        elif test_folder_count > 1:
            raise AssertionError('Количество тестовых папок > 1')

    def create_unique_dashboard_name(self, basename, dashboard_nodes=None):
        if not dashboard_nodes:
            dashboard_nodes = self.get_tree_nodes().get('dashboard') or []
        count = 0
        newname = basename
        while newname in dashboard_nodes:
            count += 1
            newname = f"{basename}_{count}"
        return newname
