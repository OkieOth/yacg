# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from yacg.model.genModel import Type
from yacg.model.genModel import IntegerType
from yacg.model.genModel import IntegerTypeFormatEnum
from yacg.model.genModel import NumberType
from yacg.model.genModel import NumberTypeFormatEnum
from yacg.model.genModel import StringType
from yacg.model.genModel import EnumType
from yacg.model.genModel import DateType
from yacg.model.genModel import DateTimeType
from yacg.model.genModel import ComplexType
from yacg.model.genModel import Property
from yacg.model.genModel import Tag


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

    def testStringType(self):
        x = StringType()
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

