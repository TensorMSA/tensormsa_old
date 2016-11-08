import json

from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore import netconf

class ConvNeuralNetConfig(APIView):
    """
    1. Name : ConvNeuralNetConfig
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
        set cnn conf data 
    """
    def post(self, request, nnid):
        """
        - desc : insert cnn configuration data
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
        - desc : get cnn configuration data
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
        - desc ; update cnn configuration data
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
        - desc : delete cnn configuration data
        """
        try:
            jd = jc.load_obj_json("{}")
            jd.config = ""
            jd.nn_id = nnid
            netconf.update_network(jd)
            netconf.remove_conf(nnid)
            netconf.remove_trained_data(nnid)
            return_data = {"status": "200", "result": str(nnid)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

