# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

import yacg.model.model


class TestYacgModel (unittest.TestCase):
    def testType(self):
        x = yacg.model.model.Type()
        self.assertIsNotNone(x)

    def testObjectType(self):
        x = yacg.model.model.ObjectType()
        self.assertIsNotNone(x)

    def testIntegerTypeFormatEnum(self):
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.INT8)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.INT16)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.INT24)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.INT32)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.INT64)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.UINT8)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.UINT16)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.UINT24)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.UINT32)
        self.assertIsNotNone(yacg.model.model.IntegerTypeFormatEnum.UINT64)

    def testIntegerType(self):
        x = yacg.model.model.IntegerType()
        self.assertIsNotNone(x)

    def testNumberTypeFormatEnum(self):
        self.assertIsNotNone(yacg.model.model.NumberTypeFormatEnum.FLOAT)
        self.assertIsNotNone(yacg.model.model.NumberTypeFormatEnum.DOUBLE)

    def testNumberType(self):
        x = yacg.model.model.NumberType()
        self.assertIsNotNone(x)

    def testBooleanType(self):
        x = yacg.model.model.BooleanType()
        self.assertIsNotNone(x)

    def testStringType(self):
        x = yacg.model.model.StringType()
        self.assertIsNotNone(x)

    def testUuidType(self):
        x = yacg.model.model.UuidType()
        self.assertIsNotNone(x)

    def testEnumTypeValuesMap(self):
        x = yacg.model.model.EnumTypeValuesMap()
        self.assertIsNotNone(x)

    def testTag(self):
        x = yacg.model.model.Tag()
        self.assertIsNotNone(x)

    def testEnumType(self):
        x = yacg.model.model.EnumType()
        self.assertIsNotNone(x)

    def testDateType(self):
        x = yacg.model.model.DateType()
        self.assertIsNotNone(x)

    def testTimeType(self):
        x = yacg.model.model.TimeType()
        self.assertIsNotNone(x)

    def testDateTimeType(self):
        x = yacg.model.model.DateTimeType()
        self.assertIsNotNone(x)

    def testDurationType(self):
        x = yacg.model.model.DurationType()
        self.assertIsNotNone(x)

    def testBytesType(self):
        x = yacg.model.model.BytesType()
        self.assertIsNotNone(x)

    def testComplexType(self):
        x = yacg.model.model.ComplexType()
        self.assertIsNotNone(x)

    def testProperty(self):
        x = yacg.model.model.Property()
        self.assertIsNotNone(x)

    def testDictionaryType(self):
        x = yacg.model.model.DictionaryType()
        self.assertIsNotNone(x)

    def testArrayConstraints(self):
        x = yacg.model.model.ArrayConstraints()
        self.assertIsNotNone(x)

    def testArrayType(self):
        x = yacg.model.model.ArrayType()
        self.assertIsNotNone(x)

    def testForeignKey(self):
        x = yacg.model.model.ForeignKey()
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
