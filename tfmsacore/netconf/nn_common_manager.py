# -*- coding: utf-8 -*-
import json
import os
from tfmsacore.data import json_conv
from tfmsacore import models
from tfmsacore.utils import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NNInfoManager():
    """
    List all snippets, or create a new snippet.
    """
    def create_new_network(self, req):
        """
        create new nn user request
        :param net_id:
        :return:
        """

        print("=========request.data : {0}".format(req.data))
        serializer = serializers.NNInfoSerializer(data=req.data)
        print("=====serializer : {0} " .format(serializer))

        if serializer.is_valid():
            serializer.save()
            print("======serializer.data : {0}".format(serializer.data))
            return "success"
        return "failure"


