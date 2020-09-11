from core import BaseApi
from variables import PkmVars as Vars
import time
import users
import copy


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
        resp = self.post(url, self.token, payload)
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
        resp = self.post(url, self.token, payload)
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

    def api_get_user(self, login, name):
        users_list = self.post(f'{Vars.PKM_API_URL}users/get-list', self.token, {}).get('data')
        for user in users_list:
            if user.get('login') == login and user.get('fullName') == name:
                return user

    def api_create_user(self, email, login, password, user_name, settings, ignore_error=False):
        fname = user_name.split(' ')[1]
        lname = user_name.split(' ')[0]
        payload = {
            "email": email,
            "login": login,
            "password": password,
            "firstname": fname,
            "lastname": lname,
            "settings": settings
        }
        request = self.post(f'{Vars.PKM_API_URL}users/create', self.token, payload)
        if not ignore_error:
            assert not request.get('error'), f'Ошибка при создании пользователя "{user_name}"'
            assert request.get('uuid'), f'Невозможно получить uuid пользователя "{user_name}"'
        return request.get('uuid')

    def api_set_admin_role(self, user_uuid):
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
        assert not request.get('error'), f'Ошибка при назначении роли "{Vars.PKM_ADMIN_ROLE_NAME}" пользователю'

    def api_get_plans(self, names_only=False):
        request = self.post(f'{Vars.PKM_API_URL}plans/get-list', self.token, {})
        plans = request.get('data')
        if names_only:
            names = []
            for plan in plans:
                plan_name = plan.get('name')
                names.append(plan_name)
            return names
        else:
            return plans

    def api_get_plan_by_uuid(self, plan_uuid):
        plans = self.api_get_plans()
        for plan in plans:
            if plan.get('uuid') == plan_uuid:
                return plan

    def api_get_k6_plans(self):
        k6_plans = []
        k6_comments = []
        plans = self.api_get_plans()
        for plan in plans:
            comment = plan.get('settings').get('plan').get('comment')
            if Vars.PKM_DEFAULT_K6_PLAN_COMMENT in comment:
                k6_plans.append(plan)
                k6_comments.append(comment)
        assert len(k6_plans) > 0, 'В системе нет планов K6'
        data = {
            'plans': k6_plans,
            'comments': k6_comments
        }
        return data

    def api_get_last_k6_plan(self):
        numbers = []
        plans = self.api_get_k6_plans()
        comments = plans.get('comments')
        for comment in comments:
            numbers.append(int(comment.split(Vars.PKM_DEFAULT_K6_PLAN_COMMENT)[1]))
        numbers.sort(reverse=True)
        last_number = str(numbers[0])
        comment = f'{Vars.PKM_DEFAULT_K6_PLAN_COMMENT}{last_number}'

        def f_func(x):
            if x.get('settings').get('plan').get('comment') == comment:
                return True
            else:
                return False

        plan = filter(f_func, plans.get('plans'))
        plan = list(plan)
        k6_plan = plan[0]
        k6_plan['plan_prefix'] = f'{last_number}u1'
        return k6_plan

    def api_get_datasets_by_plan(self, plan_uuid):
        payload = {"modelUuid": plan_uuid}
        request = self.post(f'{Vars.PKM_API_URL}datasets/get-by-model-id', self.token, payload)
        assert not request.get('error'), f'Ошибка при получении наборов данных'
        return request.get('data')

    def api_get_version_uuid(self, model_uuid, version_name):
        datasets = self.api_get_datasets_by_plan(model_uuid)
        for dataset in datasets:
            if dataset.get('name') == version_name:
                return dataset.get('uuid')

    def api_get_gantt(self, version_name, plan_uuid, login):
        version_uuid = self.api_get_version_uuid(plan_uuid, version_name)
        gantt_uuid = self.api_get_user_by_login(login).get('settings').get('ui').get('ganttUuid')
        payload = {
            "uuid": gantt_uuid,
            "modelUuid": plan_uuid,
            "datasetUuid": version_uuid
        }
        request = self.post(f'{Vars.PKM_API_URL}gantts/get-by-id', self.token, payload)
        assert not request.get('error'), f'Ошибка при получении Ганта'
        return request

    @staticmethod
    def get_plan_prefixes(gantt):
        prefixes = ('', '')
        gantt_classes = gantt.get('data').get('classes')
        if gantt_classes:
            for i in gantt_classes:
                if 'Мероприятие' in gantt_classes.get(i).get('name'):
                    class_name = gantt_classes.get(i).get('name')
                    if ' ' in class_name:
                        words = class_name.split(' ')
                        prefixes = (f'{words[0]} ', f' {words[2]}')
                        return prefixes
            return prefixes

    @staticmethod
    def api_get_dict_element_uuid(gantt, dict_name, dict_value):
        for dict_uuid in gantt.get('data').get('dictionaries'):
            if gantt.get('data').get('dictionaries').get(dict_uuid).get('name') == dict_name:
                for element in gantt.get('data').get('dictionaries').get(dict_uuid).get('elements'):
                    if element.get('name') == dict_value:
                        return element.get('uuid')

    def api_create_event(self, event_name, model_uuid, version_name, login, event_data):
        """
               Пример:
               event_data = {
                   'event_name': event_name,
                   'start_day': '10',
                   'duration': '5',
                   'event_type': 'Текущая',
                   'works_type': 'Бурение',
                   'plan': 'План отгрузок',
                   'ready': 'Готово к реализации',
                   'comment': 'Авто тест',
                   'responsible': 'Олег Петров',
                   'is_cross_platform': True,
                   'is_need_attention': True
               }
               """

        def get_custom_field_uuid(gantt_dict, field_name):
            custom_fields = gantt_dict.get('ganttDiagram').get('options')[0].get('customFields')
            for field in custom_fields:
                if custom_fields.get(field) == field_name:
                    return field

        dataset = self.api_get_version_uuid(model_uuid, version_name)
        gantt = self.api_get_gantt(version_name, model_uuid, login)
        start_uuid = gantt.get('ganttDiagram').get('options')[0].get('startUuid')
        duration_uuid = gantt.get('ganttDiagram').get('options')[0].get('durationUuid')
        end_uuid = gantt.get('ganttDiagram').get('options')[0].get('endUuid')
        event_type_uuid = get_custom_field_uuid(gantt, 'Тип работ')
        works_type_uuid = get_custom_field_uuid(gantt, 'Тип одновременных работ')
        plan_type_uuid = get_custom_field_uuid(gantt, 'Функциональный план')
        ready_type_uuid = get_custom_field_uuid(gantt, 'Готовность')
        comment_uuid = get_custom_field_uuid(gantt, 'Комментарий')
        responsible_uuid = get_custom_field_uuid(gantt, 'Ответственный')
        is_cross_platform_uuid = get_custom_field_uuid(gantt, 'Кросс-функцильальное')
        is_need_attention_uuid = get_custom_field_uuid(gantt, 'Требует повышенного внимания')
        utc = self.get_utc_date()
        start_day = event_data.get("start_day")
        duration = int(event_data.get("duration"))
        end_day = str(int(start_day) + int(duration))
        start_date = f'{utc[2]}-{utc[1]}-{start_day}T00:00:00.000Z'
        end_date = f'{utc[2]}-{utc[1]}-{end_day}T00:00:00.000Z'

        data = {
            start_uuid: [
                {
                    "value": {
                        "data": start_date,
                        "type": "datetime"
                    }
                }
            ],
            duration_uuid: [
                {
                    "value": {
                        "data": duration,
                        "type": "number"
                    }
                }
            ],
            end_uuid: [
                {
                    "value": {
                        "data": end_date,
                        "type": "datetime"
                    }
                }
            ],
            event_type_uuid: [
                {
                    "value": {
                        "data": self.api_get_dict_element_uuid(gantt, 'Типы работ', event_data.get('event_type')),
                        "type": "uuid"
                    }
                }
            ],
            works_type_uuid: [
                {
                    "value": {
                        "data": self.api_get_dict_element_uuid(gantt, 'Типы одновременных работ', event_data.get('works_type')),
                        "type": "uuid"
                    }
                }
            ],
            plan_type_uuid: [
                {
                    "value": {
                        "data": self.api_get_dict_element_uuid(gantt, 'Функциональные планы', event_data.get('plan')),
                        "type": "uuid"
                    }
                }
            ],
            ready_type_uuid: [
                {
                    "value": {
                        "data": self.api_get_dict_element_uuid(gantt, 'Типы готовности мероприятий', event_data.get('ready')),
                        "type": "uuid"
                    }
                }
            ],
            comment_uuid: [
                {
                    "value": {
                        "data": event_data.get('comment'),
                        "type": "string"
                    }
                }
            ],
            responsible_uuid: [
                {
                    "value": {
                        "data": event_data.get('responsible'),
                        "type": "string"
                    }
                }
            ],
            is_cross_platform_uuid: [
                {
                    "value": {
                        "data": event_data.get('is_cross_platform'),
                        "type": "boolean"
                    }
                }
            ],
            is_need_attention_uuid: [
                {
                    "value": {
                        "data": event_data.get('is_need_attention'),
                        "type": "boolean"
                    }
                }
            ]
        }
        payload = {
            "name": event_name,
            "classUuid": gantt.get('ganttDiagram').get('options')[0].get('classUuid'),
            "modelUuid": model_uuid,
            "datasetUuid": dataset,
            "data": data
        }
        request = self.post(f'{Vars.PKM_API_URL}gantts/create-object', self.token, payload)
        assert not request.get('error'), f'Ошибка при создании мероприятия'
        assert request.get('uuid') is not None, 'Невозможно получить uuid мероприятия'
        uuid = request.get('uuid')
        event_data = {
            'event_uuid': uuid,
            'event_data': {
                'event_name': event_name,
                'start_date': start_date.split('T')[0].split('-')[::-1],
                'end_date': end_date.split('T')[0].split('-')[::-1],
                'duration': str(duration),
                'event_type': event_data.get('event_type'),
                'works_type': event_data.get('works_type'),
                'plan': event_data.get('plan'),
                'ready': event_data.get('ready'),
                'comment': event_data.get('comment'),
                'responsible': event_data.get('responsible'),
                'is_cross_platform': event_data.get('is_cross_platform'),
                'is_need_attention': event_data.get('is_need_attention')
            }
        }
        return event_data

    def api_update_event(self, event_uuid, model_uuid, version_name, login, event_data):
        """
               Пример:
               event_data = {
                   'event_name': event_name
                   'start_day': '10',
                   'duration': '5',
                   'event_type': 'Текущая',
                   'works_type': 'Бурение',
                   'plan': 'План отгрузок',
                   'ready': 'Готово к реализации',
                   'comment': 'Авто тест',
                   'responsible': 'Олег Петров',
                   'is_cross_platform': True,
                   'is_need_attention': True
               }
               """

        def get_custom_field_uuid(gantt_dict, field_name):
            custom_fields = gantt_dict.get('ganttDiagram').get('options')[0].get('customFields')
            for field in custom_fields:
                if custom_fields.get(field) == field_name:
                    return field

        dataset = self.api_get_version_uuid(model_uuid, version_name)
        gantt = self.api_get_gantt(version_name, model_uuid, login)
        start_uuid = gantt.get('ganttDiagram').get('options')[0].get('startUuid')
        duration_uuid = gantt.get('ganttDiagram').get('options')[0].get('durationUuid')
        end_uuid = gantt.get('ganttDiagram').get('options')[0].get('endUuid')
        event_type_uuid = get_custom_field_uuid(gantt, 'Тип работ')
        works_type_uuid = get_custom_field_uuid(gantt, 'Тип одновременных работ')
        plan_type_uuid = get_custom_field_uuid(gantt, 'Функциональный план')
        ready_type_uuid = get_custom_field_uuid(gantt, 'Готовность')
        comment_uuid = get_custom_field_uuid(gantt, 'Комментарий')
        responsible_uuid = get_custom_field_uuid(gantt, 'Ответственный')
        is_cross_platform_uuid = get_custom_field_uuid(gantt, 'Кросс-функцильальное')
        is_need_attention_uuid = get_custom_field_uuid(gantt, 'Требует повышенного внимания')
        utc = self.get_utc_date()
        start_day = event_data.get("start_day")
        duration = int(event_data.get("duration"))
        end_day = str(int(start_day) + int(duration))
        start_date = f'{utc[2]}-{utc[1]}-{start_day}T00:00:00.000Z'
        end_date = f'{utc[2]}-{utc[1]}-{end_day}T00:00:00.000Z'

        data = [
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': start_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': start_date,
                    'type': 'datetime'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': duration_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': duration,
                    'type': 'number'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': end_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': end_date,
                    'type': 'datetime'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': event_type_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': self.api_get_dict_element_uuid(gantt, 'Типы работ', event_data.get('event_type')),
                    'type': 'uuid'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': works_type_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': self.api_get_dict_element_uuid(gantt, 'Типы одновременных работ', event_data.get('works_type')),
                    'type': 'uuid'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': plan_type_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': self.api_get_dict_element_uuid(gantt, 'Функциональные планы', event_data.get('plan')),
                    'type': 'uuid'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': ready_type_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': self.api_get_dict_element_uuid(gantt, 'Типы готовности мероприятий', event_data.get('ready')),
                    'type': 'uuid'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': comment_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': event_data.get('comment'),
                    'type': 'string'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': responsible_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': event_data.get('responsible'),
                    'type': 'string'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': is_cross_platform_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': event_data.get('is_cross_platform'),
                    'type': 'boolean'
                }
            },
            {
                'datasetUuid': dataset,
                'dimensionsElements': None,
                'indicatorUuid': is_need_attention_uuid,
                'modelUuid': model_uuid,
                'objectUuid': event_uuid,
                'uuid': None,
                'value': {
                    'data': event_data.get('is_need_attention'),
                    'type': 'boolean'
                }
            }
        ]
        payload = {
            "data": data
        }
        request = self.post(f'{Vars.PKM_API_URL}data/save', self.token, payload)
        assert not request.get('error'), f'Ошибка при редактировании мероприятия'
        event_data = {
            'event_uuid': event_uuid,
            'event_data': {
                'event_name': event_data.get('event_name'),
                'start_date': start_date.split('T')[0].split('-')[::-1],
                'end_date': end_date.split('T')[0].split('-')[::-1],
                'duration': str(duration),
                'event_type': event_data.get('event_type'),
                'works_type': event_data.get('works_type'),
                'plan': event_data.get('plan'),
                'ready': event_data.get('ready'),
                'comment': event_data.get('comment'),
                'responsible': event_data.get('responsible'),
                'is_cross_platform': event_data.get('is_cross_platform'),
                'is_need_attention': event_data.get('is_need_attention')
            }
        }
        return event_data

    @staticmethod
    def anti_doublespacing(string):
        if '  ' in string:
            string_list = string.split(' ')
            new_string_list = [elem for elem in string_list if elem != '']
            string = ' '.join(new_string_list)

        if string[0] == ' ':
            string = string[1:]

        if string[len(string) - 1] == ' ':
            string = string[:len(string) - 1]

        return string

    def api_get_event_names(self, version, plan_uuid, login, deleleted_only=False, get_deleted=True):
        if deleleted_only:
            return [self.anti_doublespacing(event) for event in self.api_event_names_generator(version, plan_uuid, login, deleleted_only=True)]
        else:
            if get_deleted:
                return [self.anti_doublespacing(event) for event in self.api_event_names_generator(version, plan_uuid, login, get_deleted=True)]
            else:
                return [self.anti_doublespacing(event) for event in self.api_event_names_generator(version, plan_uuid, login, get_deleted=False)]

    def api_get_events(self, version, plan_uuid, login, filter_set=None, names_only=True, anti_doublespacing=True, group_by=False):
        """
        filter_set = {
            "unfilled_events_filter": {
                'Только незаполненные мероприятия': False,
                'Отображать незаполненные мероприятия': True
            },
            "custom_fields_filter": {
                'Тип одновременных работ': [],
                'Функциональный план': [],
                'Готовность': [],
                'Тип работ': [],

            },
            "custom_relations_filter": {
                'Персонал': [],
                'Зона': [],
                'Влияние на показатели': [],
                'Риски': [],
                'События для ИМ': []
            }

        }
        """
        gantt = self.api_get_gantt(version, plan_uuid, login)
        values_dictionary = gantt.get('uuidValues')
        invalid_field = False
        invalid_relation = False
        if filter_set is None:
            filter_set = {}

        def none_converter(value):
            if value == '(пусто)':
                return None
            else:
                return value

        def get_custom_relation_names(gantt):
            names = []
            for relation in gantt.get('ganttDiagram').get('options')[0].get('customRelations'):
                name = relation['name']
                names.append(name)
            return names

        def get_custom_fields_names(gantt):
            names = []
            for field in gantt.get('ganttDiagram').get('options')[0].get('customFields'):
                name = gantt.get('ganttDiagram').get('options')[0].get('customFields')[field]
                if name:
                    names.append(name)
            return names

        def get_group_value(event, gantt, group_indicator):

            def custom_value_to_text(value):
                if value != 'Не указано':
                    nonlocal values_dictionary
                    return values_dictionary.get(value)
                else:
                    return 'Не указано'

            if group_indicator in get_custom_fields_names(gantt):
                value = self.api_get_custom_field_value(gantt, group_indicator, event) if group_indicator == 'Комментарий' else custom_value_to_text(self.api_get_custom_field_value(gantt, group_indicator, event))
                if not value:
                    value = 'Не указано'
            elif group_indicator in get_custom_relation_names(gantt):
                value = self.api_get_custom_relation_values(gantt, group_indicator, event)
                if value is None or value == []:
                    value = 'Не указано'
            else:
                raise AssertionError('Невозможно определить тип группируемого показателя (custom field или custom relation)')
            return value

        def add_in_group(item, dictionary, group_value):
            if type(group_value) is str:
                if group_value in dictionary.keys():
                    dictionary[group_value].append(item)
                else:
                    dictionary[group_value] = [item]
            elif type(group_value) is list:
                for i in group_value:
                    if i in dictionary.keys():
                        dictionary[i].append(item)
                    else:
                        dictionary[i] = [item]
            return dictionary

        def custom_value_to_uuid(value):
            if value:
                nonlocal values_dictionary
                for uuid in values_dictionary:
                    if values_dictionary.get(uuid) == value:
                        return uuid
                raise AssertionError(f'can`t find {value} value in uuids dictionary')

        if group_by:
            events = {}

        else:
            events = []

        if filter_set:
            filter_set = copy.deepcopy(filter_set)

        if filter_set.get('custom_fields_filter'):
            for custom_filter in filter_set.get('custom_fields_filter'):
                filter_set['custom_fields_filter'][custom_filter] = list(
                    map(none_converter, filter_set['custom_fields_filter'][custom_filter]))
                filter_set['custom_fields_filter'][custom_filter] = list(
                    map(custom_value_to_uuid, filter_set['custom_fields_filter'][custom_filter]))

        if filter_set.get('custom_relations_filter'):
            for custom_filter in filter_set.get('custom_relations_filter'):
                filter_set['custom_relations_filter'][custom_filter] = list(
                    map(none_converter, filter_set['custom_relations_filter'][custom_filter]))

        for event in self.api_events_generator(gantt):
            if filter_set.get('unfilled_events_filter'):
                if filter_set.get('unfilled_events_filter').get('Только незаполненные мероприятия'):
                    if event.get('start') is not None and event.get('end') is not None:
                        continue
                if not filter_set.get('unfilled_events_filter').get('Отображать незаполненные мероприятия'):
                    if event.get('start') is None or event.get('end') is None:
                        continue
            if filter_set.get('custom_fields_filter'):
                for field in filter_set.get('custom_fields_filter'):
                    if filter_set.get('custom_fields_filter').get(field) != []:
                        actual = self.api_get_custom_field_value(gantt, field, event)
                        expected = filter_set.get('custom_fields_filter').get(field)
                        if filter_set.get('custom_fields_filter').get(field) != '(пусто)':
                            if actual not in expected:
                                invalid_field = True
                                break
                            else:
                                invalid_field = False
                        else:
                            if actual is not None:
                                invalid_field = True
                                break
                            else:
                                invalid_field = False
            if filter_set.get('custom_relations_filter'):
                for relation in filter_set.get('custom_relations_filter'):
                    if filter_set.get('custom_relations_filter').get(relation) != []:
                        actual = self.api_get_custom_relation_values(gantt, relation, event)
                        expected = filter_set.get('custom_relations_filter').get(relation)
                        if filter_set.get('custom_relations_filter').get(relation) != '(пусто)':
                            if actual != []:
                                for actual_value in actual:
                                    if actual_value not in expected:
                                        invalid_relation = True
                                    else:
                                        invalid_relation = False
                                        break
                            else:
                                invalid_relation = True
                        else:
                            if actual != []:
                                invalid_relation = True
                                break
                            else:
                                invalid_relation = False
            if invalid_field or invalid_relation:
                continue

            if names_only:
                if anti_doublespacing:
                    if group_by:
                        add_in_group(self.anti_doublespacing(event.get('object').get('name')), events, get_group_value(event, gantt, group_by))
                    else:
                        event = self.anti_doublespacing(event.get('object').get('name'))
                        events.append(event)
                else:
                    if group_by:
                        add_in_group(event.get('object').get('name'), events, get_group_value(event, gantt, group_by))
                    else:
                        event = event.get('object').get('name')
                        events.append(event)
            else:
                if group_by:
                    add_in_group(event, events, get_group_value(event, gantt, group_by))
                else:
                    events.append(event)
        return events

    def api_event_names_generator(self, version, plan_uuid, login, deleleted_only=False, get_deleted=True):
        gantt = self.api_get_gantt(version, plan_uuid, login)
        tasks = gantt.get('data').get('tasks')
        if deleleted_only:
            for task in tasks:
                if task.get('start') is None and task.get('end') is None:
                    yield task.get('object').get('name')
        else:
            if get_deleted:
                for task in tasks:
                    yield task.get('object').get('name')
            else:
                for task in tasks:
                    if task.get('start') is not None and task.get('end') is not None:
                        yield task.get('object').get('name')

    @staticmethod
    def api_events_generator(gantt):
        tasks = gantt.get('data').get('tasks')
        for task in tasks:
            yield task

    def api_create_unique_event_name(self, base_name, versions, plan_uuid, login, subname=None):
        events_list = []
        for version in versions:
            events = self.api_get_event_names(version, plan_uuid, login)
            events_list.extend(events)
        count = 0
        if not subname:
            new_name = base_name
        else:
            new_name = f'{base_name}_{subname}'
        while new_name in events_list:
            count += 1
            if not subname:
                new_name = "{0}_{1}".format(base_name, count)
            else:
                new_name = "{0}_{1}_{2}".format(base_name, subname, count)
        return new_name

    def api_create_plan(self, plan_data, ignore_error=False):
        """
        plan_data = {
            'comment': 'test',
            'name': 'name',
            'planStart': '2020-05-28T00:00:00.000Z',
            'planType': 14,
            'responsibleUuid': '7989e70a-8a2a-11ea-bf82-02000a0a140c',
            'sourceModelUuid': '01ea9444-bd74-9f28-5b11-00b15c0c400',
            'sourceVersionUuid': '01ea9444-bd87-a506-c853-00b15c0c4000'
        }
        """
        request = self.post(f'{Vars.PKM_API_URL}plans/create', self.token, plan_data)
        if not ignore_error:
            assert not request.get('error'), f'Ошибка при создании версии'
            assert request.get('uuid') is not None, 'Невозможно получить uuid созданного плана'
        uuid = request.get('uuid')
        if ignore_error and not uuid:
            return None
        time.sleep(Vars.PKM_API_WAIT_TIME*2)
        plans = self.api_get_plans()
        for plan in plans:
            if plan.get('uuid') == uuid:
                return plan
        if not ignore_error:
            raise AssertionError(f'План "{plan_data}" не сохранился в системе')
        else:
            return {}

    def check_k6_plan_copy(self, k6_plan_comment, k6_plan_uuid, ignore_error=False):
        today = self.get_utc_date()
        start_date = f'{today[2]}-{today[1]}-{today[0]}T00:00:00.000Z'
        copy_comment = f'{k6_plan_comment[3:]}-autotest_copy'
        plans = self.api_get_plans()
        for plan in plans:
            if plan.get('settings').get('plan').get('comment') == copy_comment:
                plan['is_new_created'] = False
                return plan
            if plan.get('uuid') == k6_plan_uuid:
                start_date = plan.get('timeMeasurement').get('timeStart')

        version = self.api_get_version_uuid(k6_plan_uuid, 'Проект плана')
        user = self.api_get_user_by_login(users.admin.login)
        copied_plan_data = {
            'comment': copy_comment,
            'name': 'name',
            'planStart': start_date,
            'planType': 14,
            'responsibleUuid': user.get('uuid'),
            'sourceModelUuid': k6_plan_uuid,
            'sourceVersionUuid': version
        }
        plan = self.api_create_plan(copied_plan_data, ignore_error=ignore_error)
        plan['is_new_created'] = True
        return plan

    def get_object(self, object_uuid):
        payload = {
            'uuids': [object_uuid]
        }
        pkm_objects = self.post(f'{Vars.PKM_API_URL}objects/get', self.token, payload).get('data')
        for pkm_object in pkm_objects:
            if pkm_object.get('uuid') == object_uuid:
                return pkm_object
        return None

    @staticmethod
    def api_get_custom_relation_objects(gantt, custom_relation_name):
        custom_relations = gantt.get('data').get('relations').get('customRelations')
        relation = {}
        for relation in custom_relations:
            if relation.get('name') == custom_relation_name:
                break
        relation_objects = relation.get('relatedObjects')
        return relation_objects

    def api_get_custom_relation_value(self, gantt, custom_relation_name, event):
        task_object_uuid = event.get('object').get('uuid')
        custom_relations_objects = self.api_get_custom_relation_objects(gantt, custom_relation_name)
        value_object_uuid = None
        for related_object in custom_relations_objects:
            if related_object.get('destinationObjectUuid') == task_object_uuid:
                value_object_uuid = related_object.get('sourceObjectUuid')
                break
            elif related_object.get('sourceObjectUuid') == task_object_uuid:
                value_object_uuid = related_object.get('destinationObjectUuid')
                break
        if value_object_uuid:
            value_object = self.get_object(value_object_uuid)
            value_name = value_object.get('name')
            return self.anti_doublespacing(value_name)
        else:
            return None

    def api_get_custom_relation_values(self, gantt, custom_relation_name, event):
        values = []
        task_object_uuid = event.get('object').get('uuid')
        custom_relations_objects = self.api_get_custom_relation_objects(gantt, custom_relation_name)
        for related_object in custom_relations_objects:
            if related_object.get('destinationObjectUuid') == task_object_uuid:
                values.append(self.anti_doublespacing(self.get_object(related_object.get('sourceObjectUuid')).get('name')))
            elif related_object.get('sourceObjectUuid') == task_object_uuid:
                values.append(self.anti_doublespacing(self.get_object(related_object.get('destinationObjectUuid')).get('name')))
        return values

    @staticmethod
    def api_get_custom_field_uuid(gantt, custom_field_name):
        for custom_field_uuid in gantt.get('ganttDiagram').get('options')[0].get('customFields'):
            if gantt.get('ganttDiagram').get('options')[0].get('customFields').get(custom_field_uuid) == custom_field_name:
                return custom_field_uuid
        return None

    def api_get_custom_field_value(self, gantt, custom_field_name, event):
        if event.get('custom') is not None and event.get('custom') != {}:
            if custom_field_name == 'Тип мероприятия':
                custom_field_name = 'Тип работ'
            custom_field_uuid = self.api_get_custom_field_uuid(gantt, custom_field_name)
            for custom_field in event.get('custom'):
                if custom_field == custom_field_uuid:
                    return event.get('custom').get(custom_field)
        return None


class ApiCreator(BaseApi):
    def get_api_eu(self):
        return ApiEu(self.login, self.password, token=self.token)

    def get_api_classes(self):
        return ApiClasses(self.login, self.password, token=self.token)

    def get_api_models(self):
        return ApiModels(self.login, self.password, token=self.token)
