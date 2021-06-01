import os


class PkmVars:
    PKM_MAIN_URL = 'https://pkm.andersenlab.com/' if os.getenv('USE_STAGE') != 'true' else 'https://rc-test.ks.works/'
    PKM_API_URL = f'{PKM_MAIN_URL}api/'
    PKM_TEST_FOLDER_NAME = 'auto-test'
    DEFAULT_PROJECT_NAME = 'Шельф. Приразломная'
    PKM_PROJECT_NAME = os.getenv('PROJECT_NAME', 'Шельф. Приразломная')
    PKM_PUBLICATION_NAME = 'Приразломная'
    PKM_BASE_DICTIONARY_NAME = 'Тестовый_справочник'
    PKM_BASE_CLASS_NAME = 'Тестовый_класс'
    PKM_BASE_MODEL_NAME = 'Тестовая_модель'
    PKM_RELATION_CLASS_NAME = 'Класс для связи'
    PKM_BASE_FOLDER_NAME = 'auto_folder-2'
    PKM_DEFAULT_TREE_TYPE = 'model'
    PKM_BASE_INDICATOR_NAME = 'Показатель'
    PKM_INDICATOR_NAME_TYPE = {
        'number': ' Число ',
        'string': ' Строка ',
        'datetime': ' Дата ',
        'boolean': ' Логический ',
        'dictionary': ' Справочник значений '
    }
    PKM_API_WAIT_TIME = 5
    PKM_USER_WAIT_TIME = 5
    PKM_DEFAULT_FORMULA_NAME = 'formula'
    PKM_BASE_OBJECT_NAME = 'object'
    PKM_BASE_DATASET_NAME = 'dataset'
    PKM_BASE_TABLE_NAME = 'table'
    PKM_ADMIN_ROLE_NAME = 'администратор'
    PKM_DEFAULT_K6_PLAN_COMMENT = 'k6-test-'
    PKM_BASE_EVENT_NAME = 'Тестовое мероприятие'
