import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore.evaluation import CNNEval
from tfmsacore.netconf.nn_common_manager import get_network_config


class ConvNeuralNetEval(APIView):
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
            jd = jc.load_obj_json(request.body)
            result = CNNEval().eval_model(nnid, jd.samplenum, jd.samplemethod)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


    def get(self, request, nnid):
        """
        return all databases
        :param request: Not used
        :param baseid: schemaId
        :return: list of schemaa (database)
        """
        try:
            result = get_network_config(nnid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))