import pytest
import requests
import json
import random
import binascii
import os
from base_test import TestBase
from type import *

class TestRetrieveProject(TestBase):

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
            json={
                    "scale": 800,
                    "rotate": 90,
                    "trim": "5.1,20.5"
                },
        )
        return json.loads(resp.text)
    
    def test_01(self):
        """
            `Test activity diagram: RETRIEVE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Truy xuất thông tin project
            3. Kiểm tra thông tin khớp với p-01.mp4
            4. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # truy xuất thông tin project
        resp_project = self.retrieve_project(_id)
        print(resp_project)

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp_project['metadata']['codec_name'] == 'h264'
        assert resp_project['metadata']['width'] == 848
        assert resp_project['metadata']['height'] == 480
        assert resp_project['metadata']['r_frame_rate'] == '30/1'
        assert resp_project['metadata']['bit_rate'] == 1467581
        assert resp_project['metadata']['nb_frames'] == 1117
        assert abs(resp_project['metadata']['duration'] - 37.233333) <= 1e-3
        assert resp_project['metadata']['size'] == 8037827

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')

    def test_02(self):
        """
            `Test activity diagram: RETRIEVE PROJECT DETAILS`
            1. Truy xuất thông tin project với id không tồn tại
            2. Kiểm tra xem có thông báo lỗi hay không
        """
        result = binascii.b2a_hex(os.urandom(10))
        _id = result.decode('utf-8')        

        # truy xuất thông tin project
        resp_project = self.retrieve_project(_id)
        print(resp_project)

        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

    def test_03(self):
        """
            `Test activity diagram: RETRIEVE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Xóa project
            3. Truy xuất thông tin project
            4. Kiểm tra xem có thông báo lỗi hay không
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
        print(resp_project)

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

        print(f'2. checked ok')
                
    def test_04(self):
        """
            `Test activity diagram: RETRIEVE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate một project để chỉnh sửa nhưng chưa chỉnh sửa
            2. Truy xuất thông tin project
            3. Kiểm tra thông tin khớp với project bản sao nhưng chưa chỉnh sửa đó
            4. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']
        print(f'2. duplicated {_id_dup}')

        # truy xuất thông tin project
        resp_project = self.retrieve_project(_id_dup)
        print(resp_project)

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp_project['metadata']['codec_name'] == 'h264'
        assert resp_project['metadata']['width'] == 848
        assert resp_project['metadata']['height'] == 480
        assert resp_project['metadata']['r_frame_rate'] == '30/1'
        assert resp_project['metadata']['bit_rate'] == 1467581
        assert resp_project['metadata']['nb_frames'] == 1117
        assert abs(resp_project['metadata']['duration'] - 37.233333) <= 1e-3
        assert resp_project['metadata']['size'] == 8037827

        print(f'4. checked ok')

        # xóa project
        self.delete_project(_id_create)
        self.delete_project(_id_dup)
        print(f'3. deleted ok')

    def __waitingCondition(self, condition_func):
        import time
        begin = time.time()
        while time.time() - begin < TIMEOUT_CHECK_TEST_CASE:
            try:
                if condition_func():
                    return True
            except:
                time.sleep(1)
                pass

    def test_05(self):
        """
            `Test activity diagram: RETRIEVE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate một project để chỉnh 
            3. Chỉnh sửa project
            4. Truy xuất thông tin project
            5. Kiểm tra thông tin khớp với project bản sao nhưng chưa chỉnh sửa đó
            6. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']
        print(f'2. duplicated {_id_dup}')

        # chỉnh sửa project
        resp_edit = self.edit_project(_id_dup)
        print(resp_edit)
        assert resp_edit['processing'] == True

        def condition_func():
            resp = self.retrieve_project(_id_dup)
            return resp['metadata']['width'] == 452
        
        self.__waitingCondition(condition_func)

        # truy xuất thông tin project
        resp_project = self.retrieve_project(_id_dup)
        print(resp_project)

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp_project['metadata']['codec_name'] == 'h264'
        assert resp_project['metadata']['width'] == 452
        assert resp_project['metadata']['height'] == 800
        assert resp_project['metadata']['r_frame_rate'] == '30/1'
        assert resp_project['metadata']['nb_frames'] == 462
        assert abs(resp_project['metadata']['duration'] - 15.4) <= 1e-3
        assert resp_project['parent'] == _id_create

        # print(f'4. checked ok')

        # xóa project
        self.delete_project(_id_create)
        self.delete_project(_id_dup)
        print(f'3. deleted ok')