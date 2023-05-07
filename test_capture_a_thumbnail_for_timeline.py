import pytest
import requests
import json
import random
import time
import binascii
import os
from type import *
import cv2
from base_test import TestBase

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
    def get_project_thumbnails(self, project_id):
        resp = requests.get(URL_LIST_PROJECTS + project_id)
        assert resp.status_code == 200
        j = json.loads(resp.text)
        return j['thumbnails']
    
    @pytest.mark.skip
    def waiting_for_processing(self, project_id):
        while True:
            resp = requests.get(URL_LIST_PROJECTS + project_id)
            assert resp.status_code == 200
            j = json.loads(resp.text)
            processing = j['processing']
            is_processing = False
            is_processing = is_processing or processing['video']
            is_processing = is_processing or processing['thumbnail_preview']
            is_processing = is_processing or processing['thumbnails_timeline']

            if not is_processing:
                break

            time.sleep(0.25)
            print('Waiting for ...', project_id, time.time())

    @pytest.mark.skip
    def get_video(self, project_id) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + '/raw/video'
        )
        return  resp.content, resp.status_code
    
    @pytest.mark.skip
    def get_timeline_thumbnail(self, project_id, index) -> json:
        resp = requests.get(
            URL_GET_VIDEO + str(project_id) + f'/raw/thumbnails/timeline/{index}'
        )
        return  resp.content, resp.status_code
    
    @pytest.mark.skip
    def capture_a_thumbnail_for_timeline(self, project_id, amount) -> json:
        url = URL_GET_VIDEO + str(project_id) + f'/thumbnails?type=timeline&amount={amount}'

        resp = requests.get(url)
        return  json.loads(resp.text), resp.status_code
    
    @pytest.mark.skip
    def get_cv_image_from_stream(self, stream):
        result = None
        try:
            with open("temp.jpg", 'wb') as f:
                f.write(stream)
            result = cv2.imread('./temp.jpg')
        except Exception as e:
            print(e)
        finally:
            if os.path.exists('temp.jpg'):
                os.remove('temp.jpg')
        return result

    def test_01(self):
        """
            `Test activity diagram: CAPTURE A THUMBNAIL FOR TIMELINE`
            1. Tạo một project upload video tên là `p-07.mp4`
            2. Tạo một timeline thumbnail từ một project không tồn tại hoặc bị xóa xem có thông báo lỗi hay không
        """
        
        result = binascii.b2a_hex(os.urandom(10))
        _id = result.decode('utf-8')    
        print(_id)    

        resp_project, status_code = self.capture_a_thumbnail_for_timeline(_id, 1)
        print(resp_project)
        assert resp_project['error'] == 'Project with id \''+ _id +'\' was not found.'

        _id_create = self.create_project('test_data/p-07.mp4')['_id']
        self.delete_project(_id_create)

        resp_project, status_code = self.capture_a_thumbnail_for_timeline(_id_create, 1)
        assert resp_project['error'] == 'Project with id \''+ _id_create +'\' was not found.'

    def test_02(self):
        """
            `Test activity diagram: CAPTURE A THUMBNAIL FOR TIME LINE`
            1. Tạo một project upload video tên là `p-07.mp4`
            2. Tạo một timeline thumbnail với thông số amount = 1 và kiểm tra thông số đầu ra
        """
        self.delete_all_projects()

        _id_create = self.create_project('test_data/p-07.mp4')['_id']
        self.waiting_for_processing(_id_create)

        resp_project, status_code = self.capture_a_thumbnail_for_timeline(_id_create, 1)
        self.waiting_for_processing(_id_create)

        thumbnails = self.get_project_thumbnails(_id_create)

        timelines = thumbnails['timeline']

        assert len(timelines) == 1

        timeline = timelines[0]

        assert timeline['width'] == 89
        assert timeline['height'] == 50
        assert timeline['mimetype'] == 'image/png'

        self.delete_project(_id_create)
        

    def test_03(self):
        """
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-04.mp4`
            2. Tạo một project khác cũng với video ở trên
            3. Tạo 2 cái thumb_nail
            4. Kiểm tra 2 thumb_nail giống nhau không
        """

        def create_timeline_thumb(file_name):  
            _id_create = self.create_project(file_name)['_id']
            self.waiting_for_processing(_id_create)
            
            self.capture_a_thumbnail_for_timeline(_id_create, 1)
            self.waiting_for_processing(_id_create)

            return self.get_timeline_thumbnail(_id_create, 0)
        
        p1 = create_timeline_thumb('test_data/p-07.mp4')
        p2 = create_timeline_thumb('test_data/p-07.mp4')

        assert p1 == p2

        self.delete_all_projects()

    def test_04(self):
        '''
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-07.mp4`
            2. Chuẩn bị 1 thumbnail để so sánh
            3. Tạo một thumbnail sao đó so khớp với cái ở mục 2
        '''

        self.delete_all_projects()
        resp = self.create_project('test_data/p-07.mp4')
        _id_create = resp['_id']
        
        self.waiting_for_processing(_id_create)

        self.capture_a_thumbnail_for_timeline(_id_create, 1)
        self.waiting_for_processing(_id_create)
        
        p1_buffer, p1_buffer_status_code = self.get_timeline_thumbnail(_id_create, 0)
        p1 = self.get_cv_image_from_stream(p1_buffer)
        
        #self.delete_all_projects()

        p2 = cv2.imread('./test_data/thumbnail-02.jpg')

        print(p1.shape, p2.shape)

        assert (p1 == p2).all()

    def test_05(self):
        '''
            `Test activity diagram: CAPTURE A THUMBNAIL FOR PREVIEW`
            1. Tạo một project upload video tên là `p-07.mp4`
            2. Tạo thử 100 thumbnail và kiểm tra toàn bộ kích thông số thumnail xem có giống nhau không?
        '''

        self.delete_all_projects()
        resp = self.create_project('test_data/p-07.mp4')
        _id_create = resp['_id']
        self.waiting_for_processing(_id_create)

        self.capture_a_thumbnail_for_timeline(_id_create, 100)
        self.waiting_for_processing(_id_create)

        thumbnails = self.get_project_thumbnails(_id_create)

        timelines = thumbnails['timeline']

        assert len(timelines) == 100

        self.delete_all_projects()

        for timeline in timelines:
            assert timeline['width'] == timelines[0]['width']
            assert timeline['height'] == timelines[0]['height']
            assert timeline['mimetype'] == timelines[0]['mimetype']


        

    