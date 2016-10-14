from pyspark import SparkContext, SparkConf
from tfmsacore.utils.logger import tfmsa_logger
from pyspark.sql import SQLContext
from django.conf import settings
import pandas as pd
import os
import shutil
import happybase
import json
import struct
import sys
import numpy as np


class HiveManager:
    def __init__(self):
        print("Hive file manager")


    def spark_session_create(self):
        """
        Hbase Loader Class
        creadted for the purpose of handling Spark Jobs
        """

        tfmsa_logger("Spark Session Created")
        conn = happybase.Connection(host=settings.HBASE_HOST, port=settings.HBASE_HOST_PORT)
        #print(conn.__class__)
        return conn

    def search_all_database(self):
        """
        search all databases
        :return: database list
        """
        try:
            conn = self.spark_session_create()
            db_names = []
            tables = conn.tables()
            for tb in tables:
                print(tb)
                if (tb.find(":") > 0):
                    db_names.append(tb.split(":")[0])
            distict_db = set(db_names)
            return json.dumps(distict_db)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def search_database(self, db_name):
        """
        return all tables names
        :param db_name: target database name
        :return: table list
        """
        try:
            conn = self.spark_session_create()
            conn.table_prefix = db_name
            conn.table_prefix_separator = ":"
            print(db_name)
            table = conn.tables()
            return json.dumps(table)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def query_data(self, data_frame, table_name, query_str, limit_cnt=0):
        """
        get query data from spark
        :param table_name: name of table you want to get data
        :param query_str: sql strings
        :return: query result as json Object
        """
        try:
            tfmsa_logger("start query data !")
            conn = self.spark_session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            # DBNAME probably needs

            table = conn.table(table_name)

            key = 'networkid'  # shoud be chaned when producing.

            column_dtype_key = key + 'columns'
            cf = 'data'
            column_dtype = table.row(column_dtype_key, columns=[cf])
            columns = {col.split(':')[1]: value for col, value in column_dtype.items()}

            column_order_key = key + 'column_order'
            column_order_dict = table.row(column_order_key, columns=[cf])
            column_order = list()
            for i in xrange(len(column_order_dict)):
                column_order.append(column_order_dict[':'.join((cf, struct.pack('>q', i)))])

            row_start = key + 'rows' + struct.pack('>q', 0)
            row_end = key + 'rows' + struct.pack('>q', sys.maxint)
            rows = table.scan(row_start=row_start, row_stop=row_end, limit=30000)
            df = pd.DataFrame(columns=columns)
            for row in rows:
                df_row = {key.split(':')[1]: value for key, value in row[1].items()}
                df = df.append(df_row, ignore_index=True)
                print (df_row)
            for column, data_type in columns.items():
                df[column] = df[column].astype(np.dtype(data_type))
            return df

            # hdfs_path = settings.HDFS_DF_ROOT + "/" + data_frame + "/" + table_name
            #
            # sqlContext = SQLContext(self.sc)
            # df = sqlContext.read.load(hdfs_path, "parquet")
            # df.registerTempTable(table_name)
            # if (limit_cnt == 0):
            #     result = sqlContext.sql(str(query_str)).collect()
            # else:
            #     result = sqlContext.sql(str(query_str)).limit(limit_cnt).collect()
            # return result


            tfmsa_logger("End query data!")

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            df.unpersist()
            self.sc.stop()