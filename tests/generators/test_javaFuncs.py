import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config

from yacg.model.model import IntegerType, IntegerTypeFormatEnum, NumberType, NumberTypeFormatEnum
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType
import yacg.generators.helper.javaFuncs as javaFuncs

# For executing these test run: pipenv run python3 -m unittest -v tests/generators/test_javaFuncs.py
class TestJavaFuncs (unittest.TestCase):
    def testJavaFuncs(self):
        modelFile = 'tests/resources/models/json/examples/all_types.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(3, len(modelTypes))
        self.assertTrue(isinstance(modelTypes[0], ComplexType))
        self.assertTrue(isinstance(modelTypes[1], EnumType))
        self.assertTrue(isinstance(modelTypes[2], EnumType))

        myType = modelTypes[0]
        self.assertEqual('ExampleType', myType.name)

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
