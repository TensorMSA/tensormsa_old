# import json
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from tfmsacore.utils.json_conv import JsonDataConverter as jc
# from tfmsacore.evaluation import CNNEval
# from tfmsacore.netconf.nn_common_manager import get_network_config
#
#
# class ConvNeuralNetEval(APIView):
#     """
#     1. Name : ConvNeuralNetEval (step 10)
#     2. Steps - CNN essential steps
#         - post /api/v1/type/common/env/
#         - post /api/v1/type/common/job/{nnid}/
#         - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/
#         - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/
#         - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/data/{args}/
#         - post /api/v1/type/dataframe/base/{baseid}/table/{tb}/format/{nnid}/
#         - post /api/v1/type/cnn/conf/{nnid}/
#         - post /api/v1/type/cnn/train/{nnid}/
#         - post /api/v1/type/cnn/eval/{nnid}/
#         - post /api/v1/type/cnn/predict/{nnid}/
#     3. Description \n
#         Manage data store schema (strucutre : schema - table - data)
#     """
#
#     # read
#     def post(self, request, nnid):
#         """
#         - desc : evaluate train result
#         """
#         try:
#             jd = jc.load_obj_json(request.body)
#             result = CNNEval().eval_model(nnid, jd.samplenum, jd.samplemethod)
#             return_data = {"status": "ok", "result": result}
#             return Response(json.dumps(return_data))
#         except Exception as e:
#             return_data = {"status": "404", "result": str(e)}
#             return Response(json.dumps(return_data))
#
#
#     def get(self, request, nnid):
#         """
#         - desc : get network evaluation result
#         """
#         try:
#             result = get_network_config(nnid)
#             return_data = {"status": "200", "result": result}
#             return Response(json.dumps(return_data))
#         except Exception as e:
#             return_data = {"status": "400", "result": str(e)}
#             return Response(json.dumps(return_data))