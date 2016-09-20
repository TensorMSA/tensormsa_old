from rest_framework.views import APIView
from rest_framework.response import Response
from tfmsacore.service.tfmsa import TFMsa
from tfmsarest import livy
from tfmsacore.data.json_conv import JsonDataConverter as jc
import json



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
            result = tfmsa.createDataFrame(jd.nn_id, jd.table, jd.data)
            print(result)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = {"status": "404", "result": e}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        select data form spark table
        :param request: request data
        :return: query result on json form (list - dict)
        """
        try:
            jd = jc.load_obj_json(request.body)
            livy_client = livy.LivyDfClientManager(2)
            livy_client.create_session()
            result = livy_client.query_data(jd.table, jd.query)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = {"status": "404", "result": e}
            return Response(json.dumps(return_data))

    def put(self, request, pk, format=None):
        """
        append data on the spark table
        :param request: request data
        :return: create table success or failure
        """
        try:
            jd = jc.load_obj_json(request.body)
            livy_client = livy.LivyDfClientManager(2)
            livy_client.create_session()
            result = livy_client.append_data(jd.table, jd.data)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = {"status": "404", "result": e}
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")