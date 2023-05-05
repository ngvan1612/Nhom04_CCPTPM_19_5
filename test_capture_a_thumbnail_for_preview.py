import pytest
import requests
import json
import random
import time
import binascii
import os
from type import *
class TestEditVideo:
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
    def get_preview_thumbnail(self, project_id) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + '/raw/thumbnails/preview'
        )
        return  resp.content, resp.status_code
    
    @pytest.mark.skip
    def capture_a_thumbnail_for_preview(self, project_id, position_param, crop_param, rotate_param) -> json:
        url = URL_GET_VIDEO + str(project_id) + '/thumbnails?type=preview'
        is_set = False

        
        if crop_param is not None:
            crop_param = crop_param.replace(',', '%2C')
        
        if crop_param is None and rotate_param is None and is_set is False:
            url = url + '&position=' + str(position_param)
            is_set = True
        if crop_param is None and is_set is False:
            url = url + '&position=' + str(position_param) + '&rotate=' + str(rotate_param)
            is_set = True
        elif rotate_param is None and is_set is False:
            url = url + '&position=' + str(position_param) + '&crop=' + str(crop_param)
            is_set = True
        elif is_set is False:
            url = url + '&position=' + str(position_param) + '&crop=' + str(crop_param) + '&rotate=' + str(rotate_param)
        resp = requests.get(url)
        return  json.loads(resp.text), resp.status_code

    def test_01(self):
        """
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Tạo một preview thumbnail từ một project không tồn tại hoặc bị xóa xem có thông báo lỗi hay không
        """
        
        result = binascii.b2a_hex(os.urandom(10))
        _id = result.decode('utf-8')    
        print(_id)    

        resp_project, status_code = self.capture_a_thumbnail_for_preview(_id, 10, '200,100,400,360', -90)
        print(resp_project)
        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

        _id_create = self.create_project('test_data/p-06.mp4')['_id']
        self.delete_project(_id_create)

        resp_project, status_code = self.capture_a_thumbnail_for_preview(_id_create, 10, None, -90)
        assert resp_project['error'] == 'Project with id \''+ _id_create +'\' was not found.'

    def test_02(self):
        """
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Tạo một preview thumbnail đầu tiên với posion nằm ngoài video
            3. Lưu thumbnail đó để so sánh
            4. Tạo một preview thumbnail thứ 2 với posion trong video
            5. So sánh xem 2 thumnail đó có bằng nhau không
        """

        _id_create = self.create_project('test_data/p-06.mp4')['_id']
        print(_id_create)

        while True:
            resp_project_1, status_code = self.capture_a_thumbnail_for_preview(_id_create, 10000000000000, None, None)
            print(resp_project_1)
            print(status_code)
            time.sleep(0.5)
            if status_code == 202:
                break
                
        while True:
            thumbnail_1, status_code = self.get_preview_thumbnail(_id_create)
            time.sleep(0.5)
            if status_code == 200:
                break
    
        while True:
            resp_project_2, status_code2 = self.capture_a_thumbnail_for_preview(_id_create, 246, None, None)
            print(resp_project_2)
            print(status_code2)
            time.sleep(0.5)
            if status_code2 == 202:
                break

        while True:
            thumbnail_2, status_code2 = self.get_preview_thumbnail(_id_create)
            time.sleep(0.5)
            if status_code2 == 200:
                break

        self.delete_project(_id_create)
        assert thumbnail_1 == thumbnail_2
        

    def test_03(self):
        """
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Tạo một preview thumbnail đầu tiên với tham số hợp lệ
            3. Lưu thumbnail đó để so sánh
            4. Tạo một preview thumbnail thứ 2 với tham số hợp lệ
            5. So sánh xem 2 thumnail đó có khác nhau không
        """

        _id_create = self.create_project('test_data/p-01.mp4')['_id']
        print(_id_create)

        while True:
            resp_project_1, status_code = self.capture_a_thumbnail_for_preview(_id_create, 10, None, -180)
            print(resp_project_1)
            print(status_code)
            time.sleep(0.5)
            if status_code == 202:
                break
        
        while True:
            thumbnail_1, status_code = self.get_preview_thumbnail(_id_create)
            time.sleep(0.5)
            if status_code == 200:
                break

        while True:
            resp_project_2, status_code2 = self.capture_a_thumbnail_for_preview(_id_create, 11, '200,100,400,360', None)
            print(resp_project_2)
            print(status_code2)
            time.sleep(0.5)
            if status_code2 == 202:
                break
        
        while True:
            thumbnail_2, status_code2 = self.get_preview_thumbnail(_id_create)
            time.sleep(0.5)
            if status_code2 == 200:
                break

        self.delete_project(_id_create)
        # assert thumbnail_1 != thumbnail_2
        

    def test_04(self):
        '''
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-06.mp4`
            2. Chuẩn bị 1 thumbnail để so sánh
            3. Tạo một preview thumbnail với tham số hợp lệ
            4. So sánh xem 2 thmbnail đó có giống nhau không
        '''

        resp = self.create_project('test_data/p-06.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        while True:
            resp_project_1, status_code = self.capture_a_thumbnail_for_preview(_id_create, 10, '200,100,400,360', -180)
            print(resp_project_1)
            print(status_code)
            time.sleep(0.5)
            if status_code == 202:
                break
        
        while True:
            thumbnail_1, status_code = self.get_preview_thumbnail(_id_create)
            time.sleep(0.5)
            if status_code == 200:
                break
        
        self.delete_project(_id_create)

        with open('test_data/thumbnail-01.jpg', 'rb') as f:
            thumbnail_2 = f.read()

        assert thumbnail_1 == thumbnail_2

    def test_05(self):
        '''
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-01.mp4`
            2. Tạo một preview thumbnail với tham số rotate không hợp lệ
            4. Tạo một preview thumbnail với tham số crop không hợp lệ
            5. Xem thử có thông báo lỗi hay không
        '''
        resp = self.create_project('test_data/p-02.mp4')
        _id_create = resp['_id']
        print(f'1. created {_id_create}')

        rotate = -120
        
        resp_project_1, status_code = self.capture_a_thumbnail_for_preview(_id_create, 10, None, rotate)
        print(resp_project_1)
        resp_project_2 , status_code = self.capture_a_thumbnail_for_preview(_id_create, 10, '200000,100,400,360', None)
        print(resp_project_2)
        
        self.delete_project(_id_create)
        assert resp_project_1['rotate'] == ['unallowed value ' + str(rotate)]
        assert resp_project_2['crop'] == ['x is less than minimum allowed crop width']



        

    