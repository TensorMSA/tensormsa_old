import json, os
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder,logger
from tfmsacore import data

class ImageFilePreview(APIView):

    def get(self, request, nnid):
        """
        - desc : get image file list \n
        """
        try:
            result = data.ImageManager().get_preview_list(nnid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
