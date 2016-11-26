import json, os
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder,logger
from tfmsacore import data
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from django.conf import settings

class DataFrameData(APIView):
    """
    1. Name : DataFrameData (step 5)
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
    def post(self, request, baseid, tb, args):
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
            if(args == "JSON"):
                jd = jc.load_obj_json(str(request.body, 'utf-8'))
                conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
                data.HbaseManager().post_josn_data(baseid, tb, conf_data)

            elif(args == "CSV"):
                logger.tfmsa_logger("start uploading csv on file system")
                results_data = ""
                if len(request.FILES.keys()) > 0:
                    #loop files
                    for key, requestSingileFile in request.FILES.items():
                        file = requestSingileFile
                        filename = file._name

                        # save file on file system
                        directory = "{0}/{1}/{2}".format(settings.FILE_ROOT, baseid, tb)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        fp = open("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename), 'wb')
                        for chunk in file.chunks():
                            fp.write(chunk)
                        fp.close()
                        logger.tfmsa_logger("Before calling save csv_to df")
                        results_data = data.HbaseManager().save_csv_to_df(baseid, tb, filename)
                    else :
                        raise Exception("not supported type")

            return_data = {"status": "200", "result": results_data}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid, tb, args = None):
        """
        - desc : select data form spark table
        """
        try:
            limit = 0 #limits_t["limits"]
            if(args == None):
                result = data.HbaseManager().query_data(baseid, tb, "", args ,  int(limit))
            else:
                result = data.HbaseManager().query_data(baseid, tb, "", args,  int(limit))

            return_data = {"status": "200", "result": result}

            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, tb, args = None):
        """
        - desc : append data on the spark table
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
        """
        try:
            if (args == "JSON"):
                jd = jc.load_obj_json(str(request.body, 'utf-8'))
                conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
                data.HbaseManager().put_josn_data(baseid, tb, conf_data)

            elif (args == "CSV"):
                logger.tfmsa_logger("start uploading csv on file system")
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    filename = file._name

                    #save upload file on file system
                    directory = "{0}/{1}/{2}".format(settings.FILE_ROOT, baseid, tb)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    fp = open("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename), 'wb')
                    for chunk in file.chunks():
                        fp.write(chunk)
                    fp.close()

                    #upload data to hdfs
                    cols = data.HbaseManager().save_csv_to_df(baseid, tb, filename)
                    return HttpResponse('File Uploaded')

            else:
                raise Exception("not supported type")

            return_data = {"status": "200", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

