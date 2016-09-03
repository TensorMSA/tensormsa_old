from django.shortcuts import render

# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from TensorMSACoreModule.tensor_msa_common import TensorIris



class TensorTest1(APIView):
    def get(self, pk):
        print("=================================")
        tensor = TensorIris()
        tensor.iris_simple()
        print(tensor.score)
        print("=================================")
        return Response(tensor.score)


class TensorTest2(APIView):
    def get(self, pk):
        print("=================================")
        tensor = TensorIris()
        tensor.iris_train_save()
        print(tensor.score)
        print("=================================")
        return Response(tensor.score)

class TensorTest3(APIView):
    def get(self, pk):
        print("=================================")
        tensor = TensorIris()
        tensor.iris_predict()
        print(tensor.predict)
        print("=================================")
        return Response(tensor.predict)
