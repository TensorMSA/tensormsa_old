import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import validation
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class ConvNeuralNetChecker(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """

    # read
    def post(self, request, nnid):
        """
        train requested model and save
        :param request: json={ "nn_id": "sample" ,
                               "nn_type" : "cnn",
                               "run_type" : "local",
                               "epoch" : 50,
                               "testset" : 10 ,
                               "predict_data":<essential>})
        :return: {"status": "", "result": [[]]}
        """
        try:
            print("!!!!!!!!!!!!!")
            print(nnid)
            jd = jc.load_obj_json(request.body)
            result = validation.CNNChecker().check_sequence(nnid)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


