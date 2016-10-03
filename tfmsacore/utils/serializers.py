from rest_framework import serializers

from tfmsacore import models


class NNInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NNInfo
        fields = ('nn_id', 'category', 'subcate', 'name', 'desc', 'type', 'acc', 'train', 'config', 'dir', 'table', 'query', 'datadesc', 'datasets' )
