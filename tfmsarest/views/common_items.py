from tfmsacore import netconf
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc


class CommonItems(APIView):
    """
    """

    def get(self, request, type, condition):
        """
        - desc : return nn_info data
        """
        try:
            if type == 'category' :
                result = netconf.get_category_list()
            elif type == 'subcategory' :
                result = netconf.get_subcategory_list(condition)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))
