import unittest

from cache_app import cache_util
from cache_app import models

import time


class TestCache(unittest.TestCase):
    def setUp(self):
        tr = models.TestRequest()
        tr.status = 'BUSY'
        tr.description = 'Something new'
        tr.votes = 10
        tr.save()

    def test_consistent_data(self):
        """
        get_result - no cache yet, it will take about 5 seconds
        sleep 100 seconds
        get_result - nothing changed, it will take less then 1 second
        sleep 100 seconds
        get_result - cache expired, it will take about 5 seconds
        """
        # cache for 180 seconds
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > 4)

        # sleep and check the cache
        time.sleep(100)

        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s < 1)

        # sleep and cache again
        time.sleep(100)
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > 4)

