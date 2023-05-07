import pytest
import requests
from type import *
import os
import cv2
import json
from base_test import TestBase


class TestGetThumbnailFile(TestBase):

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
            1. Tạo một project với file là p-07.mp4
            2. Tạo một timeline thumbnail
            3. Chuẩn bị 1 file trên client tương ứng với cái thumbnail
            4. Kiểm tra timeline thumbnail với file ở bước 3
        """
        self.delete_all_projects()

        project_id = self.create_project('test_data/p-07.mp4')['_id']
        self.waiting_for_processing(project_id)

        self.capture_a_thumbnail_for_timeline(project_id, 1)
        self.waiting_for_processing(project_id)

        p1_buffer, _ = self.get_timeline_thumbnail(project_id, 0)
        p1 = self.get_cv_image_from_stream(p1_buffer)

        p2 = cv2.imread('test_data/thumbnail-02.jpg')

        assert (p1 == p2).all()

        self.delete_all_projects()

    def test_02(self):
        """
            1. Tạo một project với file là p-07.mp4
            2. Lấy tạo 10 timeline nhưng lấy timeline thứ 11 xem có bị 404 không?
        """
        self.delete_all_projects()

        project_id = self.create_project('test_data/p-07.mp4')['_id']
        self.waiting_for_processing(project_id)

        self.capture_a_thumbnail_for_timeline(project_id, 10)
        self.waiting_for_processing(project_id)

        _, status_code = self.get_timeline_thumbnail(project_id, 11 - 1)

        assert status_code == 404

        self.delete_all_projects()
    
    def test_03(self):
        """
            1. Tạo một project với file p-01.mp4
            2. Tạo thử 5 timeline
            3. Tạo một project cũng với p-01.mp4
            4. Tạo thử 5 timeline cho project 2
            5. Kiểm tra 5 timeline của 2 project xem có khớp nhau không?
        """

        def create_and_get_timeline(file_name):
            self.delete_all_projects()

            project_id = self.create_project(file_name)['_id']
            self.waiting_for_processing(project_id)

            self.capture_a_thumbnail_for_timeline(project_id, 5)
            self.waiting_for_processing(project_id)

            result = []
            for i in range(0, 5):
                buffer, status_code = self.get_timeline_thumbnail(project_id, i)
                assert status_code == 200
                result.append(self.get_cv_image_from_stream(buffer))

            return result
        
        r1 = create_and_get_timeline('test_data/p-01.mp4')
        r2 = create_and_get_timeline('test_data/p-01.mp4')

        for i in range(0, 5):
            assert (r1[i] == r2[i]).all()

    def test_04(self):
        """
            1. Kiểm tra tạo thumbail từ 1 project không tồn tạ
        """

        result, status_code = self.capture_a_thumbnail_for_timeline('ahihi', 5)
        error = result['error']
        
        assert status_code == 404
        assert error == "Project with id 'ahihi' was not found."


    def test_05(self):
        """
            1. Tạo 1 project với file là p-02.mp4
            2. Xóa project vừa tạo
            3. Tạo thumbnailt từ project vừa bị xóa
        """


        project_id = self.create_project('test_data/p-02.mp4')['_id']
        self.waiting_for_processing(project_id)

        self.delete_project(project_id)
    

        result, status_code = self.capture_a_thumbnail_for_timeline(project_id, 5)
        error = result['error']
        
        assert status_code == 404
        assert error == f"Project with id '{project_id}' was not found."


