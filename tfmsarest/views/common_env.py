from tfmsacore import train
from tfmsacore import predict
from tfmsacore import data
from tfmsacore import utils
from tfmsacore import netconf
from tfmsarest import livy
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class CommonEnvInfo(APIView):
    """
    1. POST : start selected server
    2. GET : get server status (spark, livy, tensormsa, hdfs, s3 )
    3. PUT : restart selected server
    4. DELETE :stop seleted server
    """
    """
    TO-DO : Server Setting reloated REST API need to be done
    """
    def post(self, request):
        """
        insert neural net info
        :param request:
        :return:
        """
        try:
            return_data = {"status": "200", "result": str("")}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, cate, sub):
        """
        get  neural network information
        :param request:
        :return:
        """
        try:
            return_data = {"status": "200", "result": str("")}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        put neural network information
        :param request:
        :return:
        """
        try:
            return_data = {"status": "200", "result": str("")}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request):
        """
        get  neural network information
        :param request:
        :return:
        """
        try:
            return_data = {"status": "200", "result": str("")}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))