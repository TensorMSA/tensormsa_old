from tfmsacore.data.hdfs_manager import HDFSManager
from tfmsacore.data.hive_manager import HiveManager
from tfmsacore.data.locfile_manager import LocalFileManager
from tfmsacore.data.aws_s3_manager import S3Manager
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
from TensorMSA import const


def DataMaster():
    """
    CODE 1 : HDFS direct
    CODE 2 : HIVE plugin
    CDOE 3 : AWS S3
    CODE 4 : LOCAL FILE SYSTEM
    """

    if(settings.DATA_STORE_MODE  == const.DATA_STORE_TYPE_HDFS):
        return HDFSManager()
    elif(settings.DATA_STORE_MODE  == const.DATA_STORE_TYPE_HIVE):
        return HiveManager()
    elif (settings.DATA_STORE_MODE == const.DATA_STORE_TYPE_S3):
        return S3Manager()
    elif (settings.DATA_STORE_MODE == const.DATA_STORE_TYPE_LOCAL):
        return LocalFileManager()
    else :
        tfmsa_logger("not supported data store type")
        raise Exception ("not supported data store type")
