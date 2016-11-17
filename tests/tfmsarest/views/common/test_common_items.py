

import unittest
from tfmsacore.utils.logger import tfmsa_logger
import os
import requests
import json

class TestCommonItems(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsarest/views/ --enable-coverage
    ./manage.py jenkins ./tests/tfmsarest/views/common/
    """

    def test_gete(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
        resp = requests.get('http://' + host_name + '/api/v1/type/common/item/category//',)

        data = json.loads(resp.json())
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else :
            raise Exception(resp.json())

        resp = requests.get('http://' + host_name + '/api/v1/type/common/item/subactegory/mes/',)
        data = json.loads(resp.json())
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else :
            raise Exception(resp.json())