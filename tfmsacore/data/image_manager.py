from tfmsacore import netconf
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
import os, happybase, json, struct, sys, time, random
import numpy as np
import tensorflow as tf
from django.conf import settings
import pandas as pd
from tfmsacore.data.hbase_manager import HbaseManager



class ImageManager(HbaseManager):
    """
    HdfsManager : mainly manageing hdfs folders
    lv1 : image, raw rext, parquet types
    lv2 : category
    lv3 : sub category
    lv4 : real files
    """

    def put_data(self, data_frame, table_name, label, file_set):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            tfmsa_logger("Start upload images...")

            # crate hbase session
            conn = self.session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            make_prefix = data_frame + ":"

            # get table transaction buffer
            table = conn.table(make_prefix + table_name, use_prefix=False)
            buffer = table.batch(transaction=True)

            # prepare send data

            for file in file_set:
                row_value = dict()
                row_key = table_name + ":" + self.make_hbasekey()
                byte_buffer = b""
                for chunk in file.chunks():
                    byte_buffer = byte_buffer + chunk
                row_value[':'.join(('data', 'filebyte'))] = str(byte_buffer)
                row_value[':'.join(('data', 'label'))] = str(label)
                buffer.put(row_key, row_value)
            buffer.send()
            return len(file_set)
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)
        finally:
            conn.close()
            tfmsa_logger("Finish upload image...")

    def load_data(self, data_frame, table_name, st_pnt = "0", end_pnt = "10"):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        return_list = []
        try:
            # crate hbase session
            conn = self.session_create()
            conn.table_prefix = data_frame
            conn.table_prefix_separator = ":"
            make_prefix = data_frame + ":"
            table = conn.table(make_prefix + table_name, use_prefix=False)
            #rows = table.scan(row_start=st_pnt, row_stop=end_pnt)
            rows = table.scan()

            for row in rows:
                return_list.append({'bt' : row[1][b'data:filebyte'] , 'label' : row[1][b'data:label']})

            return return_list
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)
