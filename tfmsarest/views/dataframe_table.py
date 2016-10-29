import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder
from tfmsacore import data


class DataFrameTable(APIView):
    """
    1. Name : DataFrameTable (step 4)
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
        Manage data store table (strucutre : schema - table - data)
    """
    def post(self, request, baseid, tb):
        """
        - desc :create table with given name
        """
        try:
            result = data.HbaseManager().create_table(baseid, tb)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid):
        """
        - desc : return all table
        """
        try:
            result = data.HbaseManager().search_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid):
        """
        - desc : rename table
        - Request json data example \n
        <texfield>
            <font size = 1>

                {"origin" : "A" ,
                 "modify" : "B"}
            </font>
        </textfield>
            ---
            parameters:
            - name: body
              paramType: body
              pytype: json
        """
        try:
            json_data = json.loads(request.body)
            result = data.HbaseManager().rename_table(baseid, json_data['origin'], json_data['modify'])
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid, tb):
        """
        -desc : delete table
        """
        try:
            result = data.HbaseManager().delete_table(baseid, tb)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

