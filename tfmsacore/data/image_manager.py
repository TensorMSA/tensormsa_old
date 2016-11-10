from tfmsacore import netconf
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings
import os, happybase, json, struct, sys, time, random
import numpy as np
import tensorflow as tf
from django.conf import settings
import pandas as pd
from tfmsacore.data.hbase_manager import HbaseManager
from tfmsacore import preprocess
from tfmsacore.utils.json_conv import JsonDataConverter as jc
import shutil

class ImageManager(HbaseManager):
    """
    HdfsManager : mainly manageing hdfs folders
    lv1 : image, raw rext, parquet types
    lv2 : category
    lv3 : sub category
    lv4 : real files
    """

    def put_data(self, data_frame, table_name, label, file_set, nnid):
        """
        delete label folder under table
        :param db_name:
        :param table_name:
        :return:
        """
        try:
            tfmsa_logger("[1]Start upload images...")

            # get network base info
            tfmsa_logger("[2]get network base info")
            net_info = netconf.get_network_config(nnid)

            # get data format info
            tfmsa_logger("[3]get network format info")
            format_info = json.loads(netconf.load_ori_format(nnid))

            # get hbase trasaction table
            tfmsa_logger("[4]get hbase trasaction table")
            conn, table = self.get_target_table(data_frame, table_name)
            buffer = table.batch(transaction=True)

            #get Label list
            tfmsa_logger("[5]Updata Label List ")
            self.label_info_update(net_info, label)

            # get Label list
            tfmsa_logger("[6]upload image on Hbase - start ")
            file_list = []

            for key in file_set.keys():
                file = file_set[key]
                row_value = dict()
                row_key = table_name + ":" + self.make_hbasekey()
                byte_buffer, width, height = self.image_preprocess(file, net_info, format_info, label)
                row_value[':'.join(('data', 'filebyte'))] = str(list(byte_buffer))
                row_value[':'.join(('data', 'label'))] = str(label)
                row_value[':'.join(('data', 'decoder'))] = str(key).split(".")[1]
                row_value[':'.join(('data', 'width'))] = str(width)
                row_value[':'.join(('data', 'height'))] = str(height)
                file_list.append(file._name)
                buffer.put(row_key, row_value)
            buffer.send()
            tfmsa_logger("[7]upload image on Hbase - finish")
            return file_list
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
            # get hbase trasaction table
            tfmsa_logger("[1]start - load image data")
            conn, table = self.get_target_table(data_frame, table_name)

            #rows = table.scan(row_start=st_pnt, row_stop=end_pnt)
            rows = table.scan()

            for row in rows:
                return_list.append({'bt' : row[1][b'data:filebyte'] ,
                                    'label' : row[1][b'data:label'] ,
                                    'decoder': row[1][b'data:decoder'],
                                    'width' : row[1][b'data:width'],
                                    'height': row[1][b'data:height']})
            tfmsa_logger("[2]Finish - load image data ")
            return return_list
        except Exception as e:
            tfmsa_logger("Error : {0}".format(e))
            raise Exception(e)


    def get_target_table(self, data_frame, table_name):
        """

        :param data_frame:
        :param table_name:
        :return:
        """
        # crate hbase session
        conn = self.session_create()
        conn.table_prefix = data_frame
        conn.table_prefix_separator = ":"
        make_prefix = data_frame + ":"

        # get table transaction buffer
        table = conn.table(make_prefix + table_name, use_prefix=False)

        return conn, table

    def image_preprocess(self, file, net_info, format_info, label):
        """

        :param file:
        :param net_info:
        :param format_info:
        :return:
        """
        # prepare send data
        rand_tag = str(random.randrange(0, 99999))
        save_path = "{0}/{1}".format(settings.FILE_ROOT, net_info['table'])
        save_file = "{0}/{1}/{2}{3}".format(settings.FILE_ROOT, net_info['table'], rand_tag, file._name)

        if not os.path.exists(save_path):
            os.mkdir(save_path)
        fp = open(save_file, 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        # resize image
        byte_buffer, width, height = preprocess.ImagePreprocess().\
            resize_file_image(save_file, net_info, format_info, file._name, label)

        if os.path.isfile(save_file):
            os.remove(save_file)

        return byte_buffer, width, height

    def label_info_update(self, net_info, label):
        """

        :param net_info:
        :param label:
        :return:
        """
        if (len(str(net_info['datasets'])) == 0):
            label_list = []
        else:
            label_list = json.loads(net_info['datasets'])

        if label not in label_list:
            label_list.append(label)
            jd = jc.load_obj_json("{}")
            jd.nn_id = net_info['nn_id']
            jd.datasets = json.dumps(label_list)
            result = netconf.update_network(jd)

    def get_label_list(self, nn_id):
        """
        get image label list
        :param net_info:
        :param label:
        :return:
        """
        net_info = netconf.get_network_config(nn_id)
        if (len(str(net_info['datasets'])) == 0):
            label_list = []
        else:
            label_list = json.loads(net_info['datasets'])
            print(label_list)
        return label_list

    def update_label_list(self, nn_id, label):
        """
        update image label list
        :param net_info:
        :param label:
        :return:
        """
        net_info = netconf.get_network_config(nn_id)
        if (len(str(net_info['datasets'])) == 0):
            label_list = []
        else:
            label_list = json.loads(net_info['datasets'])

        if label not in label_list:
            label_list.append(label)
            jd = jc.load_obj_json("{}")
            jd.nn_id = net_info['nn_id']
            jd.datasets = json.dumps(label_list)
            result = netconf.update_network(jd)
        return self.get_label_list(nn_id)

    def get_preview_list(self, nn_id):
        """
        return preview file locations
        :param nn_id:
        :return:
        """
        net_info = netconf.get_network_config(nn_id)
        dataframe = net_info['dir']
        table = net_info['table']
        label_set = json.loads(net_info['datasets'])
        preview_file_list = {}

        preview_table = "{0}/{1}/{2}/{3}".format(settings.PREVIEW_IMG_PATH, "preview", dataframe, table)
        url_path = "/{0}/{1}/{2}/{3}".format("dist", "preview", dataframe, table)

        for label in label_set:
            preview_file_list[label] = []
            if not os.path.exists("{0}/{1}/".format(preview_table, label)):
                os.makedirs("{0}/{1}/".format(preview_table, label))
            for filename in os.listdir("{0}/{1}/".format(preview_table, label)):
                preview_file_list[label].append("{0}/{1}/{2}".format(url_path, label, filename))
        return preview_file_list


    def delete_preview_list(self, nn_id):
        """
        return preview file locations
        :param nn_id:
        :return:
        """
        net_info = netconf.get_network_config(nn_id)
        dataframe = net_info['dir']
        table = net_info['table']
        label_set = json.loads(net_info['datasets'])
        preview_file_list = {}

        preview_table = "{0}/{1}/{2}/{3}".format(settings.PREVIEW_IMG_PATH, "preview", dataframe, table)

        for label in label_set:
            preview_file_list[label] = []
            shutil.rmtree(("{0}/{1}/".format(preview_table, label)))
        return preview_file_list