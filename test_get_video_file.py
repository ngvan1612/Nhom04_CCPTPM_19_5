import hashlib
import pytest
import requests
import json
import random
import binascii
import os
import time
from base_test import TestBase 
from type import *
# from hash_video import *

class TestGetVideoFile(TestBase):

    @pytest.mark.skip
    def upload_project(self, path):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project(path)
        _id = resp['_id']
        print(f'1. created {_id}')
                
        # không xóa project
        #self.delete_project(_id)
        #print(f'3. deleted ok')
    
    @pytest.mark.skip
    def retrieve_project(self, project_id) -> json:
        resp = requests.get(
            URL_RETRIEVE_PROJECT + str(project_id)
        )
        return json.loads(resp.text)
    
    @pytest.mark.skip
    def get_video(self, project_id) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + '/raw/video'
        )
        return  resp.content, resp.status_code
    @pytest.mark.skip
    def delete_project(self, project_id):
        resp = requests.delete(URL_DELETE_PROJECT + str(project_id))
        if resp.status_code == 204:
            return True
        else:
            return json.loads(resp.text)
    @pytest.mark.skip
    def test_01(self):
        """
            `Test activity diagram: GET VIDEO FILE`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Download video vua upload
            3. Kiem tra ma hash cua video upload va download
        """
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        
        while (True):
            video, status_code = self.get_video(_id)
            time.sleep(0.5)
            if status_code == 200:
                break
        
        with open('test_data/p-01.mp4', 'rb') as file:
            video2 = file.read()
        video_hash = hashlib.sha256(video).hexdigest()
        video_samp = hashlib.sha256(video2).hexdigest()


        assert video_hash == video_samp
        
        self.delete_project(_id)
        print(f'3. deleted ok')
    @pytest.mark.skip
    def test_02(self):
        """
            `Test activity diagram: GET VIDEO FILE`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Get Byte cua video upload trong mot pham vi cho phep cua video
            3. Kiem tra do dai cua video ta vua get
        """
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        first_bytes = 0 
        last_bytes = 9999
        resp = requests.get(URL_GET_VIDEO+_id + 'raw/video', headers={"Range":"bytes="+f'{first_bytes}'+ "-" + f'{last_bytes}'}) 
        json.loads(resp.text)

        assert resp['Content-Length'] == (f'{last_bytes+1}')

    @pytest.mark.skip
    def test_03(self):
        """
            `Test activity diagram: GET VIDEO FILE`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Get Byte cua video upload ngoai pham vi cho phep cua video
            3. Kiem tra loi duoc tra ve
        """
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']

        get_bytes = 100000000

        resp = requests.get(URL_GET_VIDEO+_id + 'raw/video', headers={"Range":"bytes="+f'{get_bytes}'}) 
        resp = self.retrieve_project(_id)

        assert resp['error'] == "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    @pytest.mark.skip
    def test_04(self):
        """
            `Test activity diagram: GET VIDEO FILE`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Get video co id khong ton tai trong he thong
            3. Kiem tra loi duoc tra ve
        """
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']

        result = binascii.b2a_hex(os.urandom(10))
        _id_random = result.decode('utf-8')
        while(_id == _id_random):
            result = binascii.b2a_hex(os.urandom(10))
            _id_random = result.decode('utf-8')

        resp_getVideo = requests.get(URL_GET_VIDEO + _id_random + 'raw/video')
        resp_getVideo = self.retrieve_project(_id_random)
        assert resp_getVideo['error'] == 'Project with id \''+ _id_random +'\' was not found.'
    @pytest.mark.skip
    def test_05(self):
        """
            `Test activity diagram: GET VIDEO FILE`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Xoa video
            3. Get video co id vua xoa
            4. Kiem tra loi tra ve
        """
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']

        self.delete_project(_id)

        resp_getVideo = requests.get(URL_GET_VIDEO + _id + 'raw/video')
        resp_getVideo = self.retrieve_project(_id)
        assert resp_getVideo['error'] == 'Project with id \''+ _id +'\' was not found.'
