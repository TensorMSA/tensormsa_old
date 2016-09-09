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
        print(json.dumps(result))
        return Response(json.dumps(result))

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
        tfmsa = TFMsa()
        result = tfmsa.createNewNeuralNet(request)
        return_data = [{"status": "ok", "result": "ok"}]
        return Response(return_data)

    def get(self, pk):
        return Response("get")

    def put(self, request, pk, format=None):
        return Response("put")

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