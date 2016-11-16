from tfmsacore import netconf
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class CommonSchema(APIView):
    """
    """

    def get(self, request, datatype, preprocess, category, subcategory ):
        """
        - desc : return nn_info data
        """
        try:
            result = netconf.get_namespace(datatype, preprocess, category, subcategory)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))