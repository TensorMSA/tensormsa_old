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


class CommonLivySession(APIView):
    """
    1. POST :
    2. GET :
    3. DELETE :
    """
    def post(self, request):
        """
        insert neural net info
        :param request:
        :return:
        """
        try:
            livy_client = livy.LivyDfClientManager()
            livy_client.create_session()
            return_data = {"status": "200", "result": str(livy_client.alive_sess_cnt)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        get  neural network information
        :param request:
        :return:
        """
        try:
            livy_client = livy.LivyDfClientManager()
            livy_client.check_alive_sessions()
            return_data = {"status": "200", "result": str(livy_client.alive_sess_list)}
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
            livy_client = livy.LivyDfClientManager()
            livy_client.delete_all_session()
            return_data = {"status": "200", "result": "0"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))