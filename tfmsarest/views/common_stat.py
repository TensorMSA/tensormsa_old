from tfmsacore import netconf
import json, unicodedata
from rest_framework.response import Response
from rest_framework.views import APIView
from tfmsacore.utils.json_conv import JsonDataConverter as jc
from tfmsacore.netconf.nn_common_manager import get_network_config
from tfmsacore.netcommon.acc_eval_common import AccEvalCommon

class CommonResultStatInfo(APIView):

    def get(self, request, nnid):
        """
        - desc : return nn_info data
        """
        try:
            result = {}
            result['detail'] = AccEvalCommon(nnid).reverse_result()
            result['summary'] = netconf.get_net_summary(nnid)
            result['loss'] = netconf.get_train_loss(nnid)
            result['jobparm'] = netconf.get_thread_status(nnid)
            return_data = {"status": "200", "result": result}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "400", "result": str(e)}
            return Response(json.dumps(return_data))
