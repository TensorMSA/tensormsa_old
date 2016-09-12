from django.shortcuts import render

# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.data.json_conv import JsonDataConverter as jc

import json


"""
TO-DO : design api rules
"""

"""
TO-DO : adjust security keys
"""
# Personal contribution check
# http://www.django-rest-framework.org/api-guide/testing/
# https://realpython.com/blog/python/api-integration-in-python/
# http://www.slideshare.net/Byungwook/rest-api-60505484

class CNN_Service(APIView):
    """
    TO-DO : Dev Rest Services for CNN (predict, train, etc)
    """

    # create
    def post(self, request):
        jd = jc.load_obj_json(request.body)
        result = TFMsa().trainNerualNetwork(jd.nn_id, jd.nn_type, jd.run_type)
        return_data = [{"status": "ok", "result": result}]
        print(json.dumps(return_data))
        return Response(json.dumps(return_data))

    # read
    def get(self, request):
        jd = jc.load_obj_json(request.body)
        result = TFMsa().predictNerualNetwork(jd.nn_id, jd.nn_type, jd.run_type, jd.predict_data)
        return_data = [{"status": "ok", "result": result}]
        return Response(json.dumps(return_data))

    # update
    def put(self, request):
        jd = jc.load_obj_json(request.body)
        result = TFMsa().trainNerualNetwork(jd.nn_id, jd.nn_type, jd.run_type)
        return_data = [{"status": "ok", "result": result}]
        print(json.dumps(return_data))
        return Response(json.dumps(return_data))

    # delete
    def delete(self, request, pk, format=None):
        return Response("delete")


class CNN_Config(APIView):
    """
    TO-DO : Dev Rest Services for CNN config change
    """
    def post(self, request):
        """
        insert neural net info with conf
        :param request:
        :return:
        """
        jd = jc.load_obj_json(request.body)
        tfmsa = TFMsa()

        result = tfmsa.createNeuralNetwork(jd.nn_info, jd.nn_conf)
        return_data = [{"status": "ok", "result": result}]
        return Response(json.dumps(return_data))

    def get(self, request):
        """
        get conf data and other info (single or multiple)
        :param pk:
        :return:
        """
        tfmsa = TFMsa()
        jd = jc.load_obj_json(request.body)
        result = tfmsa.searchNeuralNetwork(jd.nn_info)
        return_data = [{"status": "ok", "result": result}]
        return Response(json.dumps(return_data))

    def put(self, request):
        """
        update neural network info with conf
        :param request:
        :return:
        """
        tfmsa = TFMsa()
        jd = jc.load_obj_json(request.body)
        result = tfmsa.updateNeuralNetwork(jd.nn_info, jd.nn_conf)
        return_data = [{"status": "ok", "result": result}]
        return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")

class CNN_Data(APIView):
    """
    TO-DO : Dev Rest Services for CNN Test, Train Datas
    """
    def post(self, request, pk, format=None):
        return Response("post")

    def get(self, pk):
        return Response("get")

    def put(self, request, pk, format=None):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")

class CNN_Stastics(APIView):
    """
    TO-DO : Dev Rest Services for CNN Accuracy , Data, Response, etc
    """
    def post(self, request, pk, format=None):
        return Response("post")

    def get(self, pk):
        return Response("get")

    def put(self, request, pk, format=None):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")