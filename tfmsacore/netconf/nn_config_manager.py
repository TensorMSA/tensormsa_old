# -*- coding: utf-8 -*-
import os
from tfmsacore import data

def load_conf(net_id):
    """
    load json from  path and return it as python object form
    :param net_id: neural network id
    :return:
    """
    directory = "/tensorMSA/data/"
    net_id = net_id + "_conf.json"

    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        model_conf = open(directory + net_id, 'r')
        json_data = data.json_conv.JsonDataConverter().load_obj_json(model_conf)
    except :
        raise SystemError("json load error")
    finally :
        model_conf.close()

    return json_data

def load_ori_conf(net_id):
    """
    load json from  path and return it as str
    :param net_id: neural network id
    :return:
    """
    directory = "/tensorMSA/data/"
    net_id = net_id + "_conf.json"

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        model_conf = open(directory + net_id, 'r')
        json_data = model_conf.read().split()
    except :
        raise SystemError("json load error")
    finally :
        model_conf.close()

    return json_data

def save_conf(net_id, conf_data):
    """
    save json format to json file
    :param net_id: neural network id
    :param conf_data: neural network configuration json data 
    :return:
    """

    directory = "/tensorMSA/data/"
    net_id = net_id + "_conf.json"

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        f = open(directory + net_id, 'w')
        f.write(str(conf_data))
    except:
        raise SystemError("json conf save error")
    finally:
        f.close()

    return True