import json, os
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from tfmsacore.utils import CusJsonEncoder,logger
from tfmsacore import data

class ImageFileLabel(APIView):

    def post(self, request, nnid, label):
        """
        - desc : get image file list \n
        """
        try:
            result = data.ImageManager().update_label_list(nnid, label)
            return_data = {"status": "200", "result": result}
            print(json.dumps(return_data))
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, nnid):
        """
        - desc : post label info \n
        """
        try:
            result = data.ImageManager().get_label_list(nnid)
            return_data = {"status": "200", "result": result}
            print(json.dumps(return_data))
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, nnid):
        """
        - desc : delete label info \n
        """
        try:
            result = data.ImageManager().delete_preview_list(nnid)
            return_data = {"status": "200", "result": result}
            print(json.dumps(return_data))
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

