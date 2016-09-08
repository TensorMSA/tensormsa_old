from django.shortcuts import render

# Create your views here.

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Personal contribution check
#
# class TensorTest1(APIView):
#     def get(self, pk):
#         tensor = TensorIris()
#         tensor.iris_simple()
#         print(tensor.score)
#         return Response(tensor.score)
#
#
# class TensorTest2(APIView):
#     def get(self, pk):
#         tensor = TensorIris()
#         tensor.iris_train_save()
#         print(tensor.score)
#         return Response(tensor.score)
#
# class TensorTest3(APIView):
#     def get(self, pk):
#         tensor = TensorIris()
#         tensor.iris_predict()
#         print(tensor.predict)
#         return Response(tensor.predict)
