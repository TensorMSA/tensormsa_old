import unittest
#from django.utils import unittest
import unitCase

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

  #  def setUp(self):
   #          self.test = unitCase.TestA()
#            self.lion = unitCase.objects.create(name="lion", sound="roar")
#            self.cat = unitCase.objects.create(name="cat", sound="meow")

    def testSpeaking(self):
        TestMethod = unitCase.TestMethod()
        print ( TestMethod.TestA())
        self.assertEqual(TestMethod.TestA(), 'A')
          #  self.assertEqual(self.lion.speak(), 'The lion says "roar"')
          #  self.assertEqual(self.cat.speak(), 'The cat says "meow"')

if __name__ == '__main__':
    unittest.main()

