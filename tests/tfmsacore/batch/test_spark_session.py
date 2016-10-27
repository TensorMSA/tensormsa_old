import unittest
from tfmsacore.batch import SparkSessionManager
from pyspark.context import SparkContext

class TestSparkSession(unittest.TestCase):

    def setUp(self):
        print('Start TestSparkSession test')

    def tearDown(self):
        print('Finish TestSparkSession test')

    def test_init(self):
        """
        ./manage.py jenkins ./tests/tfmsacore/ --enable-coverage
        :return:
        """
        self.assertIsInstance(SparkSessionManager().get_session(), (SparkContext))

if __name__ == '__main__':
    unittest.main()

