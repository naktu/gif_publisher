import requests


class Vk:
    def __init__(self, access_token, v=5.63):
        self.params = {
            'access_token': access_token,
            'v': v
        }
        self.url = 'https://api.vk.com/method/'

    def get(self, method, **kwargs):
        self.url += method
        self.params.update(kwargs)
        print(self.params)
        return requests.get(self.url, params=self.params).json()


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
