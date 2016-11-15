from django.core.cache import cache

from cache_app import models


def get_testrequest(tr_id):
    return models.TestRequest.objects.get(id=tr_id)
