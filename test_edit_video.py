import pytest
import requests
import json
import random
import time
import binascii
import os
from base_test import TestBase
from type import *
import hashlib

class TestEditVideo(TestBase):
    
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
    def edit_project(self, project_id, json_request) -> json:
        resp = requests.put(
            URL_RETRIEVE_PROJECT + str(project_id),
            json=json_request,
        )
        return json.loads(resp.text)

    @pytest.mark.skip
    def get_video(self, project_id) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + '/raw/video'
        )
        return  resp.content, resp.status_code
    
    @pytest.mark.skip
    def calc_md5_from_stream(self, stream) -> str:
        return hashlib.md5(stream).hexdigest()

    def test_01(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Edit video gốc vừa tạo
            3. Kiểm tra xem có thông báo không cho edit video gốc hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        self.waiting_for_processing(_id_create)

        json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 800,
                "trim": "4.1,100.5"
                }
        
        resp_project = self.edit_project(_id_create, json_request)
        print(resp_project)
        self.waiting_for_processing(_id_create)

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        assert resp_project['project_id'] == ['Video with version 1 is not editable, use duplicated project instead.']


    def test_02(self):
        """
            `Test activity diagram: EDIT PROJECT DETAILS`
            1. Edit project với id không tồn tại
            2. Kiểm tra xem có thông báo lỗi hay không
        """
        result = binascii.b2a_hex(os.urandom(10))
        _id = result.decode('utf-8')    
        print(_id)

        json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 800,
                "trim": "4.1,100.5"
                }

        resp_project = self.edit_project(_id, json_request)
        print(resp_project)
        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

    def test_03(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Duplicate project vừa tạo
            2. Edit video duplicate
            3. Kiểm tra xem video mẫu và video sau edit có giống nhau hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')
        self.waiting_for_processing(_id_create)

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']

        json_request = {
                "scale": 5
                }
        
        resp_project = self.edit_project(_id_dup, json_request)
        print(resp_project)
        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        video, status_code = self.get_video(_id_dup)
        print(status_code)

        with open('test_data/video-after-edit-03.mp4', 'rb') as file:
            video2 = file.read()

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        print(len(video))
        print(len(video2))

        md5_v1 = self.calc_md5_from_stream(video)
        md5_v2 = self.calc_md5_from_stream(video2)

        assert md5_v1 == md5_v2

    def test_04(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Duplicate project vừa tạo
            2. Edit video duplicate
            3. Kiểm tra xem video mẫu và video sau edit có giống nhau hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        self.waiting_for_processing(_id_create)

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']
        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        json_request = {
                "crop": "400,300,320,180"
                }
        
        resp_project = self.edit_project(_id_dup, json_request)
        print(resp_project)

        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        video, status_code = self.get_video(_id_dup)
        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        with open('test_data/video-after-edit-04.mp4', 'rb') as file:
            video2 = file.read()

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        md5_v1 = self.calc_md5_from_stream(video)
        md5_v2 = self.calc_md5_from_stream(video2)

        assert md5_v1 == md5_v2


    def test_05(self):
        """
            `Test activity diagram: EDIT PROJECT`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Duplicate project vừa tạo
            2. Edit video duplicate
            3. Kiểm tra xem video mẫu và video sau edit có giống nhau hay không
        """
        # tạo project
        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')
        self.waiting_for_processing(_id_create)

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']
        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 5,
                "trim": "4.1,100.5"
                }
        
        resp_project = self.edit_project(_id_dup, json_request)
        print(resp_project)
        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        video, status_code = self.get_video(_id_dup)
        self.waiting_for_processing(_id_create)
        self.waiting_for_processing(_id_dup)

        with open('test_data/video-after-edit-02.mp4', 'rb') as file:
            video2 = file.read()

        self.delete_project(_id_create)
        print(f'3. deleted ok')

        md5_v1 = self.calc_md5_from_stream(video)
        md5_v2 = self.calc_md5_from_stream(video2)

        assert md5_v1 == md5_v2