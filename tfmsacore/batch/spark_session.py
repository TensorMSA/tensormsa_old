from hdfs import Config
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
from pyspark.streaming import StreamingContext
from pyspark import SparkContext, SparkConf
from tfmsacore.utils.logger import tfmsa_logger
from pyspark.sql import SQLContext
from django.conf import settings
import pandas as pd



class SparkSessionManager:
    """
    SparkSessionManager : share Spark Context via Threada
    """

    def create_session(self):
        """
        spark Loader Class
        creadted for the purpose of handling Spark Jobs
        """
        try :
            tfmsa_logger("Spark Session Created")
            global spark_context

            # #tfmsa_logger("spark_context : {0}".format(spark_context))
            # if (isinstance(spark_context, (SparkContext))):
            #     return spark_context

            conf = SparkConf()
            conf.setMaster('spark://{0}'.format(settings.SPARK_HOST))
            conf.setAppName("tfmsa_session_manager")
            conf.set('spark.driver.cores', settings.SPARK_CORE)
            conf.set('spark.driver.memory', settings.SPARK_MEMORY)
            conf.set('spark.executor.cores', settings.SPARK_WORKER_CORE)
            conf.set('spark.executor.memory', settings.SPARK_WORKER_MEMORY)
            #conf.set('spark.driver.allowMultipleContexts', "true")
            spark_context = SparkContext(conf=conf)
            return spark_context
        except Exception as e :
            # tfmsa_logger(e)
            # raise Exception(e)
            return spark_context


    def get_session(self):
        tfmsa_logger("context : {0}".format(spark_context))
        return spark_context



