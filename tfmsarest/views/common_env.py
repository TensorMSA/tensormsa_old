from tfmsacore import service
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView



class CommonEnvInfo(APIView):
    """
    1. Name : CommonEnvInfo (step 1)
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
        Server configuraiton management, for now except fw_capa non of the values are
        used yet. server config management views are planned to support in 2017

    """

    def post(self, request):
        """
        - Request json data example \n
        <texfied>
        <font size = 1>

            {'state': 'A',
            'store_type': '1',
            'fw_capa' : '1',
            'livy_host' : '8ea172cae00f:8998' ,
            'livy_sess' : '1',
            'spark_host' : '8ea172cae00f:7077',
            'spark_core': '1',
            'spark_memory': '1G',
            'hdfs_host': '587ed1df9441:9000',
            'hdfs_root': '/tensormsa',
            's3_host': '',
            's3_access': '',
            's3_sess': '',
            's3_bucket': '',
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
            service.ServerConfLoader().post(json.loads(str(request.body, 'utf-8')))
            return_data = {"status": "200", "result": str("")}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        get current server settingss
        :param request:
        :return:
        """
        try:
            return_data = service.ServerConfLoader().get()
            return_data = {"status": "200", "result": str(return_data)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))
