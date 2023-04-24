import pytest
import requests
import json
import random
import time
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
                "scale": 1000
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

# getVideoEdit01()
# getVideoEdit02()
# getVideoEdit03()
# getVideoEdit04()