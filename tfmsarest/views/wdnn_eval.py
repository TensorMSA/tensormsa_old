import json, os
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.evaluation import wdnn_eval
from tfmsacore.utils import CusJsonEncoder,logger
from tfmsacore import netconf
from tfmsacore import service
from TensorMSA import const

class WideDeepNetEval(APIView):
    """
    1. Name : WideDeepNetPredict (step 10)
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
        - desc : predict result with given data
        - Request json data example \n
        <textfield>
            <font size = 1>

               [{"pclass": "1st","survived": "tag","sex": "female","age": "30","embarked": "Southampton","boat": "2"},
               {"pclass": "1st","survived": "tag","sex": "female","age": "30","embarked": "Southampton","boat": "2"},
               {"pclass": "1st","survived": "tag","sex": "female","age": "30","embarked": "Southampton","boat": "2"}]

        </textfield>
            ---
            parameters:
            - name: body
              paramType: body
              pytype: json
        """

        try:
            logger.tfmsa_logger("[eval] start evaluation in hbase")
            result = service.JobManager().regit_job(nnid, const.JOB_TYPE_WDNN_EVAL)
            return_data = json.dumps(result)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
