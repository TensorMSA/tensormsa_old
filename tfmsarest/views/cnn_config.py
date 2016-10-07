import json

from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore import netconf

class ConvNeuralNetConfig(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, nnid):
        """
        insert new neural network information
        :param request:
        {
            "nn_info" : {  },
            "nn_conf" : {"data":{},
                         "layer":[{},]}
        }

        :return: registered network id
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.config = "Y"
            jd.nn_id = nnid
            netconf.update_network(jd)
            netconf.save_conf(nnid, request.body)
            return_data = {"status": "200", "result": nnid}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        insert new neural network information
        :param pk:
        :param request:
        :return: {
                    "data":{"datalen": 96,"taglen": 2,"matrix": [12, 8],"learnrate": 0.01,"epoch":50},
                    "layer":[{},{}]
                 }
        """
        try:
            result = netconf.load_ori_conf(nnid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, nnid):
        """
        insert new neural network information
        :param request:
        {
            "nn_info" : {  },
            "nn_conf" : {"data":{},
                         "layer":[{},]}
        }

        :return: registered network id
        """
        try:
            netconf.save_conf(nnid, json.dumps(request.body))
            return_data = {"status": "200", "result": nnid}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        delete selected net work conf
        :param request:
        :param pk: nn_id wanna delete
        :param format:
        :return:
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.config = ""
            jd.nn_id = nnid
            netconf.update_network(jd)
            netconf.remove_conf(nnid)
            netconf.remove_trained_data(nnid)
            return_data = {"status": "404", "result": str(nnid)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

