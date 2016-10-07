import findspark
findspark.init()
from pyspark.streaming import StreamingContext
from pyspark import SparkContext, SparkConf
from tfmsacore.utils.logger import tfmsa_logger
from pyspark.sql import SQLContext
from django.conf import settings

class SparkManager:
    def __init__(self):
        """
        spark Loader Class
        creadted for the purpose of handling Spark Jobs
        """
        self.create_session()
        tfmsa_logger("Spark Session Created")

    def create_session(self):
        """
        create spark session
        :return:
        """
        conf = SparkConf()
        conf.setMaster('spark://{0}'.format(settings.SPARK_HOST))
        conf.setAppName('SparkerLoader')
        conf.set('spark.driver.cores', settings.SPARK_CORE)
        conf.set('spark.driver.memory', settings.SPARK_MEMORY)
        sc = SparkContext(conf=conf)
        return sc

    def query_data(self, database, table, sql):
        """
        query data directly using Spark
        :param database:
        :param table:
        :param sql:
        :return:
        """
        sqlContext = SQLContext(self.create_session())
        rows = sqlContext.read.load("hdfs://{0}/{1}/{2}/{3}".format(settings.HDFS_HOST, settings.HDFS_DF_ROOT, database, table) , "parquet" )
        tbl = rows.registerTempTable(table)
        result = sqlContext.sql(sql)

        return result





