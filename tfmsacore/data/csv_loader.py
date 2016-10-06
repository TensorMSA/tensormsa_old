# -*- coding: utf-8 -*-
import findspark, os
findspark.init()
from pyspark import SparkContext, SparkConf
from tfmsacore import utils
from django.conf import settings
import pandas as pd
from pyspark.sql import SQLContext, DataFrameWriter, DataFrame

def save_csv_to_df(data_frame, table_name, csv_file):
    """
    json type data loader
    :param net_id:
    :return:
    """
    try:
        utils.tfmsa_logger("start uploading csv on Hadoop")
        conf = SparkConf()
        conf.setMaster('spark://{0}'.format(settings.SPARK_HOST))
        conf.setAppName('save_csv_to_df')
        conf.set('spark.driver.cores', settings.SPARK_CORE)
        conf.set('spark.driver.memory', settings.SPARK_MEMORY)
        conf.set("super-csv-2.2.0.jar", "/home/dev/spark/lib/super-csv-2.2.0.jar")
        conf.set("opencsv-2.3.jar", "/home/dev/spark/lib/opencsv-2.3.jar")
        SUBMIT_ARGS = "--packages com.databricks:spark-csv_2.11:1.2.0 pyspark-shell"
        os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS

        sc = SparkContext(conf=conf)
        sqlContext = SQLContext(sc)


        file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" +csv_file
        temp = pd.read_csv(file_path)
        df = sqlContext.createDataFrame(temp)
        #df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='false').load(file_path)
        df.write.parquet("hdfs://{0}/{1}/{2}/{3}".format(settings.HDFS_HOST, settings.HDFS_DF_ROOT , \
                                                                   data_frame, table_name), mode="append", partitionBy=None)
        utils.tfmsa_logger("uploading csv on Hadoop finished")
    except Exception as e:
        utils.tfmsa_logger(e)
        raise Exception (e)



