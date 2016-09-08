# -*- coding: utf-8 -*-
import json
import os
from tfmsacore.data import json_conv


def load_conf(net_id):
    """
    before dev db conn module get data from file for test
    TO-DO : get connection from db and get sellected nn conf info
    :param net_id:
    :return:
    """

    """
    TO-DO : need to stroe data on data base
    """
    directory = "/tensorMSA/data/"
    net_id = net_id + "_conf.json"
    #curreunt_path = os.path.dirname(os.path.abspath(__file__))
    #curreunt_path = os.path.dirname(os.getcwd())

    if not os.path.exists(directory):
        os.makedirs(directory)

    model_conf = open(directory + net_id, 'r')
    json_data = json_conv.JsonDataConverter().load_obj_json(model_conf)

    model_conf.close()
    return json_data



def save_conf(net_id):

    return True