from core import BaseApi
from variables import PkmVars as Vars
import time
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

    def api_get_user(self, login, name):
        users_list = self.post(f'{Vars.PKM_API_URL}users/get-list', self.token, {}).get('data')
        for user in users_list:
            if user.get('login') == login and user.get('fullName') == name:
                return user

    def api_create_user(self, email, login, password, user_name, settings):
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
        assert not request.get('error'), f'Ошибка при создании пользователя "{user_name}"'
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
            numbers.append(comment.split(Vars.PKM_DEFAULT_K6_PLAN_COMMENT)[1])
        numbers.sort(reverse=True)
        last_number = numbers[0]
        comment = f'{Vars.PKM_DEFAULT_K6_PLAN_COMMENT}{last_number}'

        def f_func(x):
            if x.get('settings').get('plan').get('comment') == comment:
                return True
            else:
                return False

        plan = filter(f_func, plans.get('plans'))
        plan = list(plan)
        return plan[0]

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
                        "data": event_data.get('event_type'),
                        "type": "string"
                    }
                }
            ],
            works_type_uuid: [
                {
                    "value": {
                        "data": event_data.get('works_type'),
                        "type": "string"
                    }
                }
            ],
            plan_type_uuid: [
                {
                    "value": {
                        "data": event_data.get('plan'),
                        "type": "string"
                    }
                }
            ],
            ready_type_uuid: [
                {
                    "value": {
                        "data": event_data.get('ready'),
                        "type": "string"
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
                    'data': event_data.get('event_type'),
                    'type': 'string'
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
                    'data': event_data.get('works_type'),
                    'type': 'string'
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
                    'data': event_data.get('plan'),
                    'type': 'string'
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
                    'data': event_data.get('ready'),
                    'type': 'string'
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

    def anti_doublespacing(self, string):
        if '  ' in string:
            string_list = string.split(' ')
            new_string_list = [elem for elem in string_list if elem != '']
            string = ' '.join(new_string_list)
            return string
        else:
            return string

    def api_get_event_names(self, version, plan_uuid, login, deleleted_only=False, get_deleted=True):
        if deleleted_only:
            return [self.anti_doublespacing(event) for event in self.api_event_names_generator(version, plan_uuid, login, deleleted_only=True)]
        else:
            if get_deleted:
                return [self.anti_doublespacing(event) for event in self.api_event_names_generator(version, plan_uuid, login, get_deleted=True)]
            else:
                return [self.anti_doublespacing(event) for event in self.api_event_names_generator(version, plan_uuid, login, get_deleted=False)]

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

    def api_create_plan(self, plan_data):
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
        assert not request.get('error'), f'Ошибка при создании версии'
        assert request.get('uuid') is not None, 'Невозможно получить uuid созданного плана'
        uuid = request.get('uuid')
        time.sleep(Vars.PKM_API_WAIT_TIME*2)
        plans = self.api_get_plans()
        for plan in plans:
            if plan.get('uuid') == uuid:
                return plan
        raise AssertionError(f'План "{plan_data}" не сохранился в системе')

    def check_k6_plan_copy(self, k6_plan_comment, k6_plan_uuid):
        copy_comment = f'{k6_plan_comment[3:]}-autotest_copy'
        plans = self.api_get_plans()
        for plan in plans:
            if plan.get('settings').get('plan').get('comment') == copy_comment:
                plan['is_new_created'] = False
                return plan

        today = self.get_utc_date()
        start_date = f'{today[2]}-{today[1]}-{today[0]}T00:00:00.000Z'
        version = self.api_get_version_uuid(k6_plan_uuid, 'Проект плана')
        user = self.api_get_user_by_login(users.eu_user.login)
        copied_plan_data = {
            'comment': copy_comment,
            'name': 'name',
            'planStart': start_date,
            'planType': 14,
            'responsibleUuid': user.get('uuid'),
            'sourceModelUuid': k6_plan_uuid,
            'sourceVersionUuid': version
        }
        plan = self.api_create_plan(copied_plan_data)
        plan['is_new_created'] = True
        return plan

