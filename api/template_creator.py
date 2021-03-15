from variables import PkmVars as Vars
from api.api_models import ApiModels
from api.api_classes import ApiClasses
from concurrent.futures import ThreadPoolExecutor


class TemplateCreator:
    def __init__(self, project_uuid, login=None, password=None, token=None, api_url=Vars.PKM_API_URL):
        self.model_api = ApiModels(login, password, project_uuid, token=token, api_url=api_url)
        self.classes_api = ApiClasses(login, password, project_uuid, token=token, api_url=api_url)

    def create_table_template(self, classes_folder_uuid=None, models_folder_uuid=None, names=None):
        if not names:
            names = {
                      'class_name': "Шаблонный класс",
                      'indicator_name': "Показатель",
                      'formula_name': "Формула",
                      'model_name': "Шаблонная модель",
                      'dataset_name': "Набор",
                      'object_name': "Объект"
                      }
        result = {}

        with ThreadPoolExecutor() as executor:
            class_data = result['class_data'] = executor.submit(self.classes_api.create_class_node, names.get('class_name'), parent_uuid=classes_folder_uuid, create_unique_name=True).result()
            model_data = result['model_data'] = executor.submit(self.model_api.create_model_node, names.get('model_name'), parent_uuid=models_folder_uuid, create_unique_name=True).result()

        with ThreadPoolExecutor() as executor:
            result['indicator_1_data'] = executor.submit(self.classes_api.create_indicator_node, f"{names.get('indicator_name')}_1", class_data.get('referenceUuid'), class_data.get('nodeUuid'), 'number').result()
            result['indicator_2_data'] = executor.submit(self.classes_api.create_indicator_node, f"{names.get('indicator_name')}_2", class_data.get('referenceUuid'), class_data.get('nodeUuid'), 'number').result()
            result['indicator_3_data'] = executor.submit(self.classes_api.create_indicator_node, f"{names.get('indicator_name')}_3", class_data.get('referenceUuid'), class_data.get('nodeUuid'), 'number').result()
            result['indicator_4_data'] = executor.submit(self.classes_api.create_indicator_node, f"{names.get('indicator_name')}_4", class_data.get('referenceUuid'), class_data.get('nodeUuid'), 'string').result()
            result['dataset_1_data'] = executor.submit(self.model_api.create_dataset, f"{names.get('dataset_name')}_1", model_data.get('referenceUuid')).result()
            result['dataset_2_data'] = executor.submit(self.model_api.create_dataset, f"{names.get('dataset_name')}_2", model_data.get('referenceUuid')).result()

        formula_data = {
            'class_uuid': class_data.get('referenceUuid'),
            'indicator_uuid': result.get('indicator_3_data').get('referenceUuid'),
            'formula_name': names.get('formula_name'),
            'calc_indicator_1_uuid': result.get('indicator_1_data').get('referenceUuid'),
            'calc_indicator_2_uuid': result.get('indicator_2_data').get('referenceUuid'),
            'modifier_type': '-'
        }
        result['formula_data'] = self.classes_api.create_simple_formula(formula_data)

        with ThreadPoolExecutor() as executor:
            result['object_1_data'] = executor.submit(self.model_api.create_object_node, f"{names.get('object_name')}_1", class_data.get('referenceUuid'), model_data.get('referenceUuid'), model_data.get('nodeUuid')).result()
            result['object_2_data'] = executor.submit(self.model_api.create_object_node, f"{names.get('object_name')}_2", class_data.get('referenceUuid'), model_data.get('referenceUuid'), model_data.get('nodeUuid')).result()

        return result
