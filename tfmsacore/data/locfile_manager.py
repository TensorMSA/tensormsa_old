from pyspark import SparkContext, SparkConf
from tfmsacore.utils.logger import tfmsa_logger
from pyspark.sql import SQLContext
from django.conf import settings
import pandas as pd
import os
import shutil

class LocalFileManager:
    """
    HdfsManager : mainly manageing hdfs folders
    lv1 : image, raw rext, parquet types
    lv2 : category
    lv3 : sub category
    lv4 : real files
    """
    def __init__(self):
        """
        create non exist essential directories
        """
        if not os.path.exists(settings.HDFS_ROOT):
            os.makedirs(settings.HDFS_ROOT)
        if not os.path.exists(settings.HDFS_DF_ROOT):
            os.makedirs(settings.HDFS_DF_ROOT)
        if not os.path.exists(settings.HDFS_CONF_ROOT):
            os.makedirs(settings.HDFS_CONF_ROOT)
        if not os.path.exists(settings.HDFS_MODEL_ROOT):
            os.makedirs(settings.HDFS_MODEL_ROOT)
        self.root = "{0}/".format(settings.HDFS_DF_ROOT)

    def spark_session_create(self):
        """
        spark Loader Class
        creadted for the purpose of handling Spark Jobs
        """
        tfmsa_logger("Spark Session Created")
        conf = SparkConf()
        conf.setMaster('spark://{0}'.format(settings.SPARK_HOST))
        conf.setAppName('save_csv_to_df')
        conf.set('spark.driver.cores', settings.SPARK_CORE)
        conf.set('spark.driver.memory', settings.SPARK_MEMORY)
        conf.set('spark.executor.cores', settings.SPARK_WORKER_CORE)
        conf.set('spark.executor.memory', settings.SPARK_WORKER_MEMORY)

        self.sc = SparkContext(conf=conf)


    def search_all_database(self):
        """
        search all databases
        :return: database list
        """
        try:
            databases = os.listdir("{0}".format(self.root))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)
        return databases

    def create_database(self, db_name):
        """
        :param db_name: target database name
        :return: none
        """
        try:
            directory = "{0}{1}".format(self.root,db_name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            return db_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_database(self, db_name):
        """
        :param db_name: target database name
        :return: none
        """
        try:
            shutil.rmtree("{0}{1}".format(self.root,db_name))
        except Exception as e:
            raise Exception(e)

    def search_database(self, db_name):
        """
        return all tables names
        :param db_name: target database name
        :return: table list
        """
        try:
            return os.listdir("{0}{1}".format(self.root, db_name))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def rename_database(self, db_name, change_name):
        """
        rename database
        :param db_name: as-is database name
        :param change_name: tb-be data base name
        :return:
        """
        try:
            os.rename("{0}{1}".format(self.root, db_name), "{0}{1}".format(self.root, change_name))
            return change_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def create_table(self, db_name, table_name):
        """
        create table
        :param db_name:target database name
        :param table_name:target table name
        :return:
        """
        try:
            directory = "{0}{1}".format(self.root, db_name)
            if not os.path.exists(directory):
                os.makedirs(directory)

            os.makedirs("{0}{1}/{2}".format(self.root, db_name, table_name))
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_table(self, db_name, table_name):
        """
        delete table
        :param db_name:target database name
        :param table_name:target table name
        :return:
        """
        try:
            directory = "{0}{1}/{2}".format(self.root, db_name, table_name)
            if not os.path.exists(directory):
                raise Exception("request table : {0} not exist".format(table_name))

            shutil.rmtree("{0}{1}/{2}".format(self.root, db_name, table_name))
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def reset_table(self, db_name, table_name):
        """
        reset table contents
        :param db_name:target database name
        :param table_name:target table name
        :return:
        """
        try:
            directory = "{0}{1}/{2}".format(self.root, db_name, table_name)
            if not os.path.exists(directory):
                self.create_table(db_name, table_name)

            shutil.rmtree("{0}{1}/{2}".format(self.root, db_name, table_name))
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def rename_table(self, db_name, table_name, rename_table):
        """
        rename table
        :param db_name:target database name
        :param table_name:target table name
        :param rename_table:to-be table name
        :return:
        """
        try:
            os.rename("{0}{1}/{2}".format(self.root, db_name, table_name) \
                      , "{0}{1}/{2}".format(self.root, db_name, rename_table))
            return rename_table
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
            return os.open("/{0}/{1}".format(root, nn_id)).read()
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def hdfs_chk(self, root, nn_id):
        """
        check if nn_id exist
        :param category: business category
        :param subcate: business subcategory
        :param nn_id: nerual network id
        :return:
        """
        try:
            if os.path.exists("/{0}/{1}".format(root, nn_id)):
                return True
            else :
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
            f = open("/{0}/{1}".format(root, nn_id), 'w')
            f.write(str(records))
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
            shutil.rmtree("/{0}/{1}".format(root, nn_id))
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def get_distinct_dataframe(self, data_frame, table_name, columns):
        """
        get distinct table columns
        :param table_name: name of table you want to get data
        :param query_str: sql strings
        :return: query result as json Object
        """
        try:
            self.spark_session_create()
            tfmsa_logger("start find distinct column !")
            hdfs_path = "/" + settings.HDFS_HOST + settings.HDFS_DF_ROOT + "/" + data_frame + "/" + table_name
            query_str = "select * from " + table_name

            sqlContext = SQLContext(self.sc)

            df = sqlContext.read.load(hdfs_path, "parquet")
            df.registerTempTable(table_name)
            result = sqlContext.sql(str(query_str))

            return_data = {}
            for column in columns:
                return_data[column.encode("UTF8")] = result.select(column).map(
                    lambda x: str(x[0]).encode("UTF8")).distinct().collect()

            tfmsa_logger("End find distinct column !")

            return return_data

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            df.unpersist()
            self.sc.stop()


    def query_data(self, data_frame, table_name, query_str, limit_cnt=0):
        """
        get query data from spark
        :param table_name: name of table you want to get data
        :param query_str: sql strings
        :return: query result as json Object
        """
        try:
            self.spark_session_create()
            tfmsa_logger("start query data !")
            hdfs_path = "/" + settings.HDFS_HOST + settings.HDFS_DF_ROOT + "/" + data_frame + "/" + table_name

            sqlContext = SQLContext(self.sc)
            df = sqlContext.read.load(hdfs_path, "parquet")
            df.registerTempTable(table_name)
            if (limit_cnt == 0):
                result = sqlContext.sql(str(query_str)).collect()
            else:
                result = sqlContext.sql(str(query_str)).limit(limit_cnt).collect()
            return result

            tfmsa_logger("End query data!")

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            df.unpersist()
            self.sc.stop()


    def post_json_data(self, data_frame, table_name, json_data):
        """
        create table with json data
        :param table_name: name of table want to create
        :param json_data: json form schema data
        :return: success or failure
        """
        try:
            self.spark_session_create()
            tfmsa_logger("start create_table !")
            hdfs_path = settings.HDFS_DF_ROOT + "/" + data_frame + "/" + table_name

            sqlContext = SQLContext(self.sc)
            df_writer = sqlContext.createDataFrame(str(json_data)).write
            df_writer.parquet(hdfs_path, mode="append", partitionBy=None)
            tfmsa_logger("End create_table !")

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            df_writer.unpersist()
            self.sc.stop()


    def put_json_data(self, data_frame, table_name, json_data):
        """
        append data on exist table
        :param table_name: name of table want to add data
        :param json_data: json form schema data
        :return: success or failure
        """
        try:
            self.spark_session_create()
            tfmsa_logger("start append_data !")
            hdfs_path = settings.HDFS_DF_ROOT + "/" + data_frame + "/" + table_name

            sqlContext = SQLContext(self.sc)
            df = sqlContext.read.load(hdfs_path, "parquet")
            df_writer = sqlContext.createDataFrame(str(json_data))
            df.unionAll(df_writer)
            df.write.parquet(hdfs_path, mode="append", partitionBy=None)
            tfmsa_logger("End append_data !")

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            df_writer.unpersist()
            df.unpersist()
            self.sc.stop()


    def save_csv_to_df(self, data_frame, table_name, csv_file):
        """
        create new table with inserted csv data
        :param net_id:
        :return:
        """
        try:
            self.spark_session_create()
            tfmsa_logger("start uploading csv on Hadoop")
            # clear current exist table
            self.reset_table(data_frame, table_name)

            sqlContext = SQLContext(self.sc)

            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            df = sqlContext.createDataFrame(pd.read_csv(file_path))
            df.write.parquet("{0}/{1}/{2}".format(settings.HDFS_DF_ROOT, data_frame, table_name),
                             mode="append", partitionBy=None)
            tfmsa_logger("uploading csv on Hadoop finished")


        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)
        finally:
            df.unpersist()
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
            self.spark_session_create()
            sqlContext = SQLContext(self.sc)
            df = sqlContext.read.load("{0}/{1}/{2}".format(settings.HDFS_DF_ROOT, data_frame, table_name), "parquet")
            file_path = settings.FILE_ROOT + "/" + data_frame + "/" + table_name + "/" + csv_file
            append_df = sqlContext.createDataFrame(pd.read_csv(file_path))
            append_df.unionAll(df)
            append_df.write.parquet("{0}/{1}/{2}".format(settings.HDFS_DF_ROOT, data_frame, table_name),
                                    mode="append", partitionBy=None)

        except Exception as e:
            tfmsa_logger(e)
            raise Exception(e)

        finally:
            df.unpersist()
            append_df.unpersist()
            self.sc.stop()