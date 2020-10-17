from core import BaseApi
from variables import PkmVars as Vars


class ApiDictionaries(BaseApi):

    def api_get_dicts_names(self):
        dicts = self.post(f'{Vars.PKM_API_URL}dictionaries/get-tree', self.token, {}).get('data')
        names = [dictionary.get('name') for dictionary in dicts]
        return names

    def create_unique_dict_name(self, basename):
        dicts_list = self.api_get_dicts_names()
        count = 0
        newname = basename
        while newname in dicts_list:
            count += 1
            newname = f"{basename}_{count}"
        return newname

