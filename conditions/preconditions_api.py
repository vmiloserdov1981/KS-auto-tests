from api.api import ApiClasses
from api.api import ApiEu
from variables import PkmVars as Vars
import allure
import users


class ClassesPreconditions(ApiClasses):

    def get_last_tree_node(self):
        '''
        Используется в идеальных случаях!
        В сломанном дереве не гарантируется правильная работа
        '''
        api_nodes_list = self.api_get_nodes()
        root_nodes = []
        for node in api_nodes_list.get('data'):
            if node.get('parentUuid') is None:
                root_nodes.append(node)
        nodes_prev_uuids = [i.get('previousUuid') for i in root_nodes]
        for root_node in root_nodes:
            if root_node.get('uuid') not in nodes_prev_uuids:
                return root_node

    def create_node(self, node_type, name, last=False, check=False, parent=None):
        if last:
            prev_uuid = self.get_last_tree_node().get('uuid')
        else:
            prev_uuid = None
        payload = {
            "parentUuid": parent,
            "previousUuid": prev_uuid,
            "relatedSourceUuid": None,
            "relatedDestinationUuid": None,
            "type": node_type,
            "name": name
        }
        url = f'{Vars.PKM_API_URL}/classes/create-node'
        resp = self.post(url, self.token, payload)
        resp_uuid = resp.get('nodeUuid')
        assert resp_uuid is not None, 'Невозможно получить uuid созданной ноды'
        if check:
            correct = False
            nodes = self.api_get_nodes().get('data')
            for node in nodes:
                if node.get('uuid') == resp_uuid:
                    assert node.get('name') == name, 'Созданная нода имеет неправильное имя'
                    correct = True
                    break
            assert correct, 'Созданной ноды нет в списке нод'
        return resp_uuid

    def create_test_data(self):
        with allure.step('Создать тестовые данные через api'):
            # class_1 тест создания показателей
            # class_2 тест удаления показателей
            # class_3 тест удаления класса в корне
            # class_4 тест переименования класса
            # class_5 тест переименования показателя через страницу показателя
            # class_6 тест переименования показателя через страницу класса
            test_data = {
                'folder': {
                },
                'class_1': {
                },
                'class_2': {
                    'indicators': []
                },
                'class_3': {
                },
                'class_4': {
                },
                'class_5': {
                    'indicators': []
                },
                'class_6': {
                    'indicators': []
                }
            }

            test_data['folder']['name'] = self.create_unique_folder_name(Vars.PKM_BASE_FOLDER_NAME)
            test_data['folder']['node_uuid'] = self.create_node('folder',
                                                                test_data.get('folder').get(
                                                                    'name'))

            test_data['class_1']['name'] = self.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
            test_data['class_1']['node_uuid'] = self.create_node('class',
                                                                 test_data.get('class_1').get(
                                                                     'name'),
                                                                 parent=test_data.get(
                                                                     'folder').get(
                                                                     'node_uuid'))

            test_data['class_2']['name'] = self.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
            test_data['class_2']['node_uuid'] = self.create_node('class',
                                                                 test_data.get('class_2').get(
                                                                     'name'),
                                                                 parent=test_data.get(
                                                                     'folder').get(
                                                                     'node_uuid'))
            test_data['class_2']['class_uuid'] = self.api_get_class_id_by_name(test_data['class_2']['name'])

            class_2_uuid = test_data.get('class_2').get('class_uuid')
            class_2_node_uuid = test_data.get('class_2').get('node_uuid')
            # создание показателей класса:
            test_data['class_2']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_number", 'number', class_2_uuid,
                                               None, class_2_node_uuid))
            test_data['class_2']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_date", 'datetime', class_2_uuid,
                                               test_data.get('class_2').get('indicators')[-1].get('node_uuid'), class_2_node_uuid))
            test_data['class_2']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_boolean", 'boolean', class_2_uuid,
                                               test_data.get('class_2').get('indicators')[-1].get('node_uuid'), class_2_node_uuid))
            test_data['class_2']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_string", 'string', class_2_uuid,
                                               test_data.get('class_2').get('indicators')[-1].get('node_uuid'), class_2_node_uuid))

            test_data['class_3']['name'] = self.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
            test_data['class_3']['node_uuid'] = self.create_node('class',
                                                                 test_data.get('class_3').get(
                                                                     'name'), last=True)

            test_data['class_4']['name'] = self.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
            test_data['class_4']['node_uuid'] = self.create_node('class',
                                                                 test_data.get('class_4').get(
                                                                     'name'),
                                                                 parent=test_data.get(
                                                                     'folder').get(
                                                                     'node_uuid'))
            test_data['class_4']['class_uuid'] = self.api_get_class_id_by_name(test_data['class_4']['name'])

            test_data['class_5']['name'] = self.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
            test_data['class_5']['node_uuid'] = self.create_node('class',
                                                                 test_data.get('class_5').get(
                                                                     'name'),
                                                                 parent=test_data.get(
                                                                     'folder').get(
                                                                     'node_uuid'))
            test_data['class_5']['class_uuid'] = self.api_get_class_id_by_name(test_data['class_5']['name'])

            class_5_uuid = test_data.get('class_5').get('class_uuid')
            class_5_node_uuid = test_data.get('class_5').get('node_uuid')
            # создание показателей класса:
            test_data['class_5']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_number", 'number', class_5_uuid,
                                               None, class_5_node_uuid))
            test_data['class_5']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_date", 'string', class_5_uuid,
                                               test_data.get('class_5').get('indicators')[-1].get('node_uuid'),
                                               class_5_node_uuid))

            test_data['class_6']['name'] = self.create_unique_class_name(Vars.PKM_BASE_CLASS_NAME)
            test_data['class_6']['node_uuid'] = self.create_node('class',
                                                                 test_data.get('class_6').get(
                                                                     'name'),
                                                                 parent=test_data.get(
                                                                     'folder').get(
                                                                     'node_uuid'))
            test_data['class_6']['class_uuid'] = self.api_get_class_id_by_name(test_data['class_6']['name'])

            class_6_uuid = test_data.get('class_6').get('class_uuid')
            class_6_node_uuid = test_data.get('class_6').get('node_uuid')
            # создание показателей класса:
            test_data['class_6']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_number", 'number', class_6_uuid,
                                               None, class_6_node_uuid))
            test_data['class_6']['indicators'].append(
                self.api_create_indicator_node(f"{Vars.PKM_BASE_INDICATOR_NAME}_date", 'string', class_6_uuid,
                                               test_data.get('class_6').get('indicators')[-1].get('node_uuid'),
                                               class_6_node_uuid))

            return test_data


class EuPreconditions(ApiEu):
    pass