import json

from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore import netconf

class WideDeepNetConfig(APIView):
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
        - desc : insert new neural network information
        - Request json data example \n
        <texfield>
            <font size = 1>

               {
                    "layer":[100,50,20]
               }

        </textfield>
            ---
            parameters:
            - name: body
              paramType: body
              pytype: json
        """
        try:
            netconf.set_on_net_conf(nnid)
            netconf.save_conf(nnid, str(request.body, 'utf-8'))
            return_data = {"status": "200", "result": nnid}
            return Response(json.dumps(return_data))
        except Exception as e:
            netconf.set_off_net_conf(nnid)
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


    def get(self, request, nnid):
        """
        - desc : insert new neural network information
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
        - desc : insert new neural network information
        """
        try:
            netconf.save_conf(nnid, json.dumps(str(request.body, 'utf-8')))
            return_data = {"status": "200", "result": nnid}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        -desc : delete selected net work conf
        """
        try:
            netconf.set_off_net_conf(nnid)
            netconf.remove_conf(nnid)
            netconf.remove_trained_data(nnid)
            return_data = {"status": "404", "result": str(nnid)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

