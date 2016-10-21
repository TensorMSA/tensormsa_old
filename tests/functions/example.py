import unittest
#from django.utils import unittest
import unitCase

TestMethod = unitCase.TestMethod()

class TestUnitTestExample(unittest.TestCase):

    def setUp(self):
        print('Start TensorMSA test')

    def tearDown(self):
        print('Finish TensorMSA test')

    def test_returnValue(self):
        self.assertEqual(TestMethod.returnString(), 'successful')

    def test_upper(self):
        test = 'test'
        self.assertEqual(TestMethod.returnUpper(test), 'TEST')

    def test_isupper(self):
        test = 'TEST'
        #self.assertTrue(TestMethod.checkUpper(test))
        self.assertFalse(TestMethod.checkUpper(test))

    def test_split(self):
        test = 'TensorMSA Test'
        # check that s.split fails when the separator is not a string
        self.assertRaises(TypeError, TestMethod.splitString(test))    
        self.assertEqual(TestMethod.splitString(test), ['TensorMSA', 'Test'])

if __name__ == '__main__':
    unittest.main()

