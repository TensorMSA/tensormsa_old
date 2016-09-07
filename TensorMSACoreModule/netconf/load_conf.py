"""
TO-DO : get conf data form db and return with json
"""

# -*- coding: utf-8 -*-
import json


# before dev db conn module get data from file for test
# TO-DO : get connection from db and get sellected nn conf info
def load_conf(net_id="sample.json"):
    model_conf = open("~/PycharmProjects/TensorMSA/TensorMSACoreModule/tfmsa/data/" + net_id)
    json_data = json.loads(model_conf)

    return json_data