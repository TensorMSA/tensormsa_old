

import unittest
from tfmsacore.utils.logger import tfmsa_logger
import os
import requests
import json

class TestImageFileFormat(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsarest/views/ --enable-coverage
    ./manage.py jenkins ./tests/tfmsarest/views/
    """

    def test_post(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
        # set network info
        resp = requests.post('http://' + host_name + '/api/v1/type/common/nninfo/',
                             json={
                                 "nn_id": "nn0000090",
                                 "category": "img",
                                 "subcate": "img_test",
                                 "name": "img_cnn",
                                 "desc": "img_cnn"
                             })
        data = json.loads(resp.json())
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")

        resp = requests.post('http://' + host_name + '/api/v1/type/imagefile/base/test/table/testtable/label/1/format/nn0000090/',
                             json={"x_size": 100,
                                   "y_size": 100
                                   })
        data = json.loads(resp.json())
        if (data['status'] == "200"):
            tfmsa_logger("==========PASS==========")
        else :
            raise Exception(data['result'])


