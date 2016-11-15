import json

from tfmsacore.preprocess.image_preprocess import ImagePreprocess
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore import predict
from tfmsacore.utils import file_util
from tfmsacore import netconf

class ConvNeuralNetPredict(APIView):
    """
    1. Name : ConvNeuralNetPredict
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
        Predict Label with image data
    """

    def put(self, request, nnid):
        """
        - desc : predict image with byte array
        """
        try:
            result = predict.predict_conv_network(nnid, json.loads(str(request.body, 'utf-8')))
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))


    def post(self, request, nnid):
        """
        - desc : predict image with file upload
        """
        try:
            conf = netconf.load_format(nnid)
            paths = file_util.save_upload_file(request)
            pre_img = []
            for path in paths :
                pre_img.append(ImagePreprocess().simple_resize(path, conf.x_size, conf.y_size))
                file_util.delete_upload_file(path)
            result = predict.predict_conv_network(nnid, pre_img)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))