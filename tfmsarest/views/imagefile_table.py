import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import data
from TensorMSA import const


class ImageFileTable(APIView):
    """
    1. Name : ImageFileTable (step 4)
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
        Imagedata table management
    """
    def post(self, request, baseid, table):
        """
        - desc :create table with given name
        """
        try:
            result = data.ImageManager().create_table(baseid, table)
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
            result = data.ImageManager().search_database(baseid)
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
            result = data.ImageManager().rename_table(baseid, json_data['origin'], json_data['modify'])
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid, table):
        """
        -desc : delete table
        """
        try:
            result = data.ImageManager().delete_table(baseid, table)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

