import json
import json, os
from rest_framework.response import Response
from rest_framework.views import APIView
from TensorMSA import const
from tfmsacore import service
from tfmsacore.evaluation import wdnn_eval
from tfmsacore.utils import CusJsonEncoder,logger
from django.conf import settings
from tfmsacore import data
import decimal
#from django.core.serializers.json import DjangoJSONEncoder
import pickle
from json import JSONEncoder, JSONDecoder


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
            # if 'file' in request.FILES:
            #     file = request.FILES['file']
            #     filename = file._name
            #
            #     # save file on file system
            #     directory = "{0}/{1}/{2}".format(settings.FILE_ROOT, "predict", nnid)
            #     print("wide&dnn predict using csv  " + directory)
            #     if not os.path.exists(directory):
            #         os.makedirs(directory)
            #     fp = open("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, "predict", nnid, filename), 'wb')
            #     for chunk in file.chunks():
            #         fp.write(chunk)
            #     fp.close()

                # update to hdfs
                #results_data = data.DataMaster().save_csv_to_df(baseid, tb, filename)
                # print("where is error")
                # delete file after upload
                # if os.path.isfile("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename)):
                #    os.remove("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, baseid, tb, filename))
                # fp.close()
                # logger.tfmsa_logger("finish uploading csv on file system")
                #return HttpResponse(json.dumps(results_data))


            result = wdnn_eval().wdd_eval(nnid)
            print("return results %s" % type(result))
            #return_data = json.dumps(result,cls=PythonObjectEncoder)
            return_data = json.dumps(result)
            #return_data = {"status": "200", "result": ""}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


#
# class PythonObjectEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
#             return JSONEncoder.default(self, obj)
#         return {'_python_object': pickle.dumps(obj)}
