# -*- coding: utf-8 -*-
from tfmsacore.utils.json_conv import JsonDataConverter as jc

def load_data(net_id):
    """
    json type data loader
    :param net_id:
    :return:
    """

    net_id = net_id + "_data.json"
    directory = "/tensorMSA/data/"
    #curreunt_path = os.path.dirname(os.getcwd())
    model_conf = open(directory + net_id, 'r')
    json_data = jc.load_obj_json(model_conf)

    model_conf.close()
    return json_data



def load_tag(net_id):
    """
    json type data loader
    :param net_id:
    :return:
    """

    net_id = net_id + "_tag.json"
    directory = "/tensorMSA/data/"
    #curreunt_path = os.path.dirname(os.getcwd())
    model_conf = open(directory + net_id, 'r')
    json_data = jc.load_obj_json(model_conf)

    model_conf.close()
    return json_data