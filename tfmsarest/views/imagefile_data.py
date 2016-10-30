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
    def post(self, request, baseid, tb, label):
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
                file_set = request.FILES.getlist('file')

                for file in file_set:
                    filename = "{0}-{1}".format(str(random.randrange(1,9999)) , file._name)
                    data.ImageManager().put_data(baseid, tb, label, file, filename)
            return_data = {"status": "ok", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid, tb, label):
        """
        - desc : get image file list \n
        """
        try:
            result = data.ImageManager().search_label(baseid, tb, label)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, tb, label):
        """
        - load image byte array \n
        <textfield>
        <font size = 1>

            [<file1>, <file2>]
        </font>
        </textfield>
        ---
        parameters:
        - name: body
          paramType: body
          pytype: json
        """
        try:
            file_set = json.loads(request.body)
            result = data.ImageManager().load_data(baseid, tb, label, file_set)
            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


    def delete(self, request, baseid, tb, label, file):
        """
        - desc : delete request file
        """
        try:
            data.ImageManager().delete_data(baseid, tb, label, file)
            return_data = {"status": "ok", "result": file}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))