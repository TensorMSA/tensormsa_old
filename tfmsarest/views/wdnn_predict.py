import json

from rest_framework.response import Response
from rest_framework.views import APIView
from TensorMSA import const
from tfmsacore import service
from tfmsacore import train


class WideDeepNetPredict(APIView):
    """
    1. POST :
    2. PUT :
    3. GET :
    4. DELETE :
    """

    def post(self, request, nnid):
        """
        predict
        :param networkid
        :return: {"status": "", "result": ""}
        """
        try:
            result = train.wdd_predict(nnid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
