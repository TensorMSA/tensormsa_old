# -*- coding: utf-8 -*-
import json
import os
from tfmsacore.data import json_conv
from tfmsacore import models
from tfmsacore.utils import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NNListManager():
    """
    List all snippets, or create a new snippet.
    """

    def create_new_network(self, request):
        """
        create new nn user request
        :param net_id:
        :return:
        """

        """
        TO-DO : need to stroe data on data base
        """
        serializer = serializers.NNListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


