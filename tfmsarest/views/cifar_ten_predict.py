import json

from tfmsacore.preprocess.image_preprocess import ImagePreprocess
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import predict
from tfmsacore.utils import file_util
from tfmsacore import netconf
from tfmsacore.extension import cifar10

class CifarTenPredict(APIView):


    def post(self, request):
        """
        - desc : predict image with file upload
        """
        try:
            path = file_util.save_upload_file(request)
            result = cifar10.s_predict_file(path, "path")
            file_util.delete_upload_file(path)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))