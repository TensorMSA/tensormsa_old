from tfmsacore import service
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView



class CommonEnvInfo(APIView):
    """
    1. POST :
    2. GET :
    3. PUT :
    4. DELETE :
    """

    def post(self, request):
        """
        insert new server conf and disable current setting
        :param request:
        :return:
        """
        try:
            service.ServerConfLoader().post(json.loads(request.body))
            return_data = {"status": "200", "result": str("")}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request):
        """
        get current server settingss
        :param request:
        :return:
        """
        try:
            return_data = service.ServerConfLoader().get()
            return_data = {"status": "200", "result": str(return_data)}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))
