import unittest, requests, os, json,random, datetime
from tfmsacore import netconf
from tfmsacore.utils import tfmsa_logger

class TestFlagManager(unittest.TestCase):
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

        # just consider worsk fine if no exception occurs
        netconf.set_on_net_conf("test00001")
        netconf.set_on_net_vaild("test00001")
        netconf.set_on_train("test00001")
        netconf.set_on_data_conf("test00001")
        netconf.set_on_data("test00001")

        result = netconf.get_network_config("test00001")
        idx_set = ["datavaild", "config", "train", "confvaild"]

        for idx in idx_set:
            self.assertEqual(result[idx], 'Y')
        netconf.set_off_net_conf("test00001")
        netconf.set_off_net_vaild("test00001")
        netconf.set_off_train("test00001")
        netconf.set_off_data_conf("test00001")
        netconf.set_off_data("test00001")

        result = netconf.get_network_config("test00001")
        idx_set = ["datavaild", "config", "train", "confvaild"]

        for idx in idx_set:
            self.assertEqual(result[idx], 'N')

        tfmsa_logger("================TEST END================")

