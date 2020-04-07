import unittest
from yacg.util.stringUtils import toUpperCamelCase


class TestStringUtils (unittest.TestCase):
    def testUpperCamelCase(self):
        t = toUpperCamelCase('i am a test')
        self.assertEqual('IAmATest', t)

    def testUpperCamelCase2(self):
        t = toUpperCamelCase('IamAnotherTest')
        self.assertEqual('IamAnotherTest', t)
