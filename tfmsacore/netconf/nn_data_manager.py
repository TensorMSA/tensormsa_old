from hdfs import Config
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
from pyspark.streaming import StreamingContext
from pyspark import SparkContext, SparkConf
from tfmsacore.utils.logger import tfmsa_logger
from pyspark.sql import SQLContext
from django.conf import settings
import pandas as pd

def hdfs_chk(self, root, nn_id):
    """
    check if nn_id exist
    :param category: business category
    :param subcate: business subcategory
    :param nn_id: nerual network id
    :return:
    """
    try:
        if (self.client.content("/{0}/{1}".format(root, nn_id), strict=False) == None):
            return True
        else:
            return False

    except Exception as e:
        tfmsa_logger("Error : {0}".format(e))
        raise Exception(e)


def hdfs_put(self, root, nn_id, records):
    """
    manage configration data
    :param category: business category
    :param subcate: business subcategory
    :param nn_id: nerual network id
    :return:
    """
    try:
        self.client.write("/{0}/{1}".format(root, nn_id), data=records, encoding='utf-8')
    except Exception as e:
        tfmsa_logger("Error : {0}".format(e))
        raise Exception(e)


def hdfs_del(self, root, nn_id):
    """
    manage configration data
    :param category: business category
    :param subcate: business subcategory
    :param nn_id: nerual network id
    :return:
    """
    try:
        self.client.delete("/{0}/{1}".format(root, nn_id), recursive=False)
    except Exception as e:
        tfmsa_logger("Error : {0}".format(e))
        raise Exception(e)


def hdfs_get(self, root, nn_id):
    """
    manage configration data
    :param category: business category
    :param subcate: business subcategory
    :param nn_id: nerual network id
    :return:
    """
    try:
        return self.client.read("/{0}/{1}".format(root, nn_id))
    except Exception as e:
        tfmsa_logger("Error : {0}".format(e))
        raise Exception(e)

