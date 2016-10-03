import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import train
from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.utils.json_conv import JsonDataConverter as jc


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
            train.train_conv_network(nnid, json_data['epoch'], json_data['testset'])
            return_data = {"status": "200", "result": nnid}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
