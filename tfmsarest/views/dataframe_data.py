import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsarest import livy


class DataFrameData(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, baseid, tb, args):
        """
        insert data into table
        :param request: request data
        :return: create table success or failure
        """
        try:
            if(args == "JSON"):
                jd = jc.load_obj_json(request.body)
                conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
                livy_client = livy.LivyDfClientManager()
                livy_client.create_session()
                livy_client.create_table(baseid, tb, conf_data)
            elif(args == "CSV"):
                print("on development")

            else :
                raise Exception("not supported type")

            return_data = {"status": "ok", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid, tb, args = None):
        """
        select data form spark table
        :param request: request data
        :return: query result on json form (list - dict)
        """
        try:
            livy_client = livy.LivyDfClientManager()
            livy_client.create_session()
            if(args == None):
                result = livy_client.query_data(baseid, tb, "select * from " + str(tb))
            else:
                result = livy_client.query_data(baseid, tb, args)

            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, tb, args = None):
        """
        append data on the spark table
        :param request: request data
        :return: create table success or failure
        """
        try:
            if (args == "JSON"):
                jd = jc.load_obj_json(request.body)
                conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
                livy_client = livy.LivyDfClientManager()
                livy_client.create_session()
                livy_client.append_data(baseid, tb, conf_data.replace("\"","'"))

            elif (args == "CSV"):
                print("on development")

            else:
                raise Exception("not supported type")

            return_data = {"status": "ok", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

