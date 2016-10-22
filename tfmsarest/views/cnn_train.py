import json

from rest_framework.response import Response
from rest_framework.views import APIView
from TensorMSA import const
from tfmsacore import service

class ConvNeuralNetTrain(APIView):
    """
    1. Name : ConvNeuralNetPredict (step 10)
    2. Steps - CNN essential steps
        - post /api/v1/type/common/env/
        - post /api/v1/type/common/job/{nnid}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/{args}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/format/{nnid}/
        - post /api/v1/type/cnn/conf/{nnid}/
        - post /api/v1/type/cnn/train/{nnid}/
        - post /api/v1/type/cnn/eval/{nnid}/
        - post /api/v1/type/cnn/predict/{nnid}/
    3. Description \n
        Manage data store schema (strucutre : schema - table - data)
    """

    def post(self, request, nnid):
        """
        - desc : train requested model and save
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
