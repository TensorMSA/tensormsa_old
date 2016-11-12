import unittest
from tfmsacore.utils.logger import tfmsa_logger
from tfmsacore.netcommon.acc_eval_common import AccEvalCommon
from tfmsacore import netconf

class TestAccEvalCommon(unittest.TestCase):
    """
    ./manage.py jenkins ./tests/tfmsacore/netcommon/ --enable-coverage
    ./manage.py jenkins ./tests/tfmsacore/netcommon/
    """

    def test_search_all_database(self):
        """
        test search all database works correctly
        :return:
        """
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

        AccEvalCommon("test00001").set_result("a", "a")
        AccEvalCommon("test00001").set_result("a", "a")
        AccEvalCommon("test00001").set_result("a", "b")
        AccEvalCommon("test00001").set_result("a", "c")
        AccEvalCommon("test00001").set_result("b", "a")
        AccEvalCommon("test00001").set_result("b", "b")
        AccEvalCommon("test00001").set_result("b", "c")
        AccEvalCommon("test00001").set_result("b", "b")
        AccEvalCommon("test00001").set_result("c", "c")

        result = AccEvalCommon("test00001").reverse_result()
        tfmsa_logger("Result Check : {0}".format(result))
        self.assertEqual(len(result.keys()), 3)
        tfmsa_logger("==========PASS==========")
