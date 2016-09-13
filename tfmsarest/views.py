from rest_framework.views import APIView
from rest_framework.response import Response
from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.data.json_conv import JsonDataConverter as jc
import json


"""
TO-DO : design api rules
"""

"""
TO-DO : adjust security keys
"""
# Personal contribution check
# http://www.django-rest-framework.org/api-guide/testing/
# https://realpython.com/blog/python/api-integration-in-python/
# http://www.slideshare.net/Byungwook/rest-api-60505484

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
            return_data = [{"status": "200", "result": result}]
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
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
            return_data = [{"status": "ok", "result": result}]
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
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
            return_data = [{"status": "ok", "result": result}]
            print(json.dumps(return_data))
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
            return Response(json.dumps(return_data))

    # delete
    def delete(self, request, pk, format=None):
        return Response("delete")


class CNN_Config(APIView):
    """
    TO-DO : Dev Rest Services for CNN config change
    """
    def post(self, request):
        """
        insert new neural network information
        :param request:
        {
            "nn_info" : {  "nnid": "sample",
                            "category":"test",
                            "name" : "test",
                            "type" : "cnn",
                            "acc" : "",
                            "train" : "",
                            "config" : "",
                            "dir" : "default"},
            "nn_conf" : {
                            "data":
                                {
                                    "datalen": 96,
                                    "taglen": 2,
                                    "matrix": [12, 8],
                                    "learnrate": 0.01,
                                    "epoch":50
                                },
                            "layer":
                                [
                                    {
                                        "type": "input",
                                        "active": "relu",
                                        "cnnfilter": [2, 2],
                                        "cnnstride": [1, 1],
                                        "maxpoolmatrix": [2, 2],
                                        "maxpoolstride": [1, 1],
                                        "node_in_out": [1, 16],
                                        "regualizer": "",
                                        "padding": "SAME",
                                        "droprate": ""
                                    },
                                ]
                            }
        }

        :return: registered network id
        """
        try:
            jd = jc.load_obj_json(request.body)
            tfmsa = TFMsa()
            result = tfmsa.createNeuralNetwork(jd.nn_info, jd.nn_conf)
            return_data = [{"status": "ok", "result": result}]
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        insert new neural network information
        :param request:
        {
            "nn_info" : {  "nnid": "sample",
                            "category":"test",
                            "name" : "test",
                            "type" : "cnn",
                            "acc" : "",
                            "train" : "",
                            "config" : "",
                            "dir" : "default"},
        }

        :return: {
                    "data":
                        {
                            "datalen": 96,
                            "taglen": 2,
                            "matrix": [12, 8],
                            "learnrate": 0.01,
                            "epoch":50
                        },
                    "layer":
                        [
                            {
                                "type": "input",
                                "active": "relu",
                                "cnnfilter": [2, 2],
                                "cnnstride": [1, 1],
                                "maxpoolmatrix": [2, 2],
                                "maxpoolstride": [1, 1],
                                "node_in_out": [1, 16],
                                "regualizer": "",
                                "padding": "SAME",
                                "droprate": ""
                            },
                        ]
                    }
        """
        try:
            tfmsa = TFMsa()
            jd = jc.load_obj_json(request.body)
            result = tfmsa.searchNeuralNetwork(jd.nn_info)
            return_data = [{"status": "ok", "result": result}]
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        insert new neural network information
        :param request:
        {
            "nn_info" : {  "nnid": "sample",
                            "category":"test",
                            "name" : "test",
                            "type" : "cnn",
                            "acc" : "",
                            "train" : "",
                            "config" : "",
                            "dir" : "default"},
            "nn_conf" : {
                            "data":
                                {
                                    "datalen": 96,
                                    "taglen": 2,
                                    "matrix": [12, 8],
                                    "learnrate": 0.01,
                                    "epoch":50
                                },
                            "layer":
                                [
                                    {
                                        "type": "input",
                                        "active": "relu",
                                        "cnnfilter": [2, 2],
                                        "cnnstride": [1, 1],
                                        "maxpoolmatrix": [2, 2],
                                        "maxpoolstride": [1, 1],
                                        "node_in_out": [1, 16],
                                        "regualizer": "",
                                        "padding": "SAME",
                                        "droprate": ""
                                    },
                                ]
                            }
        }

        :return: registered network id
        """
        try:
            tfmsa = TFMsa()
            jd = jc.load_obj_json(request.body)
            result = tfmsa.updateNeuralNetwork(jd.nn_info, jd.nn_conf)
            return_data = [{"status": "ok", "result": result}]
            return Response(json.dumps(return_data))
        except SystemError as e:
            return_data = [{"status": "404", "result": e}]
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")

class CNN_Data(APIView):
    """
    TO-DO : Dev Rest Services for CNN Test, Train Datas
    """
    def post(self, request, pk, format=None):
        return Response("post")

    def get(self, pk):
        return Response("get")

    def put(self, request, pk, format=None):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")

class CNN_Stastics(APIView):
    """
    TO-DO : Dev Rest Services for CNN Accuracy , Data, Response, etc
    """
    def post(self, request, pk, format=None):
        return Response("post")

    def get(self, pk):
        return Response("get")

    def put(self, request, pk, format=None):
        return Response("put")

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")