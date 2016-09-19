from rest_framework.views import APIView
from rest_framework.response import Response
from tfmsacore.service.tfmsa import TFMsa
from tfmsarest import livy
from tfmsacore.data.json_conv import JsonDataConverter as jc
import json


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