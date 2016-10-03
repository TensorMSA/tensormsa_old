# -*- coding: utf-8 -*-
import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from tfmsacore import utils
from django.conf import settings

def save_csv_to_df(data_frame, table_name, csv_file):
    """
    json type data loader
    :param net_id:
    :return:
    """
    try:
        conf = SparkConf()
        conf.setMaster('spark://{0}'.format(settings.SPARK_HOST))
        conf.setAppName('save_csv_to_df')
        conf.set('spark.driver.cores', settings.SPARK_CORE)
        conf.set('spark.driver.memory', settings.MEMORY)
        sc = SparkContext(conf=conf)
        sqlContext = SQLContext(sc)

        df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='false').load(csv_file)
        df.write.parquet("hdfs://{0}/{1}/{2}/{3}".format(settings.HDFS_HOST, settings.HDFS_DF_ROOT , \
                                                                   data_frame, table_name), mode="append", partitionBy=None)

    except Exception as e:
        utils.tfmsa_logger(e)
        raise Exception (e)



