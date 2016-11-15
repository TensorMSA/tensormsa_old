import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import validation
from tfmsacore import netconf
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class ConvNeuralNetChecker(APIView):
    """
    1. Name : ConvNeuralNetChecker
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
        check simple net config checks
    """
    def post(self, request, nnid):
        """
        - desc : check net configuration
        """
        try:
            result = validation.CNNChecker().check_sequence(nnid)
            if(len(result) == 0):
                netconf.set_on_net_vaild(nnid)
                return_data = {"status": "200", "result": result}
            else :
                netconf.set_off_net_vaild(nnid)
                return_data = {"status": "400", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))


