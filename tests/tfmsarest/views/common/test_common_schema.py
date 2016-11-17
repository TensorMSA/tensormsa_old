import unittest
from tfmsacore.utils.logger import tfmsa_logger
import os
import requests
import json

class TestCommonSchema(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsarest/views/ --enable-coverage
    ./manage.py jenkins ./tests/tfmsarest/views/common/
    """

    def test_gete(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
        resp = requests.get('http://' + host_name + '/api/v1/type/schema/datatype/image/preprocess/pre/category/mes/subcategory/m60/')

        data = json.loads(resp.json())
        self.assertEqual(data['result'][0], "image_pre_mes_m60")
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else :
            raise Exception(resp.json())

