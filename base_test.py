import pytest
import requests
from type import *
import json
import random

class TestBase:

    ids = []

    @pytest.mark.skip
    def get_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        print(json_data['_items'])

    @pytest.mark.skip
    def delete_all_projects(self):
        resp = requests.get(URL_LIST_PROJECTS)
        json_data = json.loads(resp.text)
        _items = json_data['_items']
        #ids = [x['_id'] for x in _items]
        print(f'------ DELETE {len(self.ids)} projects')
        for idx in self.ids:
            self.delete_project(idx)

    @pytest.mark.skip
    def delete_project(self, project_id):
        try:
            requests.delete(URL_DELETE_PROJECT + str(project_id))
            print(f"DEL PROJECT {project_id} SUCCESSFULLY")
        except Exception as e:
            print(f"DEL PROJECT ERROR: {e}")

    @pytest.mark.skip
    def create_project(self, video: str) -> json:
        with open(video, 'rb') as f:
            buffer = f.read()
        resp = requests.post(
            url=URL_CREATE_PROJECT,
            files={
                'file': (str(random.random()) + '.mp4', buffer, 'video/mp4')
            }
        )
        j = json.loads(resp.text)

        self.ids.append(j['_id'])

        return j
