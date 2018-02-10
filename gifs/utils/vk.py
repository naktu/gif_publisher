import os
import requests


class Vk:
    def __init__(self, access_token, v=5.63):
        self.params = {
            'access_token': access_token,
            'v': v
        }
        self.main_url = 'https://api.vk.com/method/'

    def get(self, method, **kwargs):
        url = self.main_url + method
        self.params.update(kwargs)
        resp = requests.get(url, params=self.params)
        if resp.ok:
            return resp.json()
        else:
            return {'error': {
                'status_code': resp.status_code,
                'reason': resp.reason
                         }
                    }


class Group:
    def __init__(self, owner_id, access_token):
        self.id = owner_id
        self.vk = Vk(access_token)
        self.response = None
        self.result = None
        self.count = None
        self.last_postponed = None

    def count_order_post(self):
        method = 'wall.get'
        self.result = self.vk.get(method,
                                  count=1,
                                  filter='postponed',
                                  owner_id=self.id
                                  )
        self.response = self.result.get('response', None)
        if self.response:
            self.count = self.response.get('count', None)
        return self.count

    def last_post_in_order(self):
        method = 'wall.get'
        count = self.count_order_post()
        if count:
            self.result = self.vk.get(method,
                                      count=1,
                                      filter='postponed',
                                      offset=count-1,
                                      owner_id=self.id)
            self.response = self.result.get('response', None)
            if self.response:
                self.last_postponed = self.response.get('items', None)
            return self.last_postponed

    def upload_doc(self, file):
        method = 'docs.getUploadServer'
        self.result = self.vk.get(method,
                                  owner_id=self.id)
        self.response = self.result.get('response', None)
        if self.response:
            upload_url = self.response.get('upload_url', None)
            file_up = {'file': (os.path.basename(file), open(file, 'rb'))}
            uploaded = requests.post(upload_url, files=file_up)
            if uploaded.ok:
                method = 'docs.save'
                self.result = self.vk.get(method,
                                          owner_id=self.id,
                                          file=uploaded.json()['file'])
                self.response = self.result.get('response', None)
                if self.response:
                    owner_id = self.response[0]['owner_id']
                    _id = self.response[0]['id']
                    return 'doc' + str(owner_id) + str(_id)
