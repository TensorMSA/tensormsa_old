import json

from rest_framework.response import Response
from rest_framework.views import APIView

from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class CNN_Service(APIView):
    """
    TO-DO : Dev Rest Services for CNN (predict, train, etc)
    """

    def post(self, request):
        """
        train requested model and save
        :param request: json={ "nn_id": "sample" ,
                               "nn_type" : "cnn",
                               "run_type" : "local",
                               "epoch" : 50,
                               "testset" : 10 ,
                               "predict_data":""})
        :return: {"status": "", "result": ""}
        """
        try:
            jd = jc.load_obj_json(request.body)
            result = TFMsa().trainNerualNetwork(jd.nn_id, jd.nn_type, jd.run_type, jd.epoch, jd.testset)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    # read
    def get(self, request):
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
            result = TFMsa().predictNerualNetwork(jd.nn_id, jd.nn_type, jd.run_type, jd.predict_data)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    # update
    def put(self, request):
        """
        train requested model and save
        :param request: json={ "nn_id": "sample" ,
                               "nn_type" : "cnn",
                               "run_type" : "local",
                               "epoch" : 50,
                               "testset" : 10 ,
                               "predict_data":""})
        :return: {"status": "", "result": ""}
        """
        try:
            jd = jc.load_obj_json(request.body)
            result = TFMsa().trainNerualNetwork(jd.nn_id, jd.nn_type, jd.run_type, jd.epoch, jd.testset)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    # delete
    def delete(self, request, pk, format=None):
        return Response("delete")