import unittest, requests, os, json,random, datetime
from tfmsacore import netconf
from tfmsacore.utils import tfmsa_logger
from PIL import Image, ImageFilter

class TestImagePredictProcess(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsacore/netconf --enable-coverage
    ./manage.py jenkins ./tests/tfmsacore/netconf
    """
    rand_name = str(random.randrange(1,99999))

    def test_insert_train_loss(self):
        tfmsa_logger("================TEST START================")
        init_data = {
            "nn_id": "test00001",
            "category": "MES",
            "subcate": "csv",
            "name": "CENSUS_INCOME",
            "desc": "INCOME PREDICT"
        }
        netconf.create_new_network(init_data)
        tfmsa_logger("[1] insert net base info : Done")

        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
        logInfoData = dict()
        logInfoData["nn_id"] = "test00001"
        logInfoData["loss"] = str("0.1")
        logInfoData["step"] = str("1000")
        logInfoData["max_step"] = str("1111")
        logInfoData["trainDate"] = nowDate
        logInfoData["testsets"] = "1"

        for i in range(0, 10):
            netconf.post_train_loss(logInfoData)
        tfmsa_logger("[2] insert train loss info : Done")

        result = netconf.get_train_loss("test00001")
        self.assertGreater(len(result), 1)
        tfmsa_logger("[3] check train loss inserted right : Done")
        tfmsa_logger("================TEST FINISH================")


    def test_insert_train_acc(self):
        tfmsa_logger("================TEST START================")
        init_data = {
            "nn_id": "test00001",
            "category": "MES",
            "subcate": "csv",
            "name": "CENSUS_INCOME",
            "desc": "INCOME PREDICT"
        }
        netconf.create_new_network(init_data)
        tfmsa_logger("[1] insert net base info : Done")

        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
        logInfoData = dict()
        logInfoData["nn_id"] = "test00001"
        logInfoData["label"] = str("A")
        logInfoData["guess"] = str("B")
        logInfoData["ratio"] = str("0.5")

        for i in range(0, 10):
            netconf.post_train_acc(logInfoData)
        tfmsa_logger("[2] insert train loss info : Done")

        result = netconf.get_train_acc("test00001")
        self.assertGreater(len(result), 0)
        tfmsa_logger("[3] check train loss inserted right : Done")
        tfmsa_logger("================TEST FINISH================")