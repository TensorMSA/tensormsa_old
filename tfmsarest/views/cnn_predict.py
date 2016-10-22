import json

from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import predict
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class ConvNeuralNetPredict(APIView):
    """
    1. Name : ConvNeuralNetPredict (step 10)
    2. Steps - CNN essential steps
        - post /api/v1/type/common/env/
        - post /api/v1/type/common/job/{nnid}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/{args}/
        - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/format/{nnid}/
        - post /api/v1/type/cnn/conf/{nnid}/
        - post /api/v1/type/cnn/train/{nnid}/
        - post /api/v1/type/cnn/eval/{nnid}/
        - post /api/v1/type/cnn/predict/{nnid}/
    3. Description \n
        Manage data store schema (strucutre : schema - table - data)
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
            jd = jc.load_obj_json(request.body)
            result = predict.predict_conv_network(nnid, jd)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
