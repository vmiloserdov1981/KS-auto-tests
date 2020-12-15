from api.api import ApiDictionaries
from progress.bar import Bar
import time

name = 'Тестовый_справочник'
project_uuid = '01eb0e06-136f-b9d4-784e-00b15c0c4000'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlcyI6WyLQt9Cw0YDQtdCz0LjRgdGC0YDQuNGA0L7QstCw0L3QvdGL0LkiLCLQsNC00LzQuNC90LjRgdGC0YDQsNGC0L7RgCJdLCJleHAiOjE2MDgwMTgwMTksImp0aSI6IjAxZWIwZTA0LWQxNjctODIyZC1kMjY2LTAwMDAwMDAwMDAwMCJ9.KrVpgLhflWQlHcibo0iOEfRGGhXDtRmbYuAP2xxDpnc'
dict_api = ApiDictionaries(None, None, project_uuid, token=token)
to_delete = []

tree = dict_api.get_dicts_tree()
for node in tree:
    if name in node.get('name'):
        to_delete.append(node.get('uuid'))
if len(to_delete) > 0:
    bar = Bar('delete nodes', max=len(to_delete))
    for node_uuid in to_delete:
        bar.next()
        dict_api.delete_node(node_uuid)
        # time.sleep(2)
    bar.finish()



