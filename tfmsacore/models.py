from django.db import models


class NNList(models.Model):
    id = models.CharField(max_length=10, blank=False, primary_key=True)          # unique key name (nn00000001)
    category = models.CharField(max_length=10, blank=False, primary_key=True)    # business category
    name = models.CharField(max_length=100, blank=True, default='')              # business name
    type = models.CharField(max_length=100, blank=True, default='')              # network types
    acc = models.FloatField(max_length=5, blank=True, default='')                # accuracy of model from last training
    train = models.CharField(max_length=1, blank=True, default='')           # if trained model exist
    config = models.CharField(max_length=1, blank=True, default='')          # if config exist
    dir = models.CharField(max_length=200, blank=True, default='')               # path where conf files saved
    created = models.DateTimeField(auto_now_add=True)                            # day created