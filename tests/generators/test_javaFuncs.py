import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config

from yacg.model.model import IntegerType, IntegerTypeFormatEnum, NumberType, NumberTypeFormatEnum
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType
import yacg.generators.helper.javaFuncs as javaFuncs
import yacg.model.modelFuncs as modelFuncs


def getExampleType():
    modelFile = 'tests/resources/models/json/examples/all_types.json'
    modelFileExists = os.path.isfile(modelFile)
    model = config.Model()
    model.schema = modelFile
    modelTypes = getModelFromJson(model, [])
    return modelTypes[0]


# For executing these tests run: pipenv run python3 -m unittest -v tests/generators/test_javaFuncs.py
class TestJavaFuncs (unittest.TestCase):

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


    def testJavaFuncs(self):
        myType = getExampleType()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(isinstance(myType, ComplexType))

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
