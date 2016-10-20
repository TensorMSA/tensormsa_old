# -*- coding: utf-8 -*-
from tfmsacore import models
from tfmsacore.utils import serializers
from tfmsacore.utils.logger import tfmsa_logger
from django.core import serializers as serial
import json

def create_new_network(req):
    """
    create new nn user request
    :param net_id:
    :return:
    """
    try:
        serializer = serializers.NNInfoSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        tfmsa_logger(e)
        raise Exception (e)
    finally :
        return req["nn_id"]


def update_network(req):
    """
    update neural network basic info
    :param net_id:
    :return:
    """

    try:
        obj = models.NNInfo.objects.get(nn_id= req.nn_id)
        for key in req.keys():
            if(obj[key] != None):
                setattr(obj, key, req[key])

        obj.save()
        return req.nn_id
    except Exception as e:
        return e



def set_train_result(nn_id , acc):
    """
    :param nn_id: neural network id
    :param acc: accuracy result of training
    :return: success , failure
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.acc = acc
        obj.train = "Y"
        obj.save()

    except Exception as e:
        raise Exception(e)


def set_train_datasets(nn_id , datasets):
    """
    :param nn_id: neural network id
    :param acc: accuracy result of training
    :return: success , failure
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.datasets = datasets
        obj.save()

    except Exception as e:
        raise Exception(e)


def filter_network_config(nn_id = None, category = None, subcate = None):
    """
    get selected nn_id config info
    :param nn_id: serarch condition nn_id
    :param category: serarch condition category
    :param subcate: serach condition subcate
    :return : all column data from nn_info as list-dict format
    """

    try:
        query_set = models.NNInfo.objects.filter(nn_id__contains= nn_id, \
                                                 category__contains = category, \
                                                 subcate__contains = subcate)
        query_set = serial.serialize("json", query_set)
        return json.loads(query_set, 'utf-8')
    except Exception as e:
        raise Exception(e)


def get_network_config(nn_id):
    """
    get selected nn_id config info
    :param nn_id: serarch condition nn_id
    :return : all column data from nn_info as dic format
    """
    try:
        data_set = models.NNInfo.objects.get(nn_id__contains= nn_id)
        return data_set.json()
    except Exception as e:
        raise Exception(e)


def delete_net_info(nn_id):
    """
    delete selected nn_id network info
    :param nn_id: neural network id
    :param category: business category
    :return:None
    """

    try:
        if (isinstance(nn_id, (str))):
            query_set = models.NNInfo.objects.filter(nn_id__contains= nn_id).delete()
        elif(isinstance(nn_id, (list))):
            for d_id in nn_id:
                query_set = models.NNInfo.objects.filter(nn_id__contains=d_id).delete()
        else:
            return 'delete request data type is wrong'
        return nn_id

    except Exception as e:
        return e

