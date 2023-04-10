import requests
import json
from type import *
from test_abstract import TestAbstract
import pytest
import random

class TestCreateProject:

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
        print(f'------ DELETE {len(ids)} projects')
        for idx in ids:
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
        print('ok1')
        with open(video, 'rb') as f:
            buffer = f.read()
        print('ok2')
        resp = requests.post(
            url=URL_CREATE_PROJECT,
            files={
                'file': (str(random.random()) + '.mp4', buffer, 'video/mp4')
            }
        )
        print('ok3')
        return json.loads(resp.text)

    def test_01(self):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp['metadata']['codec_name'] == 'h264'
        assert resp['metadata']['width'] == 848
        assert resp['metadata']['height'] == 480
        assert resp['metadata']['r_frame_rate'] == '30/1'
        assert resp['metadata']['bit_rate'] == 1467581
        assert resp['metadata']['nb_frames'] == 1117
        assert abs(resp['metadata']['duration'] - 37.233333) <= 1e-3
        assert resp['metadata']['size'] == 8037827

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')
    
    def test_02(self):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-02.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp['metadata']['codec_name'] == 'h264'
        assert resp['metadata']['width'] == 848
        assert resp['metadata']['height'] == 480
        assert resp['metadata']['r_frame_rate'] == '30/1'
        assert resp['metadata']['bit_rate'] == 1467581
        assert resp['metadata']['nb_frames'] == 1117
        assert abs(resp['metadata']['duration'] - 37.233333) <= 1e-3
        assert resp['metadata']['size'] == 8037827

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')
