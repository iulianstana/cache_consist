import unittest

from cache_app import cache_util
from cache_app import models
from cache_app.cache_util import TESTREQUEST_TIME, SLEEP_TIME, RESULT_TIME

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
        get_result - no cache yet, it will take about SLEEP_TIME seconds
        sleep TESTREQUEST_TIME seconds
        get_result - nothing changed, it will take less then 1 second
        sleep TESTREQUEST_TIME + delta > RESULT_TIME seconds
        get_result - cache expired, it will take about SLEEP_TIME seconds
        """
        # clean current cache
        cache.clear()

        # cache for RESULT_TIME seconds
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > SLEEP_TIME - 1)

        # sleep and check the cache
        time.sleep(TESTREQUEST_TIME)

        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s < 1)

        # sleep and cache again
        time.sleep(TESTREQUEST_TIME + 10)
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > SLEEP_TIME - 1)

    def test_common_data_changed(self):
        """
        get_result - no cache yet, it will take about SLEEP_TIME seconds
        sleep TESTREQUEST_TIME seconds
        # tr_data expired
        change tr_model
        get_result - new tr_data, it will take about SLEEP_TIME seconds
        sleep TESTREQUEST_TIME + delta > RESULT_TIME seconds
        get_result - use the preview cache.
        """
        # clean current cache
        cache.clear()

        # cache for RESULT_TIME seconds with current tr_data
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > SLEEP_TIME - 1)

        # sleep and check the cache
        time.sleep(TESTREQUEST_TIME)

        # change tr_model
        tr_obj = models.TestRequest.objects.get(pk=1)
        tr_obj.status = 'DONE'
        tr_obj.save()

        # new data cache for other TESTREQUEST_TIME seconds
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s > SLEEP_TIME - 1)

        # sleep and cache again
        time.sleep(TESTREQUEST_TIME + 10)
        s = time.time()
        cache_util.get_result_cache(1)
        e = time.time()
        self.assertTrue(e - s < 1)

    def test_testrequest_unknown(self):
        """
        use unknown testrequest id - test to see if it returns None
        """
        # clean current cache
        cache.clear()

        unknown_result = cache_util.get_result_cache(100)

        self.assertEqual(unknown_result, 'nothing here')

