from django.shortcuts import render

# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tfmsacore.service.tfmsa import TFMsa
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
        req_data = json.loads(request.body)
        result = TFMsa().trainNerualNetwork("cnn", req_data["nn_id"], "local")
        return_data = [{"status": "ok", "result": result}]
        print(json.dumps(return_data))
        return Response(json.dumps(return_data))

    # read
    def get(self, pk):
        #result = TFMsa().predictNerualNetwork("cnn", "sample")
        return_data = [{"status":"ok" , "result":"on dev"}]
        print(json.dumps(return_data))
        return Response(json.dumps(return_data))

    # update
    def put(self, request):
        req_data = json.loads(request.body)
        result = TFMsa().trainNerualNetwork("cnn", req_data["nn_id"], "local")
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