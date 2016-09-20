import json

from rest_framework.response import Response
from rest_framework.views import APIView

from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.utils.json_conv import JsonDataConverter as jc


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
            return_data = {"status": "ok", "result": str(result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")