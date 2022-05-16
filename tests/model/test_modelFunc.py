import unittest

import os.path
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config

from yacg.model.model import IntegerType, IntegerTypeFormatEnum, NumberType, NumberTypeFormatEnum
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType, DictionaryType
import yacg.model.modelFuncs as modelFuncs

def getComplexTypeNoBase():
    modelFile = 'tests/resources/models/json/examples/all_types.json'
    modelFileExists = os.path.isfile(modelFile)
    model = config.Model()
    model.schema = modelFile
    modelTypes = getModelFromJson(model, [])
    myType = modelTypes[0]
    return myType

# For executing these test run: pipenv run python3 -m unittest -v tests/model/test_modelFunc.py
class TestModelFuncs (unittest.TestCase):

    def testHasPropertyOfTypeNoBaseType(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(myType.extendsType is None)

        self.assertTrue(modelFuncs.hasPropertyOfType(myType, UuidType))
        self.assertFalse(modelFuncs.hasPropertyOfType(myType, DictionaryType))

        # pop() removes item from list!
        prop = myType.properties.pop(3)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertTrue(prop.isArray)

        prop = myType.properties.pop(2)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertFalse(prop.isArray)

        self.assertFalse(modelFuncs.hasPropertyOfType(myType, UuidType))


    def testHasSinglePropertyOfTypeNoBaseType(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(myType.extendsType is None)

        self.assertTrue(modelFuncs.hasSinglePropertyOfType(myType, UuidType))
        self.assertFalse(modelFuncs.hasSinglePropertyOfType(myType, DictionaryType))

        # pop() removes item from list!
        prop = myType.properties.pop(2)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertFalse(prop.isArray)
        self.assertFalse(modelFuncs.hasSinglePropertyOfType(myType, UuidType))


    def testHasArrayPropertyOfTypeNoBaseType(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(myType.extendsType is None)

        self.assertTrue(modelFuncs.hasArrayPropertyOfType(myType, UuidType))
        self.assertFalse(modelFuncs.hasArrayPropertyOfType(myType, DictionaryType))

        # pop() removes item from list!
        prop = myType.properties.pop(3)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertTrue(prop.isArray)
        self.assertFalse(modelFuncs.hasArrayPropertyOfType(myType, UuidType))


    def testFilterPropsNoBaseType(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(myType.extendsType is None)

        # get UuidType properties
        uuidProps = modelFuncs.filterProps(myType, lambda prop: isinstance(prop.type, UuidType))
        self.assertIsNotNone(uuidProps)
        self.assertEqual(2, len(uuidProps))

        for prop in uuidProps:
            self.assertTrue(isinstance(prop.type, UuidType))

        # get DictionaryType properties
        dictProps = modelFuncs.filterProps(myType, lambda prop: isinstance(prop.type, DictionaryType))
        self.assertIsNotNone(dictProps)
        self.assertEqual(0, len(dictProps))

    def testGetComplexTypesInProperties(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertTrue(myType.extendsType is None)

        # should find the following sequence of properties
        expPropNameSequence = ['complexProp', 'complexRefProp', 'complexArrayRef']
        # Reasoning:
        # should ignore property ExampleType.complexDuplicate as it uses the same type as property ExampleType.complexRefProp
        # should ignore property ExampleType.complexRefProp.recursiveComplexReference as the search is not recursive!

        # corresponding sequence of complex types:
        expComplexTypeSequence = ['ExampleTypeInlineComplexProp', 'OtherComplexType', 'OtherComplexTypeForArray']

        actComplexTypes = modelFuncs.getComplexTypesInProperties(myType)
        self.assertIsNotNone(actComplexTypes)
        self.assertEqual(len(expComplexTypeSequence), len(actComplexTypes))

        for expName, actProp in zip(expComplexTypeSequence, actComplexTypes):
            self.assertEqual(expName, actProp.name)


    def testWithBaseTyp(self):
        self.assertTrue('True')