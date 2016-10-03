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


class CommonNetInfo(APIView):
    """
    1. POST : Insert network base info
    2. GET : Search network base info (id, cate, subcate)
    3. PUT : Update selected network base info
    4. DELETE :Delete selected network base info
    """
    def post(self, request):
        """
        insert neural net info
        :param request:
        :return:
        """
        try:
            result = netconf.create_new_network(json.loads(request.body))
            return_data = {"status": "200", "result": str(result)}
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
            result = netconf.filter_network_config(nnid, cate, sub)
            return_data = {"status": "200", "result": str(result)}
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
            jd = jc.load_obj_json(request.body)
            result = netconf.update_network(jd)
            return_data = {"status": "200", "result": str(result)}
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
            result = netconf.delete_net_info(json.loads(request.body))
            return_data = {"status": "200", "result": str(result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))