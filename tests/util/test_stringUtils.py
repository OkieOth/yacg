import unittest
from yacg.util.stringUtils import toUpperCamelCase, toName


class TestStringUtils (unittest.TestCase):
    def testUpperCamelCase(self):
        t = toUpperCamelCase('i am a test')
        self.assertEqual('IAmATest', t)

    def testUpperCamelCase2(self):
        t = toUpperCamelCase('IamAnotherTest')
        self.assertEqual('IamAnotherTest', t)

    def testToName(self):
        t = toName('IamAnotherTest')
        self.assertEqual('IamAnotherTest', t)
        t = toName('1')
        self.assertEqual('_1', t)
        t = toName('1.1')
        self.assertEqual('_1_1', t)
        t = toName('1/1/')
        self.assertEqual('_1_1_', t)
        t = toName('1:1:')
        self.assertEqual('_1_1_', t)
        t = toName('a:1')
        self.assertNotEqual('a_1_', t)
        t = toName('a:1')
        self.assertEqual('a_1', t)
