import os
import requests


class Vk:
    def __init__(self, access_token, v=5.70):
        self.params = {
            'access_token': access_token,
            'v': v
        }
        self.main_url = 'https://api.vk.com/method/'

    def get(self, method, **kwargs):
        url = self.main_url + method
        self.params.update(kwargs)
        try:
            resp = requests.get(url, params=self.params)
        except Exception as e:
            return {'error': {'exception': e}}
        if resp.ok:
            return resp.json()
        else:
            return {'error': {
                'status_code': resp.status_code,
                'reason': resp.reason
                         }
                    }


class Group:
    """
    Class work working with group in vk
    You need group id - owner_id and access_token
    """
    def __init__(self, owner_id, access_token):
        self.id = owner_id
        self.vk = Vk(access_token)
        self.response = None
        self.result = None
        self.count = None
        self.last_postponed_post = None

    def order_size(self):
        """
        :return: postponed order in vk group
        """
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

    def last_postponed(self):
        """
        :return: last postponed post from vk api
        """
        method = 'wall.get'
        count = self.order_size()
        if count:
            self.result = self.vk.get(method,
                                      count=1,
                                      filter='postponed',
                                      offset=count-1,
                                      owner_id=self.id)
            self.response = self.result.get('response', None)
            if self.response:
                self.last_postponed_post = self.response.get('items', None)
            return self.last_postponed_post


class UploadFile:
    def __init__(self, _type, file, access_token, owner_id):
        self.type = _type
        self.file = file
        self.vk = Vk(access_token)
        self.id = owner_id

    def upload_doc(self):
        method = 'docs.getUploadServer'
        self.result = self.vk.get(method,
                                  owner_id=self.id)
        self.response = self.result.get('response', None)
        if self.response:
            upload_url = self.response.get('upload_url', None)
            file_name = os.path.basename(self.file)
            file_up = {'file': (file_name, open(self.file, 'rb'))}
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
                    return 'doc' + str(owner_id) + '_' + str(_id)
    def upload(self):
        if self.type == 'doc':
            return self.upload_doc()
