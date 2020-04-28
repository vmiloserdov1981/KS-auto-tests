from core import BaseApi
from variables import PkmVars as Vars
import users


class ApiClasses(BaseApi):
    def api_get_classes_list(self):
        return self.post('{}classes/get-list'.format(Vars.PKM_API_URL), self.token, {})

    def api_get_nodes(self):
        return self.post('{}classes/get-tree'.format(Vars.PKM_API_URL), self.token, {})

    def api_get_classes_names(self):
        cl_list = self.api_get_classes_list()
        list = []
        for i in cl_list.get('data'):
            list.append(i.get('name'))
        return list

    def api_get_classes_folders_names(self):
        nodes_list = self.api_get_nodes()
        list = []
        for i in nodes_list.get('data'):
            if i.get('type') == 'folder':
                list.append(i.get('name'))
        return list

    def class_name_is_exists(self, name):
        class_names = self.api_get_classes_names()
        return name in class_names

    def folder_name_is_exists(self, name):
        folders_names = self.api_get_classes_folders_names()
        return name in folders_names

    def create_unique_class_name(self, basename):
        classes_list = self.api_get_classes_names()
        count = 0
        newname = basename
        while newname in classes_list:
            count += 1
            newname = "{0}_{1}".format(basename, count)
        return newname

    def create_unique_folder_name(self, basename):
        folders_list = self.api_get_classes_folders_names()
        count = 0
        newname = basename
        while newname in folders_list:
            count += 1
            newname = "{0}_{1}".format(basename, count)
        return newname

    def api_get_class_name_by_id(self, uuid):
        uuids_list = [uuid]
        payload = {
            "uuids": uuids_list,
            "withRelations": False
        }
        url = '{}classes/get-by-ids'.format(Vars.PKM_API_URL)
        resp = self.post(url, self.driver.token, payload)
        name = resp.get('data').get(uuid).get('name')
        return name

    def api_get_class_id_by_name(self, class_name):
        payload = {
            "term": class_name
        }
        url = f'{Vars.PKM_API_URL}classes/get-list'
        resp = self.post(url, self.token, payload)
        class_list = resp.get('data')
        for class_data in class_list:
            if class_data.get('name') == class_name:
                return class_data.get('uuid')

    def api_check_class_absence(self, class_name):
        classes_names = self.api_get_classes_names()
        assert class_name not in classes_names, "Класс не удалился в api"

    def api_get_indicator_names_by_class(self, class_uuid):
        names = []
        class_uuids = [class_uuid]
        payload = {
            "classUuids": class_uuids
        }
        url = f'{Vars.PKM_API_URL}indicators/get'
        resp = self.post(url, self.driver.token, payload)
        ind_list = resp.get('data')
        for ind in ind_list:
            names.append(ind.get('name'))
        return names

    def api_get_indicators(self, class_uuid):
        class_uuids = [class_uuid]
        payload = {
            "classUuids": class_uuids
        }
        url = f'{Vars.PKM_API_URL}indicators/get'
        resp = self.post(url, self.token, payload)
        ind_list = resp.get('data')
        return ind_list

    def api_get_indicator(self, class_uuid, indicator_uuid):
        class_uuids = [class_uuid]
        payload = {
            "classUuids": class_uuids
        }
        url = f'{Vars.PKM_API_URL}indicators/get'
        resp = self.post(url, self.token, payload)
        ind_list = resp.get('data')
        for i in ind_list:
            if i.get('uuid') == indicator_uuid:
                return i

    def api_create_indicator_node(self, name, data_type, class_uuid, previous_node_uuid, parent_uuid):
        payload = {
            "name": name,
            "parentUuid": parent_uuid,
            "previousUuid": previous_node_uuid,
            "type": "indicator",
            "classUuid": class_uuid,
            "dataType": data_type,
        }
        url = f'{Vars.PKM_API_URL}classes/create-class-node'
        resp = self.post(url, self.token, payload)
        assert resp.get('error') is None, "Ошибка при создании показателя"
        node_uuid = resp.get('nodeUuid')
        reference_uuid = resp.get('referenceUuid')
        ind_data = {
            "name": name,
            "type": data_type,
            "indicator_uuid": reference_uuid,
            "node_uuid": node_uuid
        }
        return ind_data

    def api_check_indicator_absense(self, class_uuid, indicator_uuid):
        indicators = self.api_get_indicators(class_uuid)
        for i in indicators:
            assert i.get('uuid') != indicator_uuid, "Показатель присутствует в списке показателей класса"

    def api_get_indicator_type(self, class_uuid, indicator_uuid):
        indicators = self.api_get_indicators(class_uuid)
        for i in indicators:
            if i.get('uuid') == indicator_uuid:
                return i.get('dataType')

    def api_get_formulas_by_indicator(self, indicator_uuid):
        ind_uuids = [indicator_uuid]
        payload = {
            "uuids": ind_uuids
        }
        url = f'{Vars.PKM_API_URL}formulas/get-by-indicators'
        resp = self.post(url, self.token, payload)
        formulas_list = resp.get('data').get(indicator_uuid)
        return formulas_list

    def api_check_formula_exists(self, indicator_uuid, formula_name, formula_uuid=None):
        formulas_list = self.api_get_formulas_by_indicator(indicator_uuid)
        if formula_uuid:
            for formula in formulas_list:
                if formula.get('name') == formula_name and formula.get('uuid') == formula_uuid:
                    return True
        if not formula_uuid:
            for formula in formulas_list:
                if formula.get('name') == formula_name:
                    return True
        return False


class ApiModels(BaseApi):

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


class ApiEu(BaseApi):
    target_user = users.eu_user

    def api_check_eu_user(self, create=True):
        eu_user = None
        users_list = self.post(f'{Vars.PKM_API_URL}users/get-list', self.token, {}).get('data')
        for user in users_list:
            if user.get('login') == self.target_user.login and user.get('fullName') == self.target_user.name:
                eu_user = user
                break
        if eu_user:
            return eu_user
        else:
            if create:
                fname = self.target_user.name.split(' ')[1]
                lname = self.target_user.name.split(' ')[0]
                payload = {
                    "email": "autouser@test.com",
                    "login": self.target_user.login,
                    "password": self.target_user.password,
                    "firstname": fname,
                    "lastname": lname,
                    "settings": {}
                }
                request = self.post(f'{Vars.PKM_API_URL}users/create', self.token, payload)
                assert not request.get('error'), f'Ошибка при создании пользователя "{self.target_user.name}"'
                user_uuid = request.get('uuid')
                payload = {
                    "term": "",
                    "limit": 0
                }
                roles = self.post(f'{Vars.PKM_API_URL}access-control/get-roles', self.token, payload).get('data')
                admin_role_uuid = None
                for role in roles:
                    if role.get('name') == Vars.PKM_ADMIN_ROLE_NAME:
                        admin_role_uuid = role.get('uuid')
                assert admin_role_uuid is not None, f'В системе нет роли "{Vars.PKM_ADMIN_ROLE_NAME}"'
                payload = {
                    "roleUuid": admin_role_uuid,
                    "userUuid": user_uuid
                }
                request = self.post(f'{Vars.PKM_API_URL}access-control/set-role', self.token, payload)
                assert not request.get(
                    'error'), f'Ошибка при назначении роли "{Vars.PKM_ADMIN_ROLE_NAME}" пользователю "{self.target_user.name}"'
            else:
                return False






