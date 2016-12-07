import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import validation
from tfmsacore import netconf
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class WideAndDeepNetChecker(APIView):
    """
    1. Name : WideDeepNetConfig (step 7)
    2. Steps - WDNN essential steps
        - post /api/v1/type/common/env/
        - post /api/v1/type/common/job/{nnid}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/{args}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/format/{nnid}/
        - post /api/v1/type/wdnn/conf/{nnid}/
        - post /api/v1/type/wdnn/train/{nnid}/
        - post /api/v1/type/wdnn/eval/{nnid}/
        - post /api/v1/type/wdnn/predict/{nnid}/
    3. Description \n
        Manage data store data CRUD (strucutre : schema - table - data)
    """
    def post(self, request, nnid):
        """
        - desc : check net configuration
        """
        try:
            netconf.set_on_net_vaild(nnid)
            return_data = {"status": "200", "result": "200"}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))


