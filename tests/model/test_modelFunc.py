import unittest
import os
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config
import yacg.builder.impl.dictionaryBuilder as builder

from yacg.model.model import IntegerType, IntegerTypeFormatEnum, NumberType, NumberTypeFormatEnum, ObjectType
from yacg.model.model import StringType, UuidType
from yacg.model.model import TimeType, DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType, DictionaryType, Property
import yacg.model.modelFuncs as modelFuncs


def getComplexTypeNoBase():
    modelFile = 'tests/resources/models/json/examples/all_types.json'
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

    def testIsTimestampContained(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)

        self.assertTrue(modelFuncs.isTimestampContained([myType]))
        self.assertTrue(modelFuncs.isTypeContained([myType], DateTimeType))

        # dateTimeProp and dateTimeArr -> index 6 & 7
        dateTimeProp = myType.properties.pop(6)
        self.assertEqual('dateTimeProp', dateTimeProp.name)
        dateTimeArr = myType.properties.pop(6)
        self.assertEqual('dateTimeArr', dateTimeArr.name)

        self.assertFalse(modelFuncs.isTimestampContained([myType]))
        self.assertFalse(modelFuncs.isTypeContained([myType], DateTimeType))

    def testIsTimeContained(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)

        self.assertTrue(modelFuncs.isTimeContained([myType]))
        self.assertTrue(modelFuncs.isTypeContained([myType], TimeType))

        # timeProp and timeArr -> index 26 & 27
        timeProp = myType.properties.pop(26)
        self.assertEqual('timeProp', timeProp.name)
        timeArr = myType.properties.pop(26)
        self.assertEqual('timeArr', timeArr.name)

        self.assertFalse(modelFuncs.isTimeContained([myType]))
        self.assertFalse(modelFuncs.isTypeContained([myType], TimeType))

    def testIsObjectContained(self):
        myType = getComplexTypeNoBase()
        self.assertEqual('ExampleType', myType.name)

        self.assertTrue(modelFuncs.isObjectContained([myType]))
        self.assertTrue(modelFuncs.isTypeContained([myType], ObjectType))

        # objectProp and objectArr -> index 30 & 31
        objectProp = myType.properties.pop(30)
        self.assertEqual('objectProp', objectProp.name)
        objectArr = myType.properties.pop(30)
        self.assertEqual('objectArr', objectArr.name)

        self.assertFalse(modelFuncs.isObjectContained([myType]))
        self.assertFalse(modelFuncs.isTypeContained([myType], ObjectType))

    def testGetExternalRefStringsFromModelDict1(self):
        modelFile = 'resources/models/json/yacg_asyncapi_types.json'
        schemaAsDict = builder.getParsedSchemaFromJson(modelFile)
        references = []
        modelFuncs.getExternalRefStringsFromDict(schemaAsDict, references)
        self.assertEqual(len(references), 3)
        refHelperDict = modelFuncs.initReferenceHelperDict(references, modelFile)
        self.assertEqual(len(refHelperDict), 3)
        self.assertEqual(refHelperDict['./shared/info.json'].topLevelType, True)
        self.assertEqual(refHelperDict['./yacg_model_schema.json#/definitions/ComplexType'].topLevelType, False)
        self.assertEqual(refHelperDict['./yacg_model_schema.json#/definitions/Type'].topLevelType, False)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], True)
        extractedTypes[4].name = "InfoSection"
        extractedTypes[4].topLevelType = True
        modelFuncs.initTypesInReferenceHelperDict(refHelperDict, extractedTypes)
        for _, value in refHelperDict.items():
            self.assertIsNotNone(value.typeName)
            self.assertIsNotNone(value.type)

    def testGetReferenceStringsFromModelDict2(self):
        modelFile = 'tests/resources/models/yaml/examples/openapi_layer.yaml'
        schemaAsDict = builder.getParsedSchemaFromYaml(modelFile)
        references = []
        modelFuncs.getExternalRefStringsFromDict(schemaAsDict, references)
        self.assertEqual(len(references), 6)
        refHelperDict = modelFuncs.initReferenceHelperDict(references, modelFile)
        self.assertEqual(len(refHelperDict), 6)
        self.assertEqual(refHelperDict['./layer.yaml#/definitions/Layer'].topLevelType, False)
        self.assertEqual(refHelperDict['./layer.yaml#/definitions/DisplayConfig'].topLevelType, False)
        self.assertEqual(refHelperDict['./layer.yaml#/definitions/PointGeometry'].topLevelType, False)
        self.assertEqual(refHelperDict['./layer.yaml#/definitions/PointGeometryArray'].topLevelType, False)
        self.assertEqual(refHelperDict['./layer.yaml#/definitions/PointGeometryArrayArray'].topLevelType, False)
        self.assertEqual(refHelperDict['./layer.yaml#/definitions/PointGeometryArrayArrayArray'].topLevelType, False)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], True)
        modelFuncs.initTypesInReferenceHelperDict(refHelperDict, extractedTypes)
        for _, value in refHelperDict.items():
            self.assertIsNotNone(value.typeName)
            self.assertIsNotNone(value.type)

    def testGetLocalTypePrefix1(self):
        modelFile = 'resources/models/json/yacg_asyncapi_types.json'
        schemaAsDict = builder.getParsedSchemaFromJson(modelFile)
        self.assertEqual(modelFuncs.getLocalTypePrefix(schemaAsDict), "#/definitions/")

    def testGetLocalTypePrefix2(self):
        modelFile = 'tests/resources/models/yaml/examples/openapi_layer.yaml'
        schemaAsDict = builder.getParsedSchemaFromYaml(modelFile)
        self.assertEqual(modelFuncs.getLocalTypePrefix(schemaAsDict), "#/components/schemas/")

    def testTypeToJSONDict_1(self):
        modelFile = 'resources/models/json/yacg_asyncapi_types.json'
        schemaAsDict = builder.getParsedSchemaFromJson(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], True)
        localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)
        enumType1 = extractedTypes[10]
        self.assertTrue(isinstance(enumType1, EnumType))
        enumDict1 = modelFuncs.typeToJSONDict(enumType1, localTypePrefix)
        self.assertEqual(len(enumDict1), 2)
        self.assertEqual(enumDict1.get("type", None), "string")
        self.assertEqual(enumDict1.get("enum", None), ["topic", "direct", "fanout", "default", "headers"])
        dictType1 = extractedTypes[25]
        dictDict1 = modelFuncs.typeToJSONDict(dictType1, localTypePrefix)
        self.assertEqual(len(dictDict1), 3)
        self.assertEqual(dictDict1.get("type", None), "object")
        additionalPropertiesDict1 = dictDict1.get("additionalProperties", None)
        self.assertIsNotNone(additionalPropertiesDict1)
        self.assertEqual(additionalPropertiesDict1.get("type", None), "string")
        self.assertEqual(len(additionalPropertiesDict1), 1)
        allOfType = extractedTypes[8]
        allOfTypeDict = modelFuncs.typeToJSONDict(allOfType, localTypePrefix)
        pass

    def test_initIntegerTypeDict(self):
        ret1 = {}
        t = IntegerType()
        modelFuncs._initIntegerTypeDict(t, ret1)
        self.assertIsNone(ret1.get("format", None))
        t.format = IntegerTypeFormatEnum.INT64
        ret2 = {}
        modelFuncs._initIntegerTypeDict(t, ret2)
        self.assertEqual(ret2.get("format", None), 'int64')

    def test_initNumberTypeDict(self):
        ret1 = {}
        t = IntegerType()
        modelFuncs._initNumberTypeDict(t, ret1)
        self.assertIsNone(ret1.get("format", None))
        t.format = NumberTypeFormatEnum.DOUBLE
        ret2 = {}
        modelFuncs._initNumberTypeDict(t, ret2)
        self.assertEqual(ret2.get("format", None), 'double')
