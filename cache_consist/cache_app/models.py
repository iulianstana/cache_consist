from django.db import models

# Create your models here.

class TestRequest(models.Model):
    status = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

