# -*- coding: utf-8 -*-
from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger
from django.core import serializers as serial
import json

def insert_train_results(req):
    """
    create new nn user request
    :param net_id:
    :return:
    """
    try:
        serializer = serializers.TrainResultsSerializer(data=req)
        #print(req)
        if serializer.is_valid():
            # print("serializers is ok in if")
            serializer.save()
    except Exception as e:
        tfmsa_logger(e)
        raise Exception(e)
    finally:
        return str(req["nn_id"]) + str(req["step"])
