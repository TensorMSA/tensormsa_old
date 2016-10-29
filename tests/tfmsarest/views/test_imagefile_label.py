

import unittest
from tfmsacore.utils.logger import tfmsa_logger
import os
import requests
import json

class TestImageFileLabel(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsarest/views/ --enable-coverage
    ./manage.py jenkins ./tests/tfmsarest/views/
    """

    def test_delete(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
        resp = requests.delete('http://' + host_name + '/api/v1/type/imagefile/base/test/table/test_table/label/1/',)
        data = json.loads(resp.json())
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else :
            raise Exception(data['result'])

    def test_post(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
        resp = requests.post('http://' + host_name + '/api/v1/type/imagefile/base/test/table/test_table/label/1/',)
        data = json.loads(resp.json())
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else :
            raise Exception(data['result'])
