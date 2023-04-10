import pytest
import requests
import json
import random
import binascii
import os
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
            json={
                    "scale": 800,
                    "rotate": 90,
                    "trim": "5.1,20.5"
                },
        )
        return json.loads(resp.text)
    
    @pytest.mark.skip
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
    def test_01(self):
        """
            `Test activity diagram: DUPLICATE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project 
            3. Truy xuất thông tin project gốc và thông tin project đã duplicate
            4. Kiểm tra thông tin của project đã duplicate với project gốc
            5. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # duplicate project 
        resp_dupicate = self.duplicate_project(_id)
        _id_dupt = resp_dupicate['_id']
        print(f'2. Duplicated... ')
        
        # truy xuất thông tin project
        resp_retrieve_project = self.retrieve_project(_id)

        # truy xuất thông tin project đã duplicated
        resp_retrieve_dupicate = self.retrieve_project(_id_dupt)

        # kiểm tra thông tin của project đã duplicate với project gốc
        assert resp_retrieve_project['metadata']['codec_name'] == resp_retrieve_dupicate['metadata']['codec_name']
        assert resp_retrieve_project['metadata']['width'] == resp_retrieve_dupicate['metadata']['width']
        assert resp_retrieve_project['metadata']['height'] == resp_retrieve_dupicate['metadata']['height']
        assert resp_retrieve_project['metadata']['r_frame_rate'] == resp_retrieve_dupicate['metadata']['r_frame_rate']
        assert resp_retrieve_project['metadata']['bit_rate'] == resp_retrieve_dupicate['metadata']['bit_rate']
        assert resp_retrieve_project['metadata']['nb_frames'] == resp_retrieve_dupicate['metadata']['nb_frames']
        assert resp_retrieve_project['metadata']['size'] == resp_retrieve_dupicate['metadata']['size']

        print(f'3. checked ok')
                
        # xóa project
        self.delete_project(_id)
        self.delete_project(_id_dupt)
        print(f'4. deleted ok')


    def test_02(self): 
        """
            `Test activity diagram: DUPLICATE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Tạo một id không tồn tại trong hệ thống 
            3. Kiểm tra id vừa được tạo 
            4. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # Tạo một id sinh ngẫu nhiên
        result = binascii.b2a_hex(os.urandom(10))
        _id_random = result.decode('utf-8')
        while(_id == _id_random):
            result = binascii.b2a_hex(os.urandom(10))
            _id_random = result.decode('utf-8')
        
        # Retrive project
        resp_retrieve_dupt = self.retrieve_project(_id_random)
        print(resp_retrieve_dupt)

        assert resp_retrieve_dupt['error'] == 'Project with id \''+ _id_random +'\' was not found.'

        self.delete_project(_id)
        self.delete_project(_id_random)
        print(f'4. deleted ok')
    
    def test_03(self): 
        """
            `Test activity diagram: DUPLICATE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project 
            3. Duplicate project 2 từ project đã duplicate lần 1
            4. Kiểm tra thông tin của project đã duplicate lần 2 với project gốc
            5. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # duplicate project 
        resp_dupicate = self.duplicate_project(_id)
        _id_dupt = resp_dupicate['_id']
        print(f'2. Duplicated project number 1 with id: {_id_dupt} ... ')

        # duplicate project 2
        resp_dupicate_2 = self.duplicate_project(_id_dupt)
        _id_dupt_2 = resp_dupicate_2['_id']
        print(f'2. Duplicated project number 2 with id: {_id_dupt_2}... ')

        resp_retrieve_project = self.retrieve_project(_id)
        resp_retrieve_duplicate = self.retrieve_project(_id_dupt_2)


        assert resp_retrieve_project['metadata']['codec_name'] == resp_retrieve_duplicate['metadata']['codec_name']
        assert resp_retrieve_project['metadata']['width'] == resp_retrieve_duplicate['metadata']['width']
        assert resp_retrieve_project['metadata']['height'] == resp_retrieve_duplicate['metadata']['height']
        assert resp_retrieve_project['metadata']['r_frame_rate'] == resp_retrieve_duplicate['metadata']['r_frame_rate']
        assert resp_retrieve_project['metadata']['bit_rate'] == resp_retrieve_duplicate['metadata']['bit_rate']
        assert resp_retrieve_project['metadata']['nb_frames'] == resp_retrieve_duplicate['metadata']['nb_frames']
        assert resp_retrieve_project['metadata']['size'] == resp_retrieve_duplicate['metadata']['size']

        self.delete_project(_id)
        self.delete_project(_id_dupt)
        self.delete_project(_id_dupt_2)

        print(f'4. deleted ok')

    def test_04(self): 
        """
            `Test activity diagram: DUPLICATE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project 
            3. Chỉnh sửa project 
            4. Duplicate project đã chỉnh sửa
            5. Kiểm tra thông tin của project đã duplicate với project gốc
            6. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        # Duplicate project để chỉnh sửa
        resp_dup = self.duplicate_project(_id_create)
        _id_dup = resp_dup['_id']
        print(f'2. duplicated {_id_dup}')

        # chỉnh sửa project đã duplicate
        resp_edit = self.edit_project(_id_dup)
        print(resp_edit)
        assert resp_edit['processing'] == True

        def condition_func():
            resp = self.retrieve_project(_id_dup)
            return resp['metadata']['width'] == 452
        
        self.__waitingCondition(condition_func)

        # duplicate project từ project đã chỉnh sửa
        resp_dupicate = self.duplicate_project(_id_dup)
        _id_dupt2 = resp_dupicate['_id']
        print(f'2. Duplicated project with id: {_id_dupt2} ... ')

        # truy xuất thông tin project da chinh sua 
        resp_project = self.retrieve_project(_id_dup)
        print(resp_project)
        # truy xuất thông tin project da chinh sua va duplicate 
        resp_project_dupt = self.retrieve_project(_id_dupt2)
        print(resp_project)

        # Kiểm tra thông tin của project đã duplicate với project gốc
        assert resp_project['parent'] == _id_create
        assert resp_project_dupt['parent'] == _id_dup
        assert resp_project['metadata']['codec_name'] == resp_project_dupt['metadata']['codec_name']
        assert resp_project['metadata']['width'] == resp_project_dupt['metadata']['width']
        assert resp_project['metadata']['height'] == resp_project_dupt['metadata']['height']
        assert resp_project['metadata']['r_frame_rate'] == resp_project_dupt['metadata']['r_frame_rate']
        assert resp_project['metadata']['bit_rate'] == resp_project_dupt['metadata']['bit_rate']
        assert resp_project['metadata']['nb_frames'] == resp_project_dupt['metadata']['nb_frames']
        assert resp_project['metadata']['size'] == resp_project_dupt['metadata']['size']
        # print(f'4. checked ok')

        # xóa project
        self.delete_project(_id_create)
        self.delete_project(_id_dup)
        self.delete_project(_id_dupt2)
        print(f'3. deleted ok')

    def test_05(self): 
        """
            `Test activity diagram: DUPLICATE PROJECT DETAILS`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Duplicate project 
            3. Truy xuất thông tin project gốc và thông tin project đã duplicate
            4. Kiểm tra thông tin của project đã duplicate với project gốc
            5. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # duplicate project 
        resp_dupicate = self.duplicate_project(_id)
        _id_dupt = resp_dupicate['_id']
        print(f'2. Duplicated... ')
        
        # truy xuất thông tin project
        resp_retrieve_project = self.retrieve_project(_id)

        # truy xuất thông tin project đã duplicated
        resp_retrieve_dupicate = self.retrieve_project(_id_dupt)

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp_retrieve_project['metadata']['codec_name'] == resp_retrieve_dupicate['metadata']['codec_name']
        assert resp_retrieve_project['metadata']['width'] == resp_retrieve_dupicate['metadata']['width']
        assert resp_retrieve_project['metadata']['height'] == resp_retrieve_dupicate['metadata']['height']
        assert resp_retrieve_project['metadata']['r_frame_rate'] == resp_retrieve_dupicate['metadata']['r_frame_rate']
        assert resp_retrieve_project['metadata']['bit_rate'] == resp_retrieve_dupicate['metadata']['bit_rate']
        assert resp_retrieve_project['metadata']['nb_frames'] == resp_retrieve_dupicate['metadata']['nb_frames']
        assert resp_retrieve_project['metadata']['size'] == resp_retrieve_dupicate['metadata']['size']

        print(f'3. checked ok')
                
        # xóa project
        self.delete_project(_id)
        self.delete_project(_id_dupt)
        print(f'4. deleted ok')


