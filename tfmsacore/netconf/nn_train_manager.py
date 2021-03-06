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
        query_set = models.TrainResultLoss.objects.filter(nn_id=nn_id).select_related().order_by('step')
        query_set = serial.serialize("json", query_set)
        query_set = json.loads(query_set)
        return_list = []
        for set in query_set:
            #return_list.insert(0, set['fields']['loss'])
            return_list.append(set['fields']['loss'])
        return return_list
    except Exception as e:
        raise Exception(e)

def delete_train_loss(nn_id):
    """
    delete all loss history data on nn_id
    :param nn_id:
    :return:
    """
    try:
        models.TrainResultLoss.objects.filter(nn_id=nn_id).delete()
        return nn_id
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
        query_set = models.TrainResultAcc.objects.filter(nn_id=nn_id).select_related()
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set)
    except Exception as e:
        raise Exception(e)

def delete_train_acc(nn_id):
    """
    delete all loss history data on nn_id
    :param nn_id:
    :return:
    """
    try:
        models.TrainResultAcc.objects.filter(nn_id=nn_id).delete()
        return nn_id
    except Exception as e:
        raise Exception(e)