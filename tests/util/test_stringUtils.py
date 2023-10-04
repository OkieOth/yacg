import unittest
from yacg.util.stringUtils import toUpperCamelCase, toName
from yacg.util.stringUtils import snakeToLowerCamelCase, snakeToUpperCamelCase, toLowerCase, toUpperCase

# For executing these test run: python -m unittest -v tests/util/test_stringUtils.py
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

    def testSnakeToLowerCamelCase(self):
        t = snakeToLowerCamelCase(None)
        self.assertEqual(None, t)

        t = snakeToLowerCamelCase('')
        self.assertEqual('', t)

        t = snakeToLowerCamelCase('A')
        self.assertEqual('a', t)

        t = snakeToLowerCamelCase('this_is_a_snake_case')
        self.assertEqual('thisIsASnakeCase', t)

        t = snakeToLowerCamelCase('ALL_UPPER_SNAKE')
        self.assertEqual('aLLUPPERSNAKE', t)

    def testSnakeToUpperCamelCase(self):
        t = snakeToUpperCamelCase(None)
        self.assertEqual(None, t)

        t = snakeToUpperCamelCase('')
        self.assertEqual('', t)

        t = snakeToUpperCamelCase('a')
        self.assertEqual('A', t)

        t = snakeToUpperCamelCase('this_is_a_snake_case')
        self.assertEqual('ThisIsASnakeCase', t)

        t = snakeToUpperCamelCase('ALL_UPPER_SNAKE')
        self.assertEqual('ALLUPPERSNAKE', t)

    def testToLowerCase(self):
        t = toLowerCase(None)
        self.assertEqual(None, t)
        # test text starting with upper case character
        t = toLowerCase('AbCdE')
        self.assertEqual('abCdE', t)
        # test text starting with lower case character
        t = toLowerCase('aBcDe')
        self.assertEqual('aBcDe', t)
        # test single lower case character
        t = toLowerCase('x')
        self.assertEqual('x', t)
        # test single upper case character
        t = toLowerCase('Y')
        self.assertEqual('y', t)
        # leading numbers prevent changing case of susequent letters
        t = toLowerCase('1ABC')
        self.assertEqual('1ABC', t)
        # test empy string
        t = toLowerCase('')
        self.assertEqual('', t)

    def testToUpperCase(self):
        t = toUpperCase(None)
        self.assertEqual(None, t)
        # test text starting with upper case character
        t = toUpperCase('AbCdE')
        self.assertEqual('AbCdE', t)
        # test text starting with lower case character
        t = toUpperCase('aBcDe')
        self.assertEqual('ABcDe', t)
        # test single lower case character
        t = toUpperCase('x')
        self.assertEqual('X', t)
        # test single upper case character
        t = toUpperCase('Y')
        self.assertEqual('Y', t)
        # leading numbers prevent changing case of susequent letters
        t = toUpperCase('1abc')
        self.assertEqual('1abc', t)
        # test empy string
        t = toUpperCase('')
        self.assertEqual('', t)
