import json
from tfmsacore import netconf
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from TensorMSA import const
from tfmsacore import service


class DataFramePre(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, baseid, tb, nnid):
        """
        create table column distinct data
        :param request: Not used
        :param baseid: schemaId
        :return: create schema result
        """
        try:
            service.JobManager().regit_job(nnid, const.JOB_TYPE_DF_PRE_PROCESS)
            return_data = {"status": "200", "result": tb}
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
            return_data = {"status": "200", "result": result['datasets']}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, tb, nnid):
        """
        rename table
        :param request: {origin : , modify : }
        :return: renamed table name
        """
        try:
            service.JobManager().regit_job(nnid, const.JOB_TYPE_DF_PRE_PROCESS)
            return_data = {"status": "200", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid, tb, nnid):
        """
        delete distinct data
        :param request: request data
        :return: renamed table name
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.nn_id = nnid
            jd.datasets = ""
            result = netconf.update_network(jd)
            return_data = {"status": "200", "result": result}
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

