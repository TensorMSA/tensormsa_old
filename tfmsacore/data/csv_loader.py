# -*- coding: utf-8 -*-
import json
import os


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
    json_data = json.loads(model_conf.read())

    model_conf.close()
    return json_data

