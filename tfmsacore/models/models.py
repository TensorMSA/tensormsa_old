from django.db import models


class NNList(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, blank=False, default='')
    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=100, blank=True, default='')
    acc = models.InteagerField(max_length=1, blank=True, default='')
    train = models.InteagerField(max_length=1, blank=True, default='')
    config = models.FloatField(max_length=100, blank=True, default='')
    dir = models.CharField(max_length=200, blank=True, default='')