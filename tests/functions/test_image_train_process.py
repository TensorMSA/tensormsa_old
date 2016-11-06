import unittest, requests, os, json,random
from tfmsacore.utils.logger import tfmsa_logger
from django.core.files.uploadedfile import TemporaryUploadedFile
from tfmsacore.data import ImageManager

class TestImageTrainProcess(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/functions --enable-coverage
    ./manage.py jenkins ./tests/functions
    """
    rand_name = str(random.randrange(1,99999))

    def test_image_train(self):
        host_name = "{0}:{1}".format(os.environ['HOSTNAME'], "8989")

        tfmsa_logger("[1] Image file format update")
        resp = requests.post('http://' + host_name + '/api/v1/type/imagefile/base/mes/table/testtable2/format/nn0000090/',
                             json={"x_size": 32,"y_size": 32 })
        if(json.loads(resp.json())['status'] != "200"):
            raise Exception ("RESI Service Fail")


        tfmsa_logger("[2] Network info update")
        resp = requests.post('http://' + host_name + '/api/v1/type/common/nninfo/',
                             json={
                                 "nn_id": "nn0000090",
                                 "category": "SCM",
                                 "subcate": "csv",
                                 "name": "CENSUS_INCOME",
                                 "desc": "INCOME PREDICT"
                             })
        if (json.loads(resp.json())['status'] != "200"):
            raise Exception("RESI Service Fail")

        tfmsa_logger("[3] Network configuration update")
        resp = requests.post('http://' + host_name + '/api/v1/type/cnn/conf/nn0000090/',
                             json={
                                 "data":
                                     {
                                         "datalen": 1024,
                                         "taglen": 2,
                                         "matrix": [32, 32],
                                         "learnrate": 0.01,
                                         "epoch": 10
                                     },
                                 "layer":
                                     [
                                         {
                                             "type": "input",
                                             "active": "relu",
                                             "cnnfilter": [2, 2],
                                             "cnnstride": [2, 2],
                                             "maxpoolmatrix": [2, 2],
                                             "maxpoolstride": [2, 2],
                                             "node_in_out": [1, 16],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         },
                                         {
                                             "type": "cnn",
                                             "active": "relu",
                                             "cnnfilter": [2, 2],
                                             "cnnstride": [2, 2],
                                             "maxpoolmatrix": [2, 2],
                                             "maxpoolstride": [2, 2],
                                             "node_in_out": [16, 32],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         },
                                         {
                                             "type": "reshape",
                                         },
                                         {
                                             "type": "drop",
                                             "active": "relu",
                                             "regualizer": "",
                                             "droprate": "0.5"
                                         },
                                         {
                                             "type": "out",
                                             "active": "softmax",
                                             "cnnfilter": "",
                                             "cnnstride": "",
                                             "maxpoolmatrix": "",
                                             "maxpoolstride": "",
                                             "node_in_out": [32, 2],
                                             "regualizer": "",
                                             "padding": "SAME",
                                             "droprate": ""
                                         }
                                     ]
                             })
        if (json.loads(resp.json())['status'] != "200"):
            raise Exception("RESI Service Fail")

        tfmsa_logger("[4] Train Neural Network")
        resp = requests.post('http://' + host_name + '/api/v1/type/cnn/train/nn0000090/',
                             json={
                                 "epoch": "10",
                                 "testset": "10"
                             })
        if (json.loads(resp.json())['status'] != "200"):
            raise Exception("RESI Service Fail")

        tfmsa_logger("[5] PASS TEST")

