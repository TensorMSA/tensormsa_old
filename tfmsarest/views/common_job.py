
from tfmsacore import netconf
from tfmsacore import service
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from django.core import serializers as serial

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
            result = {}
            row = service.JobStateLoader().set_job_info(nnid, json.loads(str(request.body, 'utf-8')))
            result['epoch'] = row.epoch
            result['batchsize'] = row.batchsize
            result['status'] = row.status
            return_data = {"status": "200", "result": str(result)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        get all job list
        :param request:
        :return:
        """
        try:

            if(nnid == 'all'):
                result = service.JobStateLoader().get_all()
                result = serial.serialize("json", result)
                result = json.loads(result)
            else :
                result = {}
                row = service.JobStateLoader().get_selected_job_info(nnid)
                result['epoch'] = row.epoch
                result['batchsize'] = row.batchsize
                result['status'] = row.status
                
            return_data = {"status": "200", "result": result}
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