import unittest

from cache_app import cache_util
from cache_app import models

from django.core.cache import cache

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
        sleep 20 seconds
        get_result - nothing changed, it will take less then 1 second
        sleep 30 seconds
        get_result - cache expired, it will take about 5 seconds
        """
        # clean current cache
        cache.clear()

        # cache for 40 seconds
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > 4)

        # sleep and check the cache
        time.sleep(20)

        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s < 1)

        # sleep and cache again
        time.sleep(30)
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > 4)

    def test_common_data_changed(self):
        """
        get_result - no cache yet, it will take about 5 seconds
        sleep 20 seconds
        # tr_data expired
        change tr_model
        get_result - new tr_data, it will take about 5 seconds
        sleep 30 seconds
        get_result - use the preview cache.
        """
        # clean current cache
        cache.clear()

        # cache for 40 seconds with current tr_data
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > 4)

        # sleep and check the cache
        time.sleep(20)

        # change tr_model
        tr_obj = models.TestRequest.objects.get(pk=1)
        tr_obj.status = 'DONE'
        tr_obj.save()

        # new data cache for other 20 seconds
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > 4)

        # sleep and cache again
        time.sleep(30)
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s < 1)

