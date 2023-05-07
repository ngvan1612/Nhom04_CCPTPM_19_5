import requests
import json
from type import *
import pytest
import random
from base_test import TestBase

class TestCreateProject(TestBase):

    _ids = []

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
        resp = self.create_project('test_data/p-02.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp['metadata']['codec_name'] == 'h264'
        assert resp['metadata']['width'] == 480
        assert resp['metadata']['height'] == 658
        assert resp['metadata']['r_frame_rate'] == '5/1'
        assert resp['metadata']['bit_rate'] == 1223672
        assert resp['metadata']['nb_frames'] == 12
        assert abs(resp['metadata']['duration'] - 2.2) <= 1e-3
        assert resp['metadata']['size'] == 337454

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')
    
    def test_03(self):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-03.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-03.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp['metadata']['codec_name'] == 'h264'
        assert resp['metadata']['width'] == 480
        assert resp['metadata']['height'] == 618
        assert resp['metadata']['r_frame_rate'] == '10/1'
        assert resp['metadata']['bit_rate'] == 1058518
        assert resp['metadata']['nb_frames'] == 24
        assert abs(resp['metadata']['duration'] - 2.300977) <= 1e-3
        assert resp['metadata']['size'] == 305414

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')

    def test_04(self):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-04.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-04.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp['metadata']['codec_name'] == 'h264'
        assert resp['metadata']['width'] == 372
        assert resp['metadata']['height'] == 480
        assert resp['metadata']['r_frame_rate'] == '133/12'
        assert resp['metadata']['bit_rate'] == 670481
        assert resp['metadata']['nb_frames'] == 24
        assert abs(resp['metadata']['duration'] - 2.07601) <= 1e-3
        assert resp['metadata']['size'] == 174945

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')

    def test_05(self):
        """
            `Test activity diagram: CREATE PROJECT`
            1. Tạo một project upload video tên là `p-05.mp4`
            2. Kiểm tra thông tin project
            3. Xóa project
        """
        # tạo project
        resp = self.create_project('test_data/p-05.mp4')
        _id = resp['_id']
        print(f'1. created {_id}')

        # kiểm tra thông tin khớp với p-01.mp4
        assert resp['metadata']['codec_name'] == 'h264'
        assert resp['metadata']['width'] == 480
        assert resp['metadata']['height'] == 574
        assert resp['metadata']['r_frame_rate'] == '31/4'
        assert resp['metadata']['bit_rate'] == 1459549
        assert resp['metadata']['nb_frames'] == 13
        assert abs(resp['metadata']['duration'] - 1.549017) <= 1e-3
        assert resp['metadata']['size'] == 283460

        print(f'2. checked ok')
                
        # xóa project
        self.delete_project(_id)
        print(f'3. deleted ok')
