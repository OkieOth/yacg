# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from <<"modelPackage" template param is missing>> import Type
from <<"modelPackage" template param is missing>> import IntegerType
from <<"modelPackage" template param is missing>> import IntegerTypeFormatEnum
from <<"modelPackage" template param is missing>> import NumberType
from <<"modelPackage" template param is missing>> import NumberTypeFormatEnum
from <<"modelPackage" template param is missing>> import BooleanType
from <<"modelPackage" template param is missing>> import StringType
from <<"modelPackage" template param is missing>> import UuidType
from <<"modelPackage" template param is missing>> import EnumType
from <<"modelPackage" template param is missing>> import DateType
from <<"modelPackage" template param is missing>> import DateTimeType
from <<"modelPackage" template param is missing>> import ComplexType
from <<"modelPackage" template param is missing>> import Property
from <<"modelPackage" template param is missing>> import Tag


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
