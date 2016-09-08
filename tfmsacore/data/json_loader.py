# -*- coding: utf-8 -*-
import json
import os
from tfmsacore.data import json_conv

def load_data(net_id):
    """
    json type data loader
    :param net_id:
    :return:
    """

    net_id = net_id + "_data.json"
    #curreunt_path = os.path.dirname(os.path.abspath(__file__))
    curreunt_path = os.path.dirname(os.getcwd())

    print("loading conf path : {0}".format(curreunt_path + "/data/" + net_id))

    model_conf = open(curreunt_path + "/data/" + net_id , 'r')
    json_data = json_conv.JsonDataConverter().load_obj_json(model_conf)

    model_conf.close()
    return json_data



def load_tag(net_id):
    """
    json type data loader
    :param net_id:
    :return:
    """

    net_id = net_id + "_tag.json"
    #curreunt_path = os.path.dirname(os.path.abspath(__file__))
    curreunt_path = os.path.dirname(os.getcwd())

    print("loading conf path : {0}".format(curreunt_path + "/data/" + net_id))

    model_conf = open(curreunt_path + "/data/" + net_id , 'r')
    json_data = json_conv.JsonDataConverter().load_obj_json(model_conf)

    model_conf.close()
    return json_data