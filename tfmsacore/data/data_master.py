from tfmsacore.data.image_manager import ImageManager
from tfmsacore.data.hbase_manager import HbaseManager
from tfmsacore.data.locfile_manager import LocalFileManager
from tfmsacore.data.aws_s3_manager import S3Manager
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
from TensorMSA import const


def DataMaster(type = const.DATA_STORE_TYPE_HBASE):
    """
    type 1 : HBASE : Table Type Data
    type 2 : HDFS : Image Type Data
    """

    if(type  == const.DATA_STORE_TYPE_HBASE):
        return HbaseManager()
    elif(type  == const.DATA_STORE_TYPE_IMAGE):
        return ImageManager()
    elif (type == const.DATA_STORE_TYPE_S3):
        return S3Manager()
    elif (type == const.DATA_STORE_TYPE_LOCAL):
        return LocalFileManager()
    else :
        tfmsa_logger("not supported data store type")
        raise Exception ("not supported data store type")
