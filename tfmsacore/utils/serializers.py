from rest_framework import serializers

from tfmsacore import models


class NNInfoSerializer(serializers.ModelSerializer):
    """
    Table : store Neural Network base information
    """
    class Meta:
        model = models.NNInfo
        fields = ('nn_id', 'category', 'subcate', 'name', 'desc', 'type', 'acc', 'train', 'config', 'dir', 'table',
                  'query', 'preprocess', 'datadesc', 'datasets', 'imagex', 'imagey', 'imagepre', 'datavaild',
                  'confvaild', 'samplepercent', 'samplenum', 'samplemethod', 'testpass', 'testfail'  )



class JobManagementSerializer(serializers.ModelSerializer):
    """
    Table : Train Job Tracker
    """
    class Meta:
        model = models.JobManagement
        fields = ('nn_id', 'type','request', 'start', 'end', 'status', 'progress', 'acc', 'epoch', 'testsets')



class ServerConfSerializer(serializers.ModelSerializer):
    """
    Table : TensorMSA config data
    """
    class Meta:
        model = models.ServerConf
        fields = ('version', 'state', 'store_type', 'fw_capa', 'livy_host', 'livy_sess', 'spark_host', 'spark_core',
                  'spark_memory', 'hdfs_host', 'hdfs_root', 's3_host', 's3_access', 's3_sess', 's3_bucket')


class TrainResultsSerializer(serializers.ModelSerializer):
    """
    Table : TensorMSA config data
    """
    class Meta:
        model = models.TrainResults
        fields = ('nn_id', 'loss', 'step', 'max_step', 'trainDate', 'testsets')

