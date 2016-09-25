import json

from rest_framework.response import Response
from rest_framework.views import APIView

from tfmsacore.service.tfmsa import TFMsa
from tfmsacore.utils.json_conv import JsonDataConverter as jc


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
                            "table" : "TEST1",
                            "query" : "select * from TEST1",
                            "dataset":"{'name':'none', 'univ':'cate', 'eng' : 'cont', 'grade' : 'tag'}",
                            "dir" : "default"},
            "nn_conf" : {
                            "data":
                                {
                                    "datalen": 96,
                                    "taglen": 2,
                                    "matrix": [12, 8],
                          analizeDataFrame          "learnrate": 0.01,
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
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, pk):
        """
        insert new neural network information
        :param pk:
        :param request:
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
            result = tfmsa.searchNeuralNetwork(pk)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
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
                                                        "table" : "TEST1",
                            "query" : "select * from TEST1",
                            "dataset":"{'name':'none', 'univ':'cate', 'eng' : 'cont', 'grade' : 'tag'}",
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
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

    def get_object(self, pk):
        return Response("get_onject")