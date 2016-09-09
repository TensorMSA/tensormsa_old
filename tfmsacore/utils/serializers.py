from rest_framework import serializers

from tfmsacore import models


class NNInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NNInfo
        fields = ('nnid', 'category', 'name', 'type', 'acc', 'train', 'config', 'dir')
