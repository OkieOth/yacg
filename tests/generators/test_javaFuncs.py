import unittest
# import os.path
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config
import yacg.model.model as model

from yacg.model.model import IntegerType, IntegerTypeFormatEnum, NumberType, NumberTypeFormatEnum
from yacg.model.model import StringType, EnumType, DictionaryType
from yacg.model.model import DateType, TimeType, DateTimeType, UuidType
from yacg.model.model import ComplexType, BytesType, ObjectType
import yacg.generators.helper.javaFuncs as javaFuncs
import yacg.model.modelFuncs as modelFuncs


def getExampleType():
    modelFile = 'tests/resources/models/json/examples/all_types.json'
    # modelFileExists = os.path.isfile(modelFile)
    model = config.Model()
    model.schema = modelFile
    modelTypes = getModelFromJson(model, [])
    return modelTypes[0]


# For executing these tests run: python3 -m unittest -v tests/generators/test_javaFuncs.py
class TestJavaFuncs (unittest.TestCase):

    def testIsDouble(self):
        doubleType = NumberType()
        self.assertTrue(javaFuncs.isDouble(doubleType))
        self.assertFalse(javaFuncs.isFloat(doubleType))

        doubleType.format = NumberTypeFormatEnum.DOUBLE
        self.assertTrue(javaFuncs.isDouble(doubleType))
        self.assertFalse(javaFuncs.isFloat(doubleType))


    def testIsFloat(self):
        floatType = NumberType()
        floatType.format = NumberTypeFormatEnum.FLOAT
        self.assertTrue(javaFuncs.isFloat(floatType))
        self.assertFalse(javaFuncs.isDouble(floatType))


    def testIsLong(self):
        longType = IntegerType()
        longType.format = IntegerTypeFormatEnum.INT64
        self.assertTrue(javaFuncs.isLong(longType))
        self.assertFalse(javaFuncs.isInteger(longType))


    def testIsInteger(self):
        intType = IntegerType()
        self.assertTrue(javaFuncs.isInteger(intType))
        self.assertFalse(javaFuncs.isLong(intType))

        intType.format = IntegerTypeFormatEnum.INT32
        self.assertTrue(javaFuncs.isInteger(intType))
        self.assertFalse(javaFuncs.isLong(intType))


    def testSanitizeRestorePropertyNames(self):
        myType = getExampleType()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(isinstance(myType, ComplexType))

        allProps = modelFuncs.getFlattenProperties(myType)
        countProps = len(allProps)
        first = allProps[0]
        sixth = allProps[5]
        first.name = 'enum'
        sixth.name = 'class'

        # replace problematic property names
        idx2origName = javaFuncs.sanitizePropertyNames(myType)
        self.assertEqual(2, len(idx2origName))
        self.assertEqual(countProps, len(modelFuncs.getFlattenProperties(myType)))

        # check exactly one property with name enumValue
        props = modelFuncs.filterProps(myType, lambda prop: prop.name == 'enumValue')
        self.assertEqual(1, len(props))
        self.assertEqual('enumValue', first.name)

        actName = idx2origName[0]
        self.assertIsNotNone(actName)
        self.assertEqual('enum', actName)

        # check exactly one property with name clazz
        props = modelFuncs.filterProps(myType, lambda prop: prop.name == 'clazz')
        self.assertEqual(1, len(props))
        self.assertEqual('clazz', sixth.name)

        actName = idx2origName[5]
        self.assertIsNotNone(actName)
        self.assertEqual('class', actName)

        # restore original property names
        javaFuncs.restorePropertyNames(myType, idx2origName)
        self.assertEqual(countProps, len(modelFuncs.getFlattenProperties(myType)))

        # check exactly one property with name enum and none with enumValue
        props = modelFuncs.filterProps(myType, lambda prop: prop.name == 'enumValue')
        self.assertEqual(0, len(props))
        props = modelFuncs.filterProps(myType, lambda prop: prop.name == 'enum')
        self.assertEqual(1, len(props))
        self.assertEqual('enum', first.name)

        # check exactly one property with name class and none with clazz
        props = modelFuncs.filterProps(myType, lambda prop: prop.name == 'clazz')
        self.assertEqual(0, len(props))
        props = modelFuncs.filterProps(myType, lambda prop: prop.name == 'class')
        self.assertEqual(1, len(props))
        self.assertEqual('class', sixth.name)


    def testgetJavaTypes(self):
        intType = IntegerType()
        self.assertEqual('Integer', javaFuncs.getJavaType(intType, False))
        self.assertEqual('java.util.List<Integer>', javaFuncs.getJavaType(intType, True))

        doubleType = NumberType()
        doubleType.format = NumberTypeFormatEnum.DOUBLE
        self.assertEqual('Double', javaFuncs.getJavaType(doubleType, False))
        self.assertEqual('java.util.List<Double>', javaFuncs.getJavaType(doubleType, True))

        floatType = NumberType()
        floatType.format = NumberTypeFormatEnum.FLOAT
        self.assertEqual('Float', javaFuncs.getJavaType(floatType, False))
        self.assertEqual('java.util.List<Float>', javaFuncs.getJavaType(floatType, True))

        numberType = NumberType()
        self.assertEqual('Double', javaFuncs.getJavaType(numberType, False))
        self.assertEqual('java.util.List<Double>', javaFuncs.getJavaType(numberType, True))

        stringType = StringType()
        self.assertEqual('String', javaFuncs.getJavaType(stringType, False))
        self.assertEqual('java.util.List<String>', javaFuncs.getJavaType(stringType, True))

        uuidType = UuidType()
        self.assertEqual('java.util.UUID', javaFuncs.getJavaType(uuidType, False))
        self.assertEqual('java.util.List<java.util.UUID>', javaFuncs.getJavaType(uuidType, True))

        objectType = ObjectType()
        self.assertEqual('Object', javaFuncs.getJavaType(objectType, False))
        self.assertEqual('java.util.List<Object>', javaFuncs.getJavaType(objectType, True))

        bytesType = BytesType()
        self.assertEqual('byte[]', javaFuncs.getJavaType(bytesType, False))
        self.assertEqual('java.util.List<byte[]>', javaFuncs.getJavaType(bytesType, True))

        dateType = DateType()
        self.assertEqual('java.time.LocalDate', javaFuncs.getJavaType(dateType, False))
        self.assertEqual('java.util.List<java.time.LocalDate>', javaFuncs.getJavaType(dateType, True))

        timeType = TimeType()
        self.assertEqual('java.time.LocalTime', javaFuncs.getJavaType(timeType, False))
        self.assertEqual('java.util.List<java.time.LocalTime>', javaFuncs.getJavaType(timeType, True))

        dateTimeType = DateTimeType()
        self.assertEqual('java.time.LocalDateTime', javaFuncs.getJavaType(dateTimeType, False))
        self.assertEqual('java.util.List<java.time.LocalDateTime>', javaFuncs.getJavaType(dateTimeType, True))

        enumType = EnumType()
        enumType.name = 'Foo'
        self.assertEqual('Foo', javaFuncs.getJavaType(enumType, False))
        self.assertEqual('java.util.List<Foo>', javaFuncs.getJavaType(enumType, True))

        dictType = DictionaryType()
        dictType.valueType = UuidType()
        self.assertEqual('java.util.Map<String, java.util.UUID>', javaFuncs.getJavaType(dictType, False))
        self.assertEqual('java.util.List<java.util.Map<String, java.util.UUID>>', javaFuncs.getJavaType(dictType, True))

    def testJavaFuncs(self):
        myType = getExampleType()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(isinstance(myType, ComplexType))

        # use this line for good old print debugging
        # print("type={} javaClass={}".format(type(prop.type), javaFuncs.getJavaType(prop.type, prop.isArray)))

        # ComplexType
        self.assertEqual('ExampleType', javaFuncs.getJavaType(myType, False))
        self.assertEqual('java.util.List<ExampleType>', javaFuncs.getJavaType(myType, True))

        # StringType
        prop = myType.properties[0]
        self.assertEqual('String', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[1]
        self.assertEqual('java.util.List<String>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # UuidType
        prop = myType.properties[2]
        self.assertEqual('java.util.UUID', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[3]
        self.assertEqual('java.util.List<java.util.UUID>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # StringType with format date
        prop = myType.properties[4]
        self.assertEqual('java.time.LocalDate', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[5]
        self.assertEqual('java.util.List<java.time.LocalDate>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # StringType with format date-time
        prop = myType.properties[6]
        self.assertEqual('java.time.LocalDateTime', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[7]
        self.assertEqual('java.util.List<java.time.LocalDateTime>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # IntegerType with formats
        prop = myType.properties[12]
        self.assertEqual('Integer', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[13]
        self.assertEqual('java.util.List<Integer>', javaFuncs.getJavaType(prop.type, prop.isArray))

        prop = myType.properties[14]
        self.assertEqual('Integer', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[15]
        self.assertEqual('java.util.List<Integer>', javaFuncs.getJavaType(prop.type, prop.isArray))

        prop = myType.properties[16]
        self.assertEqual('Long', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[17]
        self.assertEqual('java.util.List<Long>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # NumberType with formats
        prop = myType.properties[18]
        self.assertEqual('Double', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[19]
        self.assertEqual('java.util.List<Double>', javaFuncs.getJavaType(prop.type, prop.isArray))

        prop = myType.properties[20]
        self.assertEqual('Float', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[21]
        self.assertEqual('java.util.List<Float>', javaFuncs.getJavaType(prop.type, prop.isArray))

        prop = myType.properties[22]
        self.assertEqual('Double', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[23]
        self.assertEqual('java.util.List<Double>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # BooleanType
        prop = myType.properties[24]
        self.assertEqual('Boolean', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[25]
        self.assertEqual('java.util.List<Boolean>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # StringType with format time
        prop = myType.properties[26]
        self.assertEqual('java.time.LocalTime', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[27]
        self.assertEqual('java.util.List<java.time.LocalTime>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # StringType with format byte
        prop = myType.properties[28]
        self.assertTrue('bytes' in prop.name)
        self.assertEqual('byte[]', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[29]
        self.assertTrue('bytes' in prop.name)
        self.assertEqual('java.util.List<byte[]>', javaFuncs.getJavaType(prop.type, prop.isArray))

        # ObjectType ("type": "object")
        prop = myType.properties[30]
        self.assertTrue('object' in prop.name)
        self.assertEqual('Object', javaFuncs.getJavaType(prop.type, prop.isArray))
        prop = myType.properties[31]
        self.assertTrue('object' in prop.name)
        self.assertEqual('java.util.List<Object>', javaFuncs.getJavaType(prop.type, prop.isArray))
