import hashlib
import time

from django.core.cache import cache

from cache_app import models



#get the cache key for storage
def cache_get_key(*args, **kwargs):
    serialise = []
    for arg in args:
        serialise.append(str(arg))
    for key,arg in kwargs.items():
        serialise.append(str(key))
        serialise.append(str(arg))
    key = hashlib.md5("".join(serialise)).hexdigest()
    return key


#decorator for caching functions
def cache_for(time):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            key = cache_get_key(fn.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result:
                result = fn(*args, **kwargs)
                cache.set(key, result, time)
            return result
        return wrapper
    return decorator


#decorator for caching functions
def cache_result(time):
    def decorator(fn):
        def wrapper(*args, **kwargs):

            testrequest_hash = get_hash_testrequest_status(args[0])
            key = cache_get_key(fn.__name__, *args, **kwargs)

            result = cache.get(testrequest_hash + key)
            if not result:
                result = fn(*args, **kwargs)
                cache.set(testrequest_hash + key, result, time)
            return result
        return wrapper
    return decorator


def get_testrequest(tr_id):
    return models.TestRequest.objects.get(id=tr_id)


@cache_for(60)
def get_testrequest_cache(tr_id):
    return models.TestRequest.objects.get(id=tr_id)


def get_hash_testrequest_status(tr_id):
    tr_obj = get_testrequest_cache(tr_id)
    serialise = ["my_private_cache", str(tr_obj.id), tr_obj.status, tr_obj.description]
    key = hashlib.md5("".join(serialise)).hexdigest()
    return key


def get_result(tr_id):
    time.sleep(5)
    result = {}
    tr = get_testrequest(tr_id)
    result = {'tr_id': tr.id,
              'tr_status': tr.status,
              'tr_description': tr.description,
              'task_test_case': ['some', 'values'],
              }
    return result


@cache_result(180)
def get_result_cache(tr_id):
    time.sleep(5)
    result = {}
    tr = get_testrequest_cache(tr_id)
    result = {'tr_id': tr.id,
              'tr_status': tr.status,
              'tr_description': tr.description,
              'task_test_case': ['some', 'values'],
              }
    return result
