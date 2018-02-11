import unittest
import time

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


if __name__ == '__main__':
    unittest.main()
