import pytest
import requests
import json
import random
import binascii
import os
from type import *

class TestGetVideoFile:
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
    
    def test_01(self):
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        resp = requests.get(URL_GET_VIDEO+ _id + 'raw/video')
        
        with open('D:\\test.mp4', 'wb') as f:
            f.write(resp.content)

        # assert resp['metadata']['codec_name'] == 'h264'
    @pytest.mark.skip
    def test_02(self):
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        get_bytes = "0-9000"
        resp = requests.get(URL_GET_VIDEO+_id + 'raw/video', headers={"Range":"bytes="+{get_bytes}}) 
        json.loads(resp.text)

        assert resp["Content-Length"] == "9001"
    @pytest.mark.skip
    def test_03(self):
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # truy xuất thông tin project
        resp_project = self.retrieve_project(_id)
        print(resp_project)
        getSize = resp_project['metadata']['size']
        get_bytes = "{getSize} - {getSize + 100}"

        resp = requests.get(URL_GET_VIDEO+_id + 'raw/video', headers={"Range":"bytes={get_bytes}"}) 
        json.loads(resp.text)

        assert resp["Content_Length"] == ""
    @pytest.mark.skip
    def test_04(self):
        resp = self.create_project('test_data/p-01.mp4')
        _id = resp['_id']

        result = binascii.b2a_hex(os.urandom(10))
        _id_random = result.decode('utf-8')
        while(_id == _id_random):
            result = binascii.b2a_hex(os.urandom(10))
            _id_random = result.decode('utf-8')

        resp_getVideo = requests.get(URL_GET_VIDEO + _id_random + 'raw/video')
        json.loads(resp_getVideo.text)
        assert resp_getVideo['error'] == 'Project with id \''+ _id_random +'\' was not found.'
    @pytest.mark.skip
    def test_05(self):
        return
