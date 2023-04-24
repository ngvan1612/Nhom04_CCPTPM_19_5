import pytest
import requests
import json
import random
import binascii
import os
import sys
import hashlib
from type import *

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
        print(f'------ DELETE {len(ids)} projects')
        for idx in ids:
            self.delete_project(idx)

    @pytest.mark.skip
    def delete_project(self, project_id):
        resp = requests.delete(URL_DELETE_PROJECT + str(project_id))
        if resp.status_code == 204:
            return True
        else:
            return json.loads(resp.text)

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
        return json.loads(resp.text)
    
    @pytest.mark.skip
    def retrieve_project(self, project_id) -> json:
        resp = requests.get(
            URL_RETRIEVE_PROJECT + str(project_id)
        )
        return json.loads(resp.text)
    
    @pytest.mark.skip
    def duplicate_project(self, project_id) -> json:
        resp = requests.post(
            URL_RETRIEVE_PROJECT + str(project_id) + '/duplicate'
        )
        return json.loads(resp.text)
    
    @pytest.mark.skip
    def edit_project(self, project_id) -> json:
        resp = requests.put(
            URL_RETRIEVE_PROJECT + str(project_id),
            data={
                    "scale": 800,

                    "rotate": 90,
                    "trim": "5.1,20.5"
                },
        )
        return json.loads(resp.text)
    
    @pytest.mark.skip
    def get_video(self, project_id) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + '/raw/video'
        )
        return  resp.content, resp.status_code
    
    def test_01(self):
        """
            `Test activity diagram: DELETE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Xóa project
            3. Kiểm tra xem project đã bị xóa hay chưa
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')

        # truy xuất thông tin project
        resp_project = self.retrieve_project(_id)

        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

        resp_get_video, statusCode = self.get_video(_id)
        resp_get_video=json.loads(resp_get_video.decode("utf-8"))

        assert resp_get_video["error"] == 'Project with id \''+ _id +'\' was not found.'

    #TODO: fix this test
    def test_02(self):
        """
            `Test activity diagram: DELETE PROJECT DETAILS`
            1. Truy xuất thông tin project với id không tồn tại
            2. Kiểm tra xem có thông báo lỗi hay không
        """
        result = binascii.b2a_hex(os.urandom(10))
        _id = result.decode('utf-8') 

        resp_project = self.delete_project(_id)

        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

        resp_get_video, statusCode = self.get_video(_id)
        resp_get_video=json.loads(resp_get_video.decode("utf-8"))

        assert resp_get_video["error"] == 'Project with id \''+ _id +'\' was not found.'

    def test_03(self):
        """
            `Test activity diagram: DELETE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project vừa tạo
            3. Xóa project gốc
            4. Kiểm tra xem project đã bị xóa hay chưa
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_duplicate = self.duplicate_project(_id_create)
        _id_duplicate = resp_duplicate['_id']
        print(f'2. duplicate {_id_duplicate}')
                
        self.delete_project(_id_create)
        print(f'3. deleted ok')

        resp_retrieve_id_create = self.retrieve_project(_id_create)
        assert resp_retrieve_id_create['error'] == 'Project with id \''+ _id_create +'\' was not found.'

        resp_retrieve_id_duplicate = self.retrieve_project(_id_duplicate)
        assert resp_retrieve_id_duplicate['_id'] == _id_duplicate

        resp_get_video, statusCode = self.get_video(_id_create)
        resp_get_video=json.loads(resp_get_video.decode("utf-8"))

        assert resp_get_video["error"] == 'Project with id \''+ _id_create +'\' was not found.'

        self.delete_project(_id_duplicate)

    def test_04(self):
        """
            `Test activity diagram: DELETE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project vừa tạo
            3. Xóa project bản sao
            4. Kiểm tra xem project đã bị xóa hay chưa và có ảnh hưởng các project khác hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_duplicate = self.duplicate_project(_id_create)
        _id_duplicate = resp_duplicate['_id']
        print(f'2. duplicate {_id_duplicate}')
                
        self.delete_project(_id_duplicate)
        print(f'3. deleted ok')

        resp_retrieve_id_create = self.retrieve_project(_id_create)
        assert resp_retrieve_id_create['_id'] == _id_create

        resp_get_video, statusCode = self.get_video(_id_duplicate)
        resp_get_video=json.loads(resp_get_video.decode("utf-8"))

        assert resp_get_video["error"] == 'Project with id \''+ _id_duplicate +'\' was not found.'

        resp_retrieve_id_duplicate = self.retrieve_project(_id_duplicate)
        assert resp_retrieve_id_duplicate['error'] == 'Project with id \''+ _id_duplicate +'\' was not found.'

        self.delete_project(_id_create)

    def test_05(self):
        """
            `Test activity diagram: DELETE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project vừa tạo
            3. Duplicate project bản sao
            4. Xóa project bản sao version 1
            5. Kiểm tra xem project đã bị xóa hay chưa và có ảnh hưởng các project khác không
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_duplicate_version_1 = self.duplicate_project(_id_create)
        _id_duplicate_version_1 = resp_duplicate_version_1['_id']
        print(f'2. duplicate {_id_duplicate_version_1}')

        resp_duplicate_version_2 = self.duplicate_project(_id_duplicate_version_1)
        _id_duplicate_version_2 = resp_duplicate_version_2['_id']
        print(f'3. duplicate {_id_duplicate_version_2}')
                
        self.delete_project(_id_duplicate_version_1)
        print(f'deleted ok')

        resp_retrieve_id_create = self.retrieve_project(_id_create)
        assert resp_retrieve_id_create['_id'] == _id_create

        resp_retrieve_version_2 = self.retrieve_project(_id_duplicate_version_2)
        assert resp_retrieve_version_2['_id'] == _id_duplicate_version_2

        resp_get_video, statusCode = self.get_video(_id_duplicate_version_1)
        resp_get_video=json.loads(resp_get_video.decode("utf-8"))

        assert resp_get_video["error"] == 'Project with id \''+ _id_duplicate_version_1 +'\' was not found.'

        resp_retrieve_id_duplicate = self.retrieve_project(_id_duplicate_version_1)
        assert resp_retrieve_id_duplicate['error'] == 'Project with id \''+ _id_duplicate_version_1 +'\' was not found.'

        self.delete_project(_id_create)
        self.delete_project(_id_duplicate_version_2)

