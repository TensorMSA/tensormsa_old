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
