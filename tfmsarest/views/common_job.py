
from tfmsacore import netconf
from tfmsacore import service
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class CommonJobInfo(APIView):
    """
    1. POST :
    2. GET :
    3. PUT :
    4. DELETE :
    """
    def post(self, request, nnid):
        """
        set the time on the job
        :param request:
        :return:
        """
        try:
            result = service.JobStateLoader().set_request_time(nnid, json.loads(str(request.body, 'utf-8')))
            return_data = {"status": "200", "result": str(result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        get all job list
        :param request:
        :return:
        """
        try:
            result = service.JobStateLoader().get_all()
            list_result = [obj.json() for obj in result]
            return_data = {"status": "200", "result": json.dumps(list_result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        set the time on the job
        :param request:
        :return:
        """
        try:
            result = service.JobStateLoader().set_request_time(nnid, json.loads(str(request.body, 'utf-8')))
            return_data = {"status": "200", "result": str(result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        stop the job on the list
        :param request:
        :return:
        """
        try:
            result = service.JobStateLoader().set_pend(nnid)
            return_data = {"status": "200", "result": str(result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))