# -*- coding: utf-8 -*-
import json
import os
from tfmsacore.data import json_conv
from tfmsacore import models
from tfmsacore.utils import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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


def set_train_result(nn_id , acc):
    """
    :param nn_id: neural network id
    :param acc: accuracy result of training
    :return: success , failure
    """

    try:
        req = { "nnid": nn_id,
                "category":"",
                "name" : "",
                "type" : "",
                "acc" : acc,
                "train" : "",
                "config" : "",
                "dir" : "default"}
        obj = models.NNInfo.objects.get(nnid= nn_id)
        obj.acc = acc
        obj.save()
    except:
        return "failure"
    return "success"
