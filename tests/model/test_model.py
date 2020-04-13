# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from yacg.model.model import Type
from yacg.model.model import IntegerType
from yacg.model.model import IntegerTypeFormatEnum
from yacg.model.model import NumberType
from yacg.model.model import NumberTypeFormatEnum
from yacg.model.model import BooleanType
from yacg.model.model import StringType
from yacg.model.model import UuidType
from yacg.model.model import EnumType
from yacg.model.model import DateType
from yacg.model.model import DateTimeType
from yacg.model.model import ComplexType
from yacg.model.model import Property
from yacg.model.model import Tag


class TestYacgModel (unittest.TestCase):
    def testType(self):
        x = Type()
        self.assertIsNotNone(x)

    def testIntegerType(self):
        x = IntegerType()
        self.assertIsNotNone(x)

    def testIntegerTypeFormatEnum(self):
        self.assertIsNotNone(IntegerTypeFormatEnum.INT32)
        self.assertIsNotNone(IntegerTypeFormatEnum.INT64)

    def testNumberType(self):
        x = NumberType()
        self.assertIsNotNone(x)

    def testNumberTypeFormatEnum(self):
        self.assertIsNotNone(NumberTypeFormatEnum.FLOAT)
        self.assertIsNotNone(NumberTypeFormatEnum.DOUBLE)

    def testBooleanType(self):
        x = BooleanType()
        self.assertIsNotNone(x)

    def testStringType(self):
        x = StringType()
        self.assertIsNotNone(x)

    def testUuidType(self):
        x = UuidType()
        self.assertIsNotNone(x)

    def testEnumType(self):
        x = EnumType()
        self.assertIsNotNone(x)

    def testDateType(self):
        x = DateType()
        self.assertIsNotNone(x)

    def testDateTimeType(self):
        x = DateTimeType()
        self.assertIsNotNone(x)

    def testComplexType(self):
        x = ComplexType()
        self.assertIsNotNone(x)

    def testProperty(self):
        x = Property()
        self.assertIsNotNone(x)

    def testTag(self):
        x = Tag()
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
