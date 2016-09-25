import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder
from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsarest import livy


class CNN_Data(APIView):
    """
    TO-DO : Dev Rest Services for CNN Test, Train Datas
    """
    def post(self, request):
        """
        create new table with new json data
        :param request: request data
        :return: create table success or failure
        """
        try:
            tfmsa = TFMsa()
            jd = jc.load_obj_json(request.body)
            conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
            result = tfmsa.createDataFrame(jd.nn_id, jd.table, conf_data.replace("\"","'"))
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, pk):
        """
        select data form spark table
        :param request: request data
        :return: query result on json form (list - dict)
        """
        try:
            livy_client = livy.LivyDfClientManager(2)
            livy_client.create_session()
            result = livy_client.query_data(pk, "select * from " + str(pk))
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        append data on the spark table
        :param request: request data
        :return: create table success or failure
        """
        try:

            jd = jc.load_obj_json(request.body)
            livy_client = livy.LivyDfClientManager(2)
            livy_client.create_session()
            conf_data = json.dumps(jd.data, cls= CusJsonEncoder)
            result = livy_client.append_data(jd.table, conf_data.replace("\"","'"))
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")