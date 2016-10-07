import json, os
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder,logger
from tfmsacore import data
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsarest import livy
from django.conf import settings

class DataFrameData(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """
    def post(self, request, baseid, tb, args):
        """
        insert data into table
        :param request: request data
        :return: create table success or failure
        """
        try:
            if(args == "JSON"):
                jd = jc.load_obj_json(request.body)
                conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
                livy_client = livy.LivyDfClientManager()
                livy_client.create_session()
                livy_client.create_table(baseid, tb, conf_data)

            elif(args == "CSV"):
                logger.tfmsa_logger("start uploading csv on file system")
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    filename = file._name

                    # save file on file system
                    directory = "{0}/{1}/{2}".format(settings.FILE_ROOT, baseid, tb)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    fp = open("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename), 'wb')
                    for chunk in file.chunks():
                        fp.write(chunk)
                    fp.close()

                    #update to hdfs
                    data.CsvLoader().save_csv_to_df(baseid, tb, filename)

                    #delete file after upload
                    if os.path.isfile("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename)):
                        os.remove("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename))
                    fp.close()
                    logger.tfmsa_logger("finish uploading csv on file system")
                    return HttpResponse('File Uploaded')
            else :
                raise Exception("not supported type")

            return_data = {"status": "ok", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, baseid, tb, args = None):
        """
        select data form spark table
        :param request: request data
        :return: query result on json form (list - dict)
        """
        try:
            livy_client = livy.LivyDfClientManager()
            livy_client.create_session()
            if(args == None):
                result = livy_client.query_data(baseid, tb, "select * from " + str(tb))
            else:
                result = livy_client.query_data(baseid, tb, args)

            return_data = {"status": "ok", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, baseid, tb, args = None):
        """
        append data on the spark table
        :param request: request data
        :return: create table success or failure
        """
        try:
            if (args == "JSON"):
                jd = jc.load_obj_json(request.body)
                conf_data = json.dumps(jd.data, cls=CusJsonEncoder)
                livy_client = livy.LivyDfClientManager()
                livy_client.create_session()
                livy_client.append_data(baseid, tb, conf_data.replace("\"","'"))

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
                    data.CsvLoader().save_csv_to_df(baseid, tb, filename)

                    #delete file after upload
                    if os.path.isfile("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename)):
                        os.remove("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename))

                    fp.close()
                    logger.tfmsa_logger("finish uploading csv on file system")
                    return HttpResponse('File Uploaded')

            else:
                raise Exception("not supported type")

            return_data = {"status": "ok", "result": tb}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, pk, format=None):
        return Response("delete")

