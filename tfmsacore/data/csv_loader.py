# -*- coding: utf-8 -*-
from pyspark import SparkContext, SparkConf
from tfmsacore import utils
from tfmsacore.data.hdfs_manager import HadoopManager
from django.conf import settings
import pandas as pd
from pyspark.sql import SQLContext, DataFrameWriter, DataFrame



class CsvLoader:
    def __init__(self):
        conf = SparkConf()
        conf.setMaster('spark://{0}'.format(settings.SPARK_HOST))
        conf.setAppName('save_csv_to_df')
        conf.set('spark.driver.cores', settings.SPARK_CORE)
        conf.set('spark.driver.memory', settings.SPARK_MEMORY)
        conf.set('spark.executor.cores', settings.SPARK_CORE)
        conf.set('spark.executor.memory', settings.SPARK_MEMORY)

        self.sc = SparkContext(conf=conf)

    def save_csv_to_df(self, data_frame, table_name, csv_file):
        """
        create new table with inserted csv data
        :param net_id:
        :return:
        """
        try:
            utils.tfmsa_logger("start uploading csv on Hadoop")
            # clear current exist table
            HadoopManager().delete_table(data_frame, table_name)

            sqlContext = SQLContext(self.sc)

            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            temp = pd.read_csv(file_path)
            df = sqlContext.createDataFrame(temp)
            df.write.parquet("hdfs://{0}/{1}/{2}/{3}".format(settings.HDFS_HOST, settings.HDFS_DF_ROOT , \
                                                                       data_frame, table_name), mode="append", partitionBy=None)
            utils.tfmsa_logger("uploading csv on Hadoop finished")


        except Exception as e:
            utils.tfmsa_logger(e)
            raise Exception (e)
        finally :
            self.sc.stop()


    def update_csv_to_df(self, data_frame, table_name, csv_file):
        """
        append csv data
        :param data_frame:
        :param table_name:
        :param csv_file:
        :return:
        """
        try:
            sqlContext = SQLContext(self.sc)
            df = sqlContext.read.load("hdfs://{0}/{1}/{2}/{3}".format(settings.HDFS_HOST, settings.HDFS_DF_ROOT , \
                                                                           data_frame, table_name) , "parquet" )
            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            temp = pd.read_csv(file_path)
            append_df = sqlContext.createDataFrame(temp)
            append_df.unionAll(df)
            append_df.write.parquet("hdfs://{0}/{1}/{2}/{3}".format(settings.HDFS_HOST, settings.HDFS_DF_ROOT, \
                                                             data_frame, table_name), mode="append", partitionBy=None)

        except Exception as e:
            utils.tfmsa_logger(e)
            raise Exception (e)

        finally:
            self.sc.stop()