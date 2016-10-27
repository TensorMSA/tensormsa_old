import unittest
from tfmsacore.batch import SparkSessionManager
from pyspark.context import SparkContext
from tfmsacore.utils.logger import tfmsa_logger

class TestSparkSession(unittest.TestCase):

    def setUp(self):
        tfmsa_logger('####### START ########')

    def tearDown(self):
        tfmsa_logger('####### FINISH ########')

    def test_create_session(self):
        """
        ./manage.py jenkins ./tests/tfmsacore/batch/ --enable-coverage
        ./manage.py jenkins ./tests/tfmsacore/batch/
        :return:
        """
        self.assertIsInstance(SparkSessionManager().create_session(), (SparkContext))
        self.assertIsInstance(SparkSessionManager().create_session(), (SparkContext))

    def test_get_session(self):
        """
        ./manage.py jenkins ./tests/tfmsacore/batch/ --enable-coverage
        ./manage.py jenkins ./tests/tfmsacore/batch/
        :return:
        """
        self.assertIsInstance(SparkSessionManager().get_session(), (SparkContext))

if __name__ == '__main__':
    unittest.main()
