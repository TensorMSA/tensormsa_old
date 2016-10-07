import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder
from tfmsacore import data


class DataFrameTable(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, baseid, tb):
        """
        create table with given name
        :param request: Not used
        :param baseid: schemaId
        :return: create schema result
        """
        try:
            result = data.HadoopManager().create_table(baseid, tb)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid):
        """
        return all table
        :param request: Not used
        :param baseid: schemaId
        :return: list of table
        """
        try:
            result = data.HadoopManager().search_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid):
        """
        rename table
        :param request: {origin : , modify : }
        :return: renamed table name
        """
        try:
            json_data = json.loads(request.body)
            result = data.HadoopManager().rename_table(baseid, json_data['origin'], json_data['modify'])
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid, tb):
        """
        delete table
        :param request: request data
        :return: renamed table name
        """
        try:
            result = data.HadoopManager().delete_table(baseid, tb)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

