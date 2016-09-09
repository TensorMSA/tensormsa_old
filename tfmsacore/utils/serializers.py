from rest_framework import serializers

from tfmsacore import models


class NNListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NNList
        fields = ('id', 'category', 'name', 'type', 'acc', 'train', 'config' 'dir')
