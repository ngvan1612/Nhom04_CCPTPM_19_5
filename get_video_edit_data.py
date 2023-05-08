import pytest
import requests
import json
import random
import time
import urllib3
from pytube import YouTube
import youtube_dl
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

def getVideoEdit01():
    testProj = TestProject()
    resp = testProj.create_project('test_data/p-01.mp4')
    _id_create = resp['_id']
    print(f'1. created {_id_create}')

    resp_dup = testProj.duplicate_project(_id_create)
    _id_dup = resp_dup['_id']
    print(f'2. duplicated {_id_dup}')

    resp_retrieve = testProj.retrieve_project(_id_dup)
    print(resp_retrieve)

    json_request = {
                "rotate": 270,
                "scale": 800,
                "trim": "5.1,20.5"
                }

    resp_edit = testProj.edit_project(_id_dup, json_request)
    print(resp_edit)
    assert resp_edit['processing'] == True

    while (True):
        resp, status_code = testProj.get_video(_id_dup)
        time.sleep(0.5)
        if status_code == 200:
            break

    resp_retrieve = testProj.retrieve_project(_id_dup)
    print(resp_retrieve)

    resp_project, status_code = testProj.get_video(_id_dup)

    with open('test_data/video-after-edit-01.mp4', 'wb') as f:
        f.write(resp_project)

    testProj.delete_project(_id_create)
    testProj.delete_project(_id_dup)
    print(f'3. deleted ok')

def getVideoEdit02():
    testProj = TestProject()
    resp = testProj.create_project('test_data/p-06.mp4')
    _id_create = resp['_id']
    print(f'1. created {_id_create}')

    resp_dup = testProj.duplicate_project(_id_create)
    _id_dup = resp_dup['_id']
    print(f'2. duplicated {_id_dup}')

    resp_retrieve = testProj.retrieve_project(_id_dup)

    json_request = {
                "crop": "200,300,320,180",
                "rotate": 90,
                "scale": 800,
                "trim": "4.1,100.5"
                }
    json_request2 = {
                "scale": 1000
                }
    json_request3 = {
                "crop": "400,300,320,180"
                }

    i = 0
    print('waiting for processing...', i)
    resp_edit = testProj.edit_project(_id_dup, json_request3)
    assert resp_edit['processing'] == True

    while (True):
        resp, status_code = testProj.get_video(_id_dup)
        time.sleep(0.5)
        i+=1
        print('waiting for processing...', i)
        if status_code == 200:
            break

    resp_project, status_code = testProj.get_video(_id_dup)

    with open('test_data/video-after-edit-04.mp4', 'wb') as f:
        f.write(resp_project)

    testProj.delete_project(_id_create)
    testProj.delete_project(_id_dup)
    print(f'3. deleted ok')

def getVideoEdit03():
    testProj = TestProject()
    resp = testProj.create_project('test_data/p-06.mp4')
    _id_create = resp['_id']
    print(f'1. created {_id_create}')

    resp_dup = testProj.duplicate_project(_id_create)
    _id_dup = resp_dup['_id']
    print(f'2. duplicated {_id_dup}')

    resp_retrieve = testProj.retrieve_project(_id_dup)

    
    json_request = {
                "scale": 5
                }

    i = 0
    print('waiting for processing...', i)
    resp_edit = testProj.edit_project(_id_dup, json_request)

    while (True):
        resp, status_code = testProj.get_video(_id_dup)
        time.sleep(0.5)
        i+=1
        print('waiting for processing...', i)
        if status_code == 200:
            break

    resp_project, status_code = testProj.get_video(_id_dup)

    with open('test_data/video-after-edit-03.mp4', 'wb') as f:
        f.write(resp_project)

    testProj.delete_project(_id_create)
    testProj.delete_project(_id_dup)
    print(f'3. deleted ok')


def getVideoEdit04():
    testProj = TestProject()
    resp = testProj.create_project('test_data/p-06.mp4')
    _id_create = resp['_id']
    print(f'1. created {_id_create}')

    resp_dup = testProj.duplicate_project(_id_create)
    _id_dup = resp_dup['_id']
    print(f'2. duplicated {_id_dup}')

    resp_retrieve = testProj.retrieve_project(_id_dup)

    json_request = {
                "crop": "400,300,320,180"
                }

    i = 0
    print('waiting for processing...', i)
    resp_edit = testProj.edit_project(_id_dup, json_request)
    assert resp_edit['processing'] == True

    while (True):
        resp, status_code = testProj.get_video(_id_dup)
        time.sleep(0.5)
        i+=1
        print('waiting for processing...', i)
        if status_code == 200:
            break

    resp_project, status_code = testProj.get_video(_id_dup)

    with open('test_data/video-after-edit-04.mp4', 'wb') as f:
        f.write(resp_project)

    testProj.delete_project(_id_create)
    testProj.delete_project(_id_dup)
    print(f'3. deleted ok')

def getVideoEdit05():
    url = 'https://www.youtube.com/watch?v=grAZ5VVKnR0'
    path = 'test_data/test_get_video.mp4'

    # yt = YouTube("https://www.youtube.com/shorts/grAZ5VVKnR0")
    # yt = yt.get('mp4', '720p')
    # yt.download('test_data/test_get_video.mp4')

    # video = YouTube(url)
    # video_streams = video.streams
    # print(video_streams)
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=grAZ5VVKnR0'])

def getThumnail_01():
    testProj = TestProject()
    resp = testProj.create_project('test_data/p-06.mp4')
    _id_create = resp['_id']
    print(f'1. created {_id_create}')

    while True:
        resp_project_1, status_code = testProj.capture_a_thumbnail_for_preview(_id_create, 10, '200,100,400,360', -180)
        print(resp_project_1)
        print(status_code)
        time.sleep(0.5)
        if status_code == 202:
            break
    
    while True:
        thumbnail_1, status_code = testProj.get_preview_thumbnail(_id_create)
        time.sleep(0.5)
        if status_code == 200:
            break

    with open('test_data/thumbnail-01.jpg', 'wb') as f:
        f.write(thumbnail_1)

    testProj.delete_project(_id_create)
    print(f'3. deleted ok')

# getVideoEdit01()
# getVideoEdit02()
getVideoEdit03()
# getVideoEdit04()
# getVideoEdit05()
# getThumnail_01()
