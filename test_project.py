import requests
import json
from type import *
from test_abstract import TestAbstract
import pytest

class TestProject:

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
        ids = [x['_id'] for x in _items]
        
        for idx in ids:
            resp = requests.delete(URL_DELETE_PROJECT + str(idx))
            print(resp.text)

    @pytest.mark.skip
    def create_project(self, video: str) -> json:
        resp = requests.post(URL_CREATE_PROJECT, )
        return json.loads(resp.text)

    def test_01(self):
        """
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Kiểm tra lại danh sách project
            3. Xóa project
        """
        pass

