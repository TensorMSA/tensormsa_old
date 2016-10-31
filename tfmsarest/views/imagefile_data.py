import json, os
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder,logger
from tfmsacore import data
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsarest import livy
from django.conf import settings
from TensorMSA import const
import random

class ImageFileData(APIView):
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
        Manage data store data CRUD (strucutre : schema - table - data)
    """
    def post(self, request, baseid, table, label):
        """
        - desc : insert data into table
        - Request json data example \n
            <texfied>
            <font size = 1>

               <form action="/api/v1/type/dataframe/base/scm/table/tb_test_incomedata_wdnn3/data/CSV/"
                     method="post"
                     enctype="multipart/form-data">
            </font>
            </textfield>
            ---
            parameters:
            - name: body
              paramType: body
              pytype: json
        """
        try:
            logger.tfmsa_logger("start uploading image on hdfs")
            if 'file' in request.FILES:
                data_count = data.ImageManager().put_data(baseid, table , label, request.FILES.getlist('file'))
            return_data = {"status": "200", "result": data_count}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid, table, label):
        """
        - desc : get image file list \n
        """
        try:
            result = data.ImageManager().search_database(baseid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, table, label):
        """
        - load image byte array \n
        <textfield>
        <font size = 1>

            [<from>, <to>]
        </font>
        </textfield>
        ---
        parameters:
        - name: body
          paramType: body
          pytype: json
        """
        try:
            pointer = json.loads(str(request.body, 'utf-8'))
            result = data.ImageManager().load_data(baseid, table, pointer[0], pointer[1])
            return_data = {"status": "200", "result": result}
            return Response(result)
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))