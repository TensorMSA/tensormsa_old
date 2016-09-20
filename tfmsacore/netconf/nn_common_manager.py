# -*- coding: utf-8 -*-
from tfmsacore import models
from tfmsacore.utils import serializers


def create_new_network(req):
    """
    create new nn user request
    :param net_id:
    :return:
    """
    serializer = serializers.NNInfoSerializer(data=req)
    if serializer.is_valid():
        serializer.save()
        return "success"
    return "failure"


def update_network(req):
    """
    update neural network basic info
    :param net_id:
    :return:
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= req.nn_id)
        obj.category = req.category
        obj.name = req.name
        obj.type = req.type
        obj.acc = req.acc
        obj.train = req.train
        obj.config = req.config
        obj.table = req.table
        obj.query = req.query
        obj.datadesc = req.datadesc
        obj.datasets = req.datasets
        obj.dir = req.dir
        obj.save()
    except IOError as e:
        print (e)
        return "failure"
    return "success"


def set_train_result(nn_id , acc):
    """
    :param nn_id: neural network id
    :param acc: accuracy result of training
    :return: success , failure
    """
    try:
        obj = models.NNInfo.objects.get(nn_id= nn_id)
        obj.acc = acc
        obj.save()
    except:
        return "failure"
    return "success"

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
    except:
        return "failure"
    return "success"


def filter_network_config(nn_id, category):
    """
    get selected nn_id config info
    :param nn_id: neural network id
    :param category: business category
    :return:
        [{ "nn_id": "",
           "category":"",
           "name" : "",
           "type" : "",
           "acc" : "",
           "train" : "",
           "config" : "",
           "table" : "",
           "query" : "",
           "datadesc":"{object : value}",
           "datasets":"{object : []}",
           "dir" : ""}]
    """

    try:
        query_set = models.NNInfo.objects.filter(nn_id__contains= nn_id, category__contains = category)
    except IOError as e:
        raise e
    finally:
        return query_set.values()

def get_network_config(nn_id):
    """
    get selected nn_id config info
    :param nn_id: neural network id
    :param category: business category
    :return:
        [{ "nn_id": "",
           "category":"",
           "name" : "",
           "type" : "",
           "acc" : "",
           "train" : "",
           "config" : "",
           "table" : "",
           "query" : "",
           "datadesc":"{object : value}",
           "datasets":"{object : []}",
           "dir" : ""}]
    """

    try:
        data_Set = models.NNInfo.objects.get(nn_id__contains= nn_id)
        return data_Set.json()
    except IOError as e:
        raise e
