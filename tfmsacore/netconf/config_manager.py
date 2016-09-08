"""
TO-DO : get conf data form db and return with json
"""

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

    net_id = net_id + "_conf.json"
    #curreunt_path = os.path.dirname(os.path.abspath(__file__))
    curreunt_path = os.path.dirname(os.getcwd())

    print("loading conf path : {0}".format(curreunt_path + "/data/" + net_id))

    model_conf = open(curreunt_path + "/data/" + net_id , 'r')
    json_data = json_conv.JsonDataConverter().load_obj_json(model_conf)

    model_conf.close()
    return json_data



def save_conf(net_id):

    return True