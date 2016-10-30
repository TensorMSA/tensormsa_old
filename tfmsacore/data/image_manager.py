#https://hdfscli.readthedocs.io/en/latest/quickstart.html#configuration
#setting : ~/.hdfscli.cfg

from hdfs import Config
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
from pyspark.streaming import StreamingContext
from pyspark import SparkContext, SparkConf
from tfmsacore.utils.logger import tfmsa_logger
from pyspark.sql import SQLContext
from django.conf import settings
import pandas as pd
import os

class ImageManager:
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
        self.client = Config().get_client()
        if(self.client.content("{0}/".format(settings.HDFS_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_DF_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_DF_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_CONF_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_CONF_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_MODEL_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_MODEL_ROOT), permission=777)

        if (self.client.content("{0}/".format(settings.HDFS_IMG_ROOT), strict=False) == None):
            self.client.makedirs("{0}/".format(settings.HDFS_IMG_ROOT), permission=777)

        self.root = "{0}/".format(settings.HDFS_IMG_ROOT)


    def search_all_database(self):
        """
        search all databases
        :return: database list
        """
        try:
            databases = self.client.list("{0}".format(self.root))
            return databases
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def create_database(self, db_name):
        """

        :param db_name: target database name
        :return: none
        """
        try:
            if (self.client.content("{0}{1}".format(self.root,db_name), strict=False) != None):
                raise Exception("Data Base {0} Already Exist!!".format(db_name))

            self.client.makedirs("{0}{1}".format(self.root,db_name), permission=777)
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
            self.client.delete("{0}{1}".format(self.root,db_name), recursive=True)
            return db_name
        except Exception as e:
            raise Exception(e)

    def search_database(self, db_name):
        """
        return all tables names
        :param db_name: target database name
        :return: table list
        """
        try:
            return self.client.list("{0}{1}".format(self.root, db_name), status=False)
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
            self.client.rename("{0}{1}".format(self.root, db_name), "{0}{1}".format(self.root, change_name))
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
            self.client.makedirs("{0}{1}/{2}".format(self.root, db_name, table_name) , permission=777)
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
            self.client.delete("{0}{1}/{2}".format(self.root, db_name, table_name), recursive=True)
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
            if (self.client.content("{0}{1}/{2}".format(self.root, db_name, table_name), strict=False) == None):
                self.create_table(db_name, table_name)
                #raise Exception("request table : {0} not exist".format(table_name))

            self.client.delete("{0}{1}/{2}/".format(self.root, db_name, table_name), recursive=True)
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def search_table(self, db_name, table_name):
        """
        return all label under table
        :param db_name: target database name
        :param table_name : target table name
        :return: label list
        """
        try:
            return self.client.list("{0}{1}/{2}".format(self.root, db_name, table_name), status=False)
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
            self.client.rename("{0}{1}/{2}".format(self.root, db_name, table_name), \
                               "{0}{1}/{2}".format(self.root, db_name, rename_table))
            return rename_table
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def create_label(self, db_name, table_name, label):
        """
        create label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            self.client.makedirs("{0}{1}/{2}/{3}".format(self.root, db_name, table_name, label) , permission=777)
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_label(self, db_name, table_name, label):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            self.client.delete("{0}{1}/{2}/{3}".format(self.root, db_name, table_name, label), recursive=True)
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def search_label(self, db_name, table_name, label):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            label_path = "{0}{1}/{2}/{3}".format(self.root, db_name, table_name, label)
            return self.client.list(label_path)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)



    def rename_label(self, db_name, table, label, rename_label):
        """
        rename table
        :param db_name:target database path
        :param table : target table path
        :param label:target label name
        :param rename_label:rename label name
        :return:
        """
        try:
            self.client.rename("{0}{1}/{2}/{3}".format(self.root, db_name, table, label), \
                               "{0}{1}/{2}/{3}".format(self.root, db_name, table, rename_label))
            return rename_label
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def put_data(self, db_name, table_name, label, file, file_name):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            tfmsa_logger("Start upload images...")
            # save file on local file system
            upload_path = "{0}{1}/{2}/{3}/{4}".format(self.root, db_name, table_name, label, file_name)
            local_path = "{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, db_name, table_name, label)
            file_path = "{0}/{1}".format(local_path, file_name)

            if not os.path.exists(local_path):
                os.makedirs(local_path)
            fp = open(file_path, 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            self.client.write(upload_path, data=open(file_path, "rb").read())

            # delete uploaded file
            if os.path.isfile(file_path):
               os.remove(file_path)
            fp.close()
            tfmsa_logger("Finish upload image...")

            return file_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def load_data(self, db_name, table_name, label, file_set):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            return_list = []
            for file_name in file_set:
                file_path = "{0}{1}/{2}/{3}/{4}".format(self.root, db_name, table_name, label, file_name)
                return_list.append(self.client.read(file_path))
            return return_list
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)

    def delete_data(self, db_name, table_name, label, file_name):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            self.client.delete("{0}{1}/{2}/{3}".format(self.root, db_name, table_name, label, file_name), recursive=True)
            return table_name
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)