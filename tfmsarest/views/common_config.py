from rest_framework.views import APIView
from rest_framework.response import Response
from tfmsacore.service.tfmsa import TFMsa
from tfmsarest import livy
from tfmsacore.data.json_conv import JsonDataConverter as jc
import json

class Common_config(APIView):
    """
    TO-DO : Dev Rest Services for CNN config change
    """
    def post(self, request):
        return Response("post")

    def get(self, request):
        """
        insert new neural network information
        :param request:
        :return:
        """
        try:
            tfmsa = TFMsa()
            jd = jc.load_obj_json(request.body)
            result = tfmsa.getNeuralNetConfig(jd.nn_id, jd.category)
            return_data = [{"status": "ok", "result": str(result)}]
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
            return Response(json.dumps(return_data))

    def put(self, request):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")