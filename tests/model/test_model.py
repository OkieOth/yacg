import unittest

from yacg.model.model import Type
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType
from yacg.model.model import Property, Tag


class TestModelClasses (unittest.TestCase):
    def testType(self):
        x = Type('test')
        self.assertIsNotNone(x)
        self.assertEqual('test', x.name)

    def testIntegerType(self):
        x = IntegerType()
        self.assertIsNotNone(x)
        self.assertEqual('IntegerType', x.name)

    def testNumberType(self):
        x = NumberType()
        self.assertIsNotNone(x)
        self.assertEqual('NumberType', x.name)

    def testStringType(self):
        x = StringType()
        self.assertIsNotNone(x)
        self.assertEqual('StringType', x.name)

    def testDateType(self):
        x = DateType()
        self.assertIsNotNone(x)
        self.assertEqual('DateType', x.name)

    def testDateTimeType(self):
        x = DateTimeType()
        self.assertIsNotNone(x)
        self.assertEqual('DateTimeType', x.name)

    def testEnumType(self):
        x = EnumType('TestEnum')
        self.assertIsNotNone(x)
        self.assertEqual('TestEnum', x.name)

    def testComplexType(self):
        x = ComplexType('ComplexTest')
        self.assertIsNotNone(x)
        self.assertEqual('ComplexTest', x.name)
        self.assertEqual(0, len(x.tags))

    def testProperty(self):
        x = ComplexType('ComplexTest')
        self.assertIsNotNone(x)
        self.assertEqual('ComplexTest', x.name)
        property = Property('testProp', x)
        self.assertEqual('testProp', property.name)
        self.assertTrue(isinstance(property.type, ComplexType))
        self.assertFalse(property.isArray)
        self.assertEqual(0, len(property.tags))

    def testTag(self):
        tag1 = Tag('myName')
        self.assertEqual('myName', tag1.name)
        self.assertTrue(tag1.value is not None)
        tag2 = Tag('myName2', 'I am a string')
        self.assertEqual('myName2', tag2.name)
        self.assertEqual('I am a string', tag2.value)


if __name__ == '__main__':
    unittest.main()
