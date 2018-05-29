import unittest
import time
import os
import requests


from gifs.utils import vk
from tests.utils.secret import API


class TestVK(unittest.TestCase):
    def setUp(self):
        self.vk_instance = vk.Vk(API)

    def test_get_valid(self):
        result = self.vk_instance.get(method='wall.get',
                                      owner_id=-96920344,
                                      count=1,
                                      )
        item = result['response']['items'][0]
        self.assertIsInstance(item, dict)

    def test_get_no_valid(self):
        self.vk_instance.main_url = 'https://vk.com/method/'
        result = self.vk_instance.get(method='wall.get',
                                      owner_id=-96920344,
                                      count=1,
                                      )
        item = result['error']
        self.assertSetEqual(set(item.keys()),
                            {'status_code', 'reason'})

    def test_no_valid_method(self):
        result = self.vk_instance.get(method='wrong.method',
                                      owner_id=-96920344)
        item = result['error']
        self.assertIsInstance(item, dict)

    def test_exception(self):
        self.vk_instance.main_url = 'http://vkdfjggscbbcxomdghls.com/method/'
        result = self.vk_instance.get(method='123')
        item = result['error']
        self.assertSetEqual(set(item.keys()), {'exception'})

    def tearDown(self):
        # Sleep after each test because vk can ban us
        time.sleep(10)


class TestGroup(unittest.TestCase):
    def setUp(self):
        # In this group last post in 1 december 2018 01:00
        self.gr = vk.Group(-103991042, API)

    def test_order_size_one_post(self):
        self.assertEqual(self.gr.order_size(), 1)

    def test_last_postponed_one_post(self):
        result = self.gr.last_postponed()
        self.assertIsInstance(result[0], dict)

    def test_last_postponed_no_posts_in_order(self):
        self.gr.id = -101004674
        self.assertIs(self.gr.last_postponed(), None)

    def tearDown(self):
        # Sleep after each test because vk can ban us
        time.sleep(10)


class TestUploadFile(unittest.TestCase):
    """b'{"error":{"error_code":14,"error_msg":"Captcha needed","request_params":[{"key":"oauth","value":"1"},{"key":"method","value":"docs.save"},{"key":"v","value":"5.7"},{"key":"owner_id","value":"-96920344"},{"key":"file","value":"196976591|0|0|834701|62df765718|gif|1273177|Ya9vttumblr_p1u99qA2x31qztgoio3_540.gif|05671f1ee2b0245bb1e2a4476477eded|cbae1e3d0c7a1163ff68e6c37911278a|m_62df765718|32|m:130x73,s:100x56,x:604x337,o:540x301|eyJkaXNrIjoiNyJ9"}],"captcha_sid":"989627655576","captcha_img":"https:\\/\\/api.vk.com\\/captcha.php?sid=989627655576&s=1"}}'"""

    def setUp(self):
        file = 'VPl8itumblr_oz754hAKrZ1ukwfs9o1_1280.gif'
        test_path = os.path.dirname(os.path.abspath(__file__))
        upload_file = os.path.join(test_path, 'files', file)
        self.uf = vk.UploadFile(_type='doc',
                                file=upload_file,
                                access_token=API,
                                owner_id=-148142803
                                )
        with open(upload_file, 'rb') as f:
            self.binary_file = f.read()

    def test_upload_doc(self):
        file = self.uf.upload_doc()
        vk_instance = vk.Vk(API)
        result = vk_instance.get(method='docs.getById',
                                 docs=file[3:]
                                 )
        print(file)
        file_to_down = result['response'][0]['url']
        download = requests.get(file_to_down).content
        self.assertEqual(self.binary_file, download)


if __name__ == '__main__':
    unittest.main()
