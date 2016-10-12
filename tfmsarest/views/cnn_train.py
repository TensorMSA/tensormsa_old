import json

from rest_framework.response import Response
from rest_framework.views import APIView
from TensorMSA import const
from tfmsacore import service

class ConvNeuralNetTrain(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """

    def post(self, request, nnid):
        """
        train requested model and save
        :param request: json={ "type" : "local",
                               "epoch" : 50,
                               "testset" : 10 })
        :return: {"status": "", "result": ""}
        """
        try:
            json_data = json.loads(request.body)
            result = service.JobManager().regit_job(nnid, const.JOB_TYPE_CNN_TRAIN,
                                                    {"epoch" : json_data['epoch'],"testset" : json_data['testset']})
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
