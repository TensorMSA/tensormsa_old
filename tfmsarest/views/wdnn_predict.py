
import json, os
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import predict
from tfmsacore.utils import CusJsonEncoder,logger
from django.conf import settings

class WideDeepNetPredict(APIView):
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
            logger.tfmsa_logger("[Predict] start uploading csv on file system")
            logger.tfmsa_logger("start uploading csv on file system")
            print(request.FILES)

            if len(request.FILES.keys()) > 0:
                # loop files
                for key, requestSingileFile in request.FILES.items():
                    print("in the loop")
                    #print(requestSingileFile)
                    #print(key)
                    #print("multi error")
                    #print(file)
                    file = requestSingileFile
                    filename = file._name
                    #print(filename)
                    # save file on file system
                    directory = "{0}/{1}/{2}".format(settings.FILE_ROOT, "predict", nnid)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    fp = open("{0}/{1}/{2}/{3}".format(settings.FILE_ROOT, "predict", nnid, filename), 'wb')
                    for chunk in file.chunks():
                        fp.write(chunk)
                    fp.close()

            print("before predict")
            result = predict.wdnn_predict().wdd_predict(nnid,filename)

            print("return results %s" % type(result))
            #return_data = json.dumps(result,cls=PythonObjectEncoder)
            return_data = json.dumps(result)
            print(return_data)
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


