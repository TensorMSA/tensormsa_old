# -*- coding: utf-8 -*-
from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger
from django.core import serializers as serial
import json

def post_train_loss(req):
    """
    insert loss value change history data
    :param net_id:
    :return:
    """
    try:
        serializer = serializers.TrainResultLossSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        tfmsa_logger(e)
        raise Exception(e)
    finally:
        return str(req["nn_id"]) + str(req["step"])

def get_train_loss(nn_id):
    """
    query all eval result
    :param nn_id:
    :return:
    """
    try:
        query_set = models.TrainResultLoss.objects.filter(nn_id=nn_id).select_related()
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)
    except Exception as e:
        raise Exception(e)


def post_train_acc(req):
    """
    train result from each label aspect
    :param net_id:
    :return:
    """
    try:
        serializer = serializers.TrainResultAccSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        tfmsa_logger(e)
        raise Exception(e)
    finally:
        return len(req)


def get_train_acc(nn_id):
    """
    query all eval result
    :param nn_id:
    :return:
    """
    try:
        query_set = models.NNInfo.objects.filter(nn_id=nn_id).select_related()
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)
    except Exception as e:
        raise Exception(e)
