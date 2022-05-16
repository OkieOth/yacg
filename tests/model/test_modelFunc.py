import unittest

import os.path
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config

from yacg.model.model import IntegerType, IntegerTypeFormatEnum, NumberType, NumberTypeFormatEnum
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType, DictionaryType, Property
import yacg.model.modelFuncs as modelFuncs

def getComplexTypeNoBase():
    modelFile = 'tests/resources/models/json/examples/all_types.json'
    modelFileExists = os.path.isfile(modelFile)
    model = config.Model()
    model.schema = modelFile
    modelTypes = getModelFromJson(model, [])
    myType = modelTypes[0]
    return myType

def getComplexTypeWithBase():
    myType = getComplexTypeNoBase()

    idProp = Property()
    idProp.name = 'id'
    idProp.type = UuidType()

    nameProp = Property()
    nameProp.name = 'name'
    nameProp.type = StringType()


    commentProp = Property()
    commentProp.name = 'comment'
    commentProp.type = StringType()


    baseType = ComplexType()
    baseType.name = 'IdNamePair'
    baseType.properties.append(idProp)
    baseType.properties.append(nameProp)
    baseType.properties.append(commentProp)

    myType.extendsType = baseType
    baseType.extendedBy.append(myType)

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
        expPropNameSequence = ['inlineComplexProp', 'complexRefProp', 'complexArrayRef']
        # Reasoning:
        # should ignore property ExampleType.complexDuplicate as it uses the same type as property ExampleType.complexRefProp
        # should ignore property ExampleType.complexRefProp.recursiveComplexReference as the search is not recursive!

        # corresponding sequence of complex types:
        expComplexTypeSequence = ['ExampleTypeInlineComplexProp', 'OtherComplexType', 'OtherComplexTypeForArray']

        actComplexTypes = modelFuncs.getComplexTypesInProperties(myType)
        self.assertIsNotNone(actComplexTypes)
        self.assertEqual(len(expComplexTypeSequence), len(actComplexTypes))

        for expName, actType in zip(expComplexTypeSequence, actComplexTypes):
            self.assertEqual(expName, actType.name)


    def testHasPropertyOfTypeWithBaseTyp(self):
        myType = getComplexTypeWithBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertFalse(myType.extendsType is None)
        idProp = None
        for prop in modelFuncs.getFlattenProperties(myType):
            if prop.name == 'id' and isinstance(prop.type, UuidType):
                idProp = prop
                break
        self.assertIsNotNone(idProp)

        self.assertTrue(modelFuncs.hasPropertyOfType(myType, UuidType))


        # pop() removes item from list!
        prop = myType.properties.pop(3)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertTrue(prop.isArray)

        prop = myType.properties.pop(2)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertFalse(prop.isArray)

        self.assertTrue(modelFuncs.hasPropertyOfType(myType, UuidType))

        # remove relevant property from base type and try again
        myType.extendsType.properties.remove(idProp)
        self.assertFalse(modelFuncs.hasPropertyOfType(myType, UuidType))


    def testHasSinglePropertyOfTypeWithBaseType(self):
        myType = getComplexTypeWithBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertFalse(myType.extendsType is None)
        idProp = None
        for prop in modelFuncs.getFlattenProperties(myType):
            if prop.name == 'id' and isinstance(prop.type, UuidType):
                idProp = prop
                break
        self.assertIsNotNone(idProp)

        self.assertTrue(modelFuncs.hasSinglePropertyOfType(myType, UuidType))

        # pop() removes item from list!
        prop = myType.properties.pop(2)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertFalse(prop.isArray)
        self.assertTrue(modelFuncs.hasSinglePropertyOfType(myType, UuidType))

        # remove relevant property from base type and try again
        myType.extendsType.properties.remove(idProp)
        self.assertFalse(modelFuncs.hasSinglePropertyOfType(myType, UuidType))


    def testHasArrayPropertyOfTypeWithBaseType(self):
        myType = getComplexTypeWithBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertFalse(myType.extendsType is None)
        idProp = None
        for prop in modelFuncs.getFlattenProperties(myType):
            if prop.name == 'id' and isinstance(prop.type, UuidType):
                idProp = prop
                break
        self.assertIsNotNone(idProp)
        idProp.isArray = True

        self.assertTrue(modelFuncs.hasArrayPropertyOfType(myType, UuidType))

        # pop() removes item from list!
        prop = myType.properties.pop(3)
        self.assertTrue(isinstance(prop.type, UuidType))
        self.assertTrue(prop.isArray)
        self.assertTrue(modelFuncs.hasArrayPropertyOfType(myType, UuidType))

        # remove relevant property from base type and try again
        myType.extendsType.properties.remove(idProp)
        self.assertFalse(modelFuncs.hasArrayPropertyOfType(myType, UuidType))


    def testFilterPropsWithBaseType(self):
        myType = getComplexTypeWithBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertFalse(myType.extendsType is None)
        idProp = None
        for prop in modelFuncs.getFlattenProperties(myType):
            if prop.name == 'id' and isinstance(prop.type, UuidType):
                idProp = prop
                break
        self.assertIsNotNone(idProp)

        # get UuidType properties
        uuidProps = modelFuncs.filterProps(myType, lambda prop: isinstance(prop.type, UuidType))
        self.assertIsNotNone(uuidProps)
        self.assertEqual(3, len(uuidProps))

        for prop in uuidProps:
            self.assertTrue(isinstance(prop.type, UuidType))

        self.assertTrue(idProp in uuidProps)

        # remove relevant property from base type and try again
        myType.extendsType.properties.remove(idProp)
        uuidProps = modelFuncs.filterProps(myType, lambda prop: isinstance(prop.type, UuidType))
        self.assertIsNotNone(uuidProps)
        self.assertEqual(2, len(uuidProps))


    def testGetComplexTypesInPropertiesWithBaseType(self):
        myType = getComplexTypeWithBase()
        self.assertEqual('ExampleType', myType.name)
        self.assertFalse(myType.extendsType is None)
        idProp = None
        for prop in modelFuncs.getFlattenProperties(myType):
            if prop.name == 'id' and isinstance(prop.type, UuidType):
                idProp = prop
                break
        self.assertIsNotNone(idProp)

        # Move property inlineComplexProp from ExampleType to baseType IdNamePair!
        props =  modelFuncs.filterProps(myType, lambda prop: prop.name == 'inlineComplexProp')
        self.assertEqual(1, len(props))
        inlineComplex = props.pop(0)

        myType.properties.remove(inlineComplex)
        myType.extendsType.properties.append(inlineComplex)


        # should find the following sequence of properties
        expPropNameSequence = ['complexRefProp', 'complexArrayRef', 'inlineComplexProp']
        # Reasoning:
        # should ignore property ExampleType.complexDuplicate as it uses the same type as property ExampleType.complexRefProp
        # should ignore property ExampleType.complexRefProp.recursiveComplexReference as the search is not recursive!

        # corresponding sequence of complex types:
        expComplexTypeSequence = ['OtherComplexType', 'OtherComplexTypeForArray', 'ExampleTypeInlineComplexProp']

        actComplexTypes = modelFuncs.getComplexTypesInProperties(myType)
        self.assertIsNotNone(actComplexTypes)
        self.assertEqual(len(expComplexTypeSequence), len(actComplexTypes))

        for expName, actType in zip(expComplexTypeSequence, actComplexTypes):
            self.assertEqual(expName, actType.name)

        # remove relevant property from base type and try again
        myType.extendsType.properties.remove(inlineComplex)

         # should find the following sequence of properties
        expPropNameSequence = ['complexRefProp', 'complexArrayRef']
        # Reasoning:
        # property IdNamePair.inlineComplexProp was removed!
        # should ignore property ExampleType.complexDuplicate as it uses the same type as property ExampleType.complexRefProp
        # should ignore property ExampleType.complexRefProp.recursiveComplexReference as the search is not recursive!

        # corresponding sequence of complex types:
        expComplexTypeSequence = ['OtherComplexType', 'OtherComplexTypeForArray']

        actComplexTypes = modelFuncs.getComplexTypesInProperties(myType)
        self.assertIsNotNone(actComplexTypes)
        self.assertEqual(len(expComplexTypeSequence), len(actComplexTypes))

        for expName, actType in zip(expComplexTypeSequence, actComplexTypes):
            self.assertEqual(expName, actType.name)
