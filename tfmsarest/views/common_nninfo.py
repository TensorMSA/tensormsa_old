from tfmsacore import train
from tfmsacore import predict
from tfmsacore import data
from tfmsacore import utils
from tfmsacore import netconf
from tfmsarest import livy
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class CommonNetInfo(APIView):
    """
    1. Name : CommonNetInfo (step 2)
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
        Manage Neural Network information. Include business category, description, netconf, data info, tarin result etc
    """
    def post(self, request):
        """
        - Request json data example \n
        <texfied>
        <font size = 1>

            {
                 "nn_id": "nn0000012",
                 "category": "MES",
                 "subcate" : "M60",
                 "name": "evaluation",
                 "desc" : "wdnn_protoType"
             }
        </font>
        </textfield>
        ---
        parameters:
        - name: body
          paramType: body
          pytype: json
        """
        try:
            result = netconf.create_new_network(json.loads(str(request.body, 'utf-8')))
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid, cate, sub):
        """
        - desc : return nn_info data
        """
        try:
            result = netconf.filter_network_config(nnid, cate, sub)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        - Request json data example \n
        <texfied>
        <font size = 1>

            {
                 "nn_id": "nn0000012",
                 "category": "MES",
                 "subcate" : "M60",
                 "name": "evaluation",
                 "desc" : "wdnn_protoType"
             }
        </font>
        </textfield>
        ---
        parameters:
        - name: body
          paramType: body
          pytype: json
        """
        try:
            jd = jc.load_obj_json(request.body)
            result = netconf.update_network(jd)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request):
        """
        - desc: delete selected nn_info data
        """
        try:
            result = netconf.delete_net_info(json.loads(request.body))
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))