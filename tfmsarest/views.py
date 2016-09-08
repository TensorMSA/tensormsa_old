from django.shortcuts import render

# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tfmsacore.service.tfmsa import TFMsa

# Personal contribution check

class CNN_Service(APIView):
    """
    TO-DO : Dev Rest Services for CNN (predict, train, etc)
    """
    def get(self, pk):
        result = TFMsa().predictNerualNetwork("cnn", "sample")
        return Response(result)

    def put(self, request, pk, format=None):
        result = TFMsa().trainNerualNetwork("cnn", "sample", "local")
        return Response(result)

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")


class CNN_Config(APIView):
    """
    TO-DO : Dev Rest Services for CNN config change
    """
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
    def get(self, pk):
        return Response("get")

    def put(self, request, pk, format=None):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")