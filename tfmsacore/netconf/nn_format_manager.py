# -*- coding: utf-8 -*-
import os
from tfmsacore.utils.json_conv import JsonDataConverter
from tfmsacore.utils.logger import tfmsa_logger
from django.conf import settings

def chk_format(net_id):
    """
    check if configuraiotn data exist with requested net id
    :param net_id: neural network id
    :return:
    """
    directory = settings.HDFS_FORMAT_ROOT + "/" + net_id + "/"
    net_id = net_id + "_format.json"

    try:
        if os.path.isfile(directory + net_id):
            if(os.stat(directory + net_id).st_size == 0):
                return False
            else:
                return True
        else :
            return False
    except :
        return False


def load_format(net_id):
    """
    load json from  path and return it as python object form
    :param net_id: neural network id
    :return:
    """
    directory = settings.HDFS_FORMAT_ROOT + "/" + net_id + "/"
    net_id = net_id + "_format.json"

    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        model_conf = open(directory + net_id, 'r')
        json_data = JsonDataConverter().load_obj_json(model_conf)
    except Exception as e:
        print(e)
        raise Exception(e)
    finally :
        model_conf.close()

    return json_data

def load_ori_format(net_id):
    """
    load json from  path and return it as str
    :param net_id: neural network id
    :return:
    """
    directory = settings.HDFS_FORMAT_ROOT + "/" + net_id + "/" #Bug fix by jh100 16.10.22
    net_id = net_id + "_format.json"

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        model_conf = open(directory + net_id, 'r')
        json_data = model_conf.read()
        return json_data
    except :
        raise SystemError("json load error")
    finally :
        model_conf.close()


def save_format(net_id, conf_data):
    """
    save json format to json file
    :param net_id: neural network id
    :param conf_data: neural network configuration json data
    :return:
    """

    directory = settings.HDFS_FORMAT_ROOT + "/" + net_id + "/" #Bug fix by jh100 16.10.22
    net_id = net_id + "_format.json"

    print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        f = open(directory + net_id, 'w')
        f.write(str(conf_data))

    except:
        raise SystemError("json conf save error")
    finally:
        f.close()


def remove_format(net_id):
    """
    remove json from  path and return it as python object form
    :param net_id: neural network id
    :return:
    """
    directory = settings.HDFS_FORMAT_ROOT + "/" + net_id + "/"
    net_id = net_id + "_format.json"

    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        if os.path.isfile(directory + net_id):
            os.remove(directory + net_id)
    except Exception as e:
        tfmsa_logger("removing conf fail : {0}".format(e))
        raise Exception(e)