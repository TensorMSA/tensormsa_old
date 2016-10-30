import json
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import data
from TensorMSA import const


class ImageFileSchema(APIView):
    """
    1. Name : ImageDataSchema (step 3)
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
        Imagedata schema management
    """
    def post(self, request, baseid):
        """
        - desc : create data base with given name
        """
        try:
            result = data.ImageManager().create_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        - desc : return all database names
        """
        try:
            result = data.ImageManager().search_all_database()
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request):
        """
        - desc : change database names
        - Request json data example \n
            <texfied>
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
            result = data.DataMaster(const.DATA_STORE_TYPE_IMAGE).rename_database(json_data['origin'], json_data['modify'])
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, baseid):
        """
        - desc : delete database
        """
        try:
            result = data.DataMaster(const.DATA_STORE_TYPE_IMAGE).delete_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

