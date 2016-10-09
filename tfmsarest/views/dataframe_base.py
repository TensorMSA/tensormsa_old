import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import data



class DataFrameSchema(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, baseid):
        """
        create data base with given name
        :param request: Not used
        :param baseid: schemaId
        :return: create schema result
        """
        try:
            result = data.DataMaster().create_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        return all databases
        :param request: Not used
        :param baseid: schemaId
        :return: list of schemaa (database)
        """
        try:
            result = data.DataMaster().search_all_database()
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        rename data base
        :param request: {origin : , modify : }
        :return: renamed database name
        """
        try:
            json_data = json.loads(request.body)
            result = data.DataMaster().rename_database(json_data['origin'], json_data['modify'])
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid):
        """
        delete data base
        :param request: request data
        :return: renamed database name
        """
        try:
            result = data.DataMaster().delete_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

