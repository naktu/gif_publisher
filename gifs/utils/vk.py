import os
import base64
import time
import requests


class Vk:
    def __init__(self, access_token, anti_c_key, v=5.70):
        self.params = {
            'access_token': access_token,
            'v': v
        }
        self.main_url = 'https://api.vk.com/method/'
        self.anti_captcha_key = anti_c_key

    def get(self, method, **kwargs):
        while True:
            url = self.main_url + method
            self.params.update(kwargs)
            try:
                resp = requests.get(url, params=self.params)
            except Exception as e:
                return {'error': {'exception': e}}
            if resp.ok:
                if 'error' in resp.json():
                    if resp.json()['error']['error_code'] == 14:
                        print("Captcha needed")
                        url_cap = resp.json()['error']['captcha_img']
                        print(url_cap)
                        r = requests.get(url_cap)
                        with open('captcha.jpg', 'wb') as f:
                            f.write(r.content)

                        with open('captcha.jpg', 'rb') as f:
                            base_str = base64.b64encode(f.read())

                        bs = base_str.decode('utf-8')
                        params_cap = {
                            "clientKey": anti,
                            "task": {
                                "type": "ImageToTextTask",
                                "body": bs,
                            }
                        }

                        r = requests.post("http://api.anti-captcha.com/createTask", json=params_cap)
                        print(r.json())
                        while True:
                            print('waiting for captha 30 seconds')
                            time.sleep(30)
                            task_id = r.json()['taskId']
                            params_cap = {
                                "clientKey": self.anti_captcha_key,
                                "taskId": task_id
                            }
                            r = requests.post("https://api.anti-captcha.com/getTaskResult", json=params_cap)
                            print(r.json())
                            if r.json()['status'] == 'ready':
                                break

                        self.params['captcha_sid'] = resp.json()['error']['captcha_sid']
                        self.params['captcha_key'] = r.json()['solution']['text']
                        continue
                print(resp.content)
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

    def post(self, **kwargs):
        """
        :return: post
        """
        method = 'wall.post'
        kwargs.setdefault('owner_id', self.id)
        self.result = self.vk.get(method=method, **kwargs)
        return self.result


class UploadFile:
    def __init__(self, _type, file, access_token, owner_id):
        self.type = _type
        self.file = file
        self.vk = Vk(access_token)
        self.id = owner_id
        self.type = None
        self.response = None
        self.result = None

    def upload_doc(self):
        method = 'docs.getUploadServer'
        self.result = self.vk.get(method,
                                  owner_id=self.id)
        self.response = self.result.get('response', None)
        if self.response:
            upload_url = self.response['upload_url']
            file_name = os.path.basename(self.file)
            file_up = {'file': (file_name, open(self.file, 'rb'))}
            print(self.file)
            uploaded = requests.post(upload_url, files=file_up)
            if uploaded.ok:

                method = 'docs.save'
                response = uploaded.json()
                print(response)
                if 'error' in response.keys():
                    print(response['file'])
                    exit(1)
                self.result = self.vk.get(method,
                                          owner_id=self.id,
                                          file=uploaded.json()['file'])

                self.response = self.result['response']
                print(self.response)
                if self.response:
                    owner_id = self.response[0]['owner_id']
                    _id = self.response[0]['id']
                    return 'doc' + str(owner_id) + '_' + str(_id)

    def upload(self):
        if self.type == 'doc':
            return self.upload_doc()
