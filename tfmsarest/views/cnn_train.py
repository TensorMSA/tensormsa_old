import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import netconf
from tfmsacore.train.conv_train import train_conv_network

class ConvNeuralNetTrain(APIView):
    """
    1. Name : ConvNeuralNetTrain
    2. Steps - CNN essential steps
        - post /api/v1/type/common/env/
        - post /api/v1/type/common/nninfo/{nnid}/
        - post /api/v1/type/imagedata/base/{baseid}/
        - post /api/v1/type/imagedata/base/{baseid}/table/{tb}/
        - post /api/v1/type/imagedata/base/{baseid}/table/{tb}/label/{label}/data/
        - post /api/v1/type/imagedata/base/{baseid}/table/{tb}/label/{label}/data/{args}/
        - post /api/v1/type/imagedata/base/{baseid}/table/{tb}/label/{label}/format/{nnid}/
        - post /api/v1/type/imagedata/base/{baseid}/table/{tb}/label/{label}/format/{nnid}/
        - post /api/v1/type/cnn/conf/{nnid}/
        - post /api/v1/type/cnn/train/{nnid}/
        - post /api/v1/type/cnn/eval/{nnid}/
        - post /api/v1/type/cnn/predict/{nnid}/
    3. Description \n
        Predict Label with image data
    """

    def post(self, request, nnid):
        """
        - desc : train requested model and save
        """
        try:
            json_data = json.loads(str(request.body, 'utf-8'))
            # result = service.JobManager().regit_job(nnid, const.JOB_TYPE_CNN_TRAIN,
            #                                         {"epoch" : json_data['epoch'],"testset" : json_data['testset']})
            result = train_conv_network(nnid)
            netconf.set_on_train(nnid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            netconf.set_off_train(nnid)
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
