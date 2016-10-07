import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder
from tfmsacore import data
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore import netconf

class DataFrameFormat(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, baseid, tb, nnid):
        """
        create a format data
        :param request: update network info
        :param baseid: schemaId
        :param tb : table name
        :return: create schema result
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.dir = baseid
            jd.table = tb
            jd.nn_id = nnid
            jd.datadesc = request.body
            result = netconf.update_network(jd)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid, tb, nnid):
        """
        return all table
        :param request: Not used
        :param baseid: schemaId
        :return: list of table
        """
        try:
            result = netconf.get_network_config(nnid)
            return_data = {"status": "200", "result": result['datadesc']}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, tb, nnid):
        """
        same as create
        :param request: update network info
        :param baseid: schemaId
        :param tb : table name
        :return: create schema result
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.dir = baseid
            jd.table = tb
            jd.nn_id = nnid
            jd.datadesc = request.body
            result = netconf.update_network(jd)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid, tb, nnid):
        """
        delete table
        :param request: request data
        :return: renamed table name
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.dir = ""
            jd.table = ""
            jd.nn_id = nnid
            jd.datadesc = ""
            result = netconf.update_network(jd)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

