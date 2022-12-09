import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.model.model import DateType, DictionaryType, IntegerType, NumberType, NumberTypeFormatEnum, ObjectType, TimeType
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType, ArrayType
from yacg.model.modelFuncs import hasTag, getPropertiesThatHasTag, doesTypeOrAttribContainsType, getTypesWithTag, getTypesRelatedTagName, getTypeAndAllChildTypes, getTypeAndAllRelatedTypes, getNotUniqueTypeNames, makeTypeNamesUnique  # noqa: E501

import yacg.model.config as config


class TestJsonBuilder (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'tests/resources/models/json/examples/single_type_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(4, len(modelTypes))

        mainType = None
        anotherType = None
        innerComplexType = None
        for type in modelTypes:
            if type.name == 'SingleTypeSchema':
                mainType = type
            elif type.name == 'AnotherType':
                anotherType = type
            else:
                innerComplexType = type
        self.assertIsNotNone(mainType)
        self.assertEqual(4, len(mainType.properties))
        self.assertTrue(isinstance(mainType.properties[0].type, StringType))
        self.assertEqual(mainType.properties[0].type.minLength, 2)
        self.assertEqual(mainType.properties[0].type.maxLength, 200)
        self.assertEqual(mainType.properties[0].type.pattern, "^\\d$")

        self.assertTrue(isinstance(mainType.properties[1].type, NumberType))
        self.assertEqual(mainType.properties[1].type.minimum, 0.5)
        self.assertEqual(mainType.properties[1].type.maximum, 1.4)
        self.assertEqual(mainType.properties[1].type.exclusiveMinimum, -1.5)
        self.assertEqual(mainType.properties[1].type.exclusiveMaximum, -10.4)

        self.assertTrue(isinstance(mainType.properties[2].type, EnumType))
        self.assertTrue(isinstance(mainType.properties[3].type, ComplexType))

        self.assertIsNotNone(anotherType)
        self.assertEqual(2, len(anotherType.properties))
        self.assertTrue(isinstance(anotherType.properties[0].type, DateTimeType))
        self.assertTrue(isinstance(anotherType.properties[1].type, NumberType))

        self.assertTrue(isinstance(anotherType.properties[1].type, NumberType))
        self.assertIsNone(anotherType.properties[1].type.minimum)
        self.assertIsNone(anotherType.properties[1].type.maximum)
        self.assertIsNone(anotherType.properties[1].type.exclusiveMinimum)
        self.assertIsNone(anotherType.properties[1].type.exclusiveMaximum)

        self.assertIsNotNone(innerComplexType)
        self.assertEqual(3, len(innerComplexType.properties))
        self.assertTrue(isinstance(innerComplexType.properties[0].type, StringType))
        self.assertTrue(isinstance(innerComplexType.properties[1].type, IntegerType))
        self.assertTrue(isinstance(innerComplexType.properties[2].type, ComplexType))
        self.assertEqual(anotherType, innerComplexType.properties[2].type)

    def testSingleTypeSchema2(self):
        modelFile = 'resources/models/json/yacg_config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(16, len(modelTypes))

        self._checkUpType(0, 'Job', 4, modelTypes, ['models', 'tasks'])
        self._checkUpType(1, 'Model', 4, modelTypes, [])
        self._checkUpType(2, 'Task', 7, modelTypes, [])
        self._checkUpType(3, 'BlackWhiteListEntry', 2, modelTypes, ['name'])
        self._checkUpType(4, 'BlackWhiteListEntryTypeEnum', 0, modelTypes, [])
        self._checkUpType(5, 'SingleFileTask', 3, modelTypes, [])
        self._checkUpType(6, 'TemplateParam', 5, modelTypes, ['name', 'value'])
        self._checkUpType(7, 'MultiFileTask', 10, modelTypes, [])
        self._checkUpType(8, 'MultiFileTaskFileFilterTypeEnum', 0, modelTypes, [])
        self._checkUpType(9, 'RandomDataTask', 13, modelTypes, [], ('keyProperties', 'valuePools', 'arrays'))

    def testDoesTypeOrAttribContainsType(self):
        modelFile = 'resources/models/json/yacg_config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertTrue(doesTypeOrAttribContainsType(modelTypes[0], StringType))
        self.assertFalse(doesTypeOrAttribContainsType(modelTypes[0], UuidType))

    def testGetTypesWithTag(self):
        modelFile = 'tests/resources/models/json/examples/nibelheim.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        mongoTypes = getTypesWithTag(modelTypes, ["mongodb"])
        self.assertEqual(len(mongoTypes), 3)
        mineType = mongoTypes[0]
        self.assertEqual(mineType.name, 'Mine')
        dwarfsProperty = mineType.properties[4]
        self.assertEqual(dwarfsProperty.name, 'dwarfs')
        self.assertEqual(len(dwarfsProperty.tags), 3)
        self.assertEqual(dwarfsProperty.tags[0].name, 'oneTag')
        self.assertEqual(dwarfsProperty.tags[0].value, True)
        self.assertEqual(dwarfsProperty.tags[1].name, 'twoTag')
        self.assertEqual(dwarfsProperty.tags[1].value, 123)
        self.assertEqual(dwarfsProperty.tags[2].name, 'three.Tag')
        self.assertEqual(dwarfsProperty.tags[2].value, 'I am a string value')

    def testTopLevelEnum(self):
        modelFile = 'tests/resources/models/json/examples/top_level_enum.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertEqual(len(modelTypes), 1)
        enumType = modelTypes[0]
        self.assertEqual(enumType.name, 'DetectorEdgeType')
        self.assertTrue(isinstance(enumType, EnumType))
        self.assertIsNotNone(enumType.tags)
        self.assertEqual(len(enumType.tags), 1)
        self.assertEqual(enumType.tags[0].name, 'ordinalEnum')

    def testGetRelatedTypesToTag(self):
        modelFile = 'tests/resources/models/json/examples/nibelheim.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        mongoTypes = getTypesRelatedTagName(modelTypes, "mongodb")
        self.assertEqual(len(mongoTypes), 7)

    def testGetTypeAndAllChildTypes(self):
        modelFile = 'tests/resources/models/json/examples/nibelheim.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        mongoTypes = getTypeAndAllChildTypes(modelTypes[0])
        self.assertEqual(len(mongoTypes), 2)

    def testGetTypeAndAllRelatedTypes(self):
        modelFile = 'resources/models/json/yacg_openapi_paths.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        # 'OpenApiInfo'
        t1 = getTypeAndAllRelatedTypes(modelTypes[2])
        self.assertEqual(len(t1), 2)
        # 'PathType'
        t3 = getTypeAndAllRelatedTypes(modelTypes[27])
        self.assertEqual(len(t3), 10)

    def testSingleTypeSchema3(self):
        modelFile = 'tests/resources/models/json/examples/model_with_bytes.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(16, len(modelTypes))
        self._checkUpType(0, 'Job', 6, modelTypes, ['models', 'tasks'])
        self._checkUpType(1, 'Model', 4, modelTypes, [])
        self._checkUpType(2, 'Task', 8, modelTypes, [])
        self._checkUpType(3, 'BlackWhiteListEntry', 2, modelTypes, ['name'])
        self._checkUpType(4, 'BlackWhiteListEntryTypeEnum', 0, modelTypes, [])
        self._checkUpType(5, 'SingleFileTask', 3, modelTypes, [])
        self._checkUpType(6, 'TemplateParam', 6, modelTypes, ['name', 'value'])
        self._checkUpType(7, 'MultiFileTask', 10, modelTypes, [])
        self._checkUpType(8, 'MultiFileTaskFileFilterTypeEnum', 0, modelTypes, [])
        self._checkUpType(9, 'RandomDataTask', 13, modelTypes, [], ('keyProperties', 'valuePools', 'arrays'))
        self.assertEqual('bValues', modelTypes[2].properties[1].name)
        self.assertTrue(modelTypes[2].properties[1].isArray)
        self.assertTrue(isinstance(modelTypes[2].properties[1].type, BytesType))
        self.assertEqual('bValue', modelTypes[6].properties[2].name)
        self.assertFalse(modelTypes[6].properties[2].isArray)
        self.assertTrue(isinstance(modelTypes[6].properties[2].type, BytesType))

        jobType = modelTypes[0]
        self.assertEqual(jobType.properties[4].type.format, NumberTypeFormatEnum.FLOAT)
        self.assertEqual(jobType.properties[5].type.format, NumberTypeFormatEnum.DOUBLE)

    def testSchemaWithExternalRef(self):
        modelFile = 'tests/resources/models/json/examples/schema_with_external_ref.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(4, len(modelTypes))
        self._checkUpType(0, 'OneType', 2, modelTypes, [])
        self._checkUpType(1, 'TwoType', 4, modelTypes, [])
        # TwoType->implicitRef
        self.assertIsNotNone(modelTypes[1].properties[3].foreignKey.type)
        self.assertIsNotNone(modelTypes[1].properties[3].foreignKey.property)
        self.assertEqual(modelTypes[1].properties[2].type, modelTypes[1].properties[3].foreignKey.type)
        self.assertEqual(modelTypes[1].properties[3].foreignKey.property.name, modelTypes[1].properties[3].foreignKey.propertyName)  # noqa: E501
        self._checkUpType(2, 'AnotherType', 2, modelTypes, [])
        self._checkUpType(3, 'DemoEnum', 0, modelTypes, [])

    def testSchemaWithHttpRef(self):
        modelFile = 'tests/resources/models/json/examples/schema_with_http_ref.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(4, len(modelTypes))
        self._checkUpType(0, 'OneType', 2, modelTypes, [])
        self._checkUpType(1, 'TwoType', 4, modelTypes, [])
        # TwoType->implicitRef
        self.assertIsNotNone(modelTypes[1].properties[3].foreignKey.type)
        self.assertEqual(modelTypes[1].properties[2].type, modelTypes[1].properties[3].foreignKey.type)
        self._checkUpType(2, 'AnotherType', 2, modelTypes, [])
        self._checkUpType(3, 'DemoEnum', 0, modelTypes, [])

    def testSchemaWithExternalCircularRefs(self):
        modelFile = 'tests/resources/models/json/examples/schema_with_circular_deps.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(5, len(modelTypes))

        self._checkUpType(0, 'OneType', 2, modelTypes, [])
        self._checkUpType(1, 'RefBackType', 4, modelTypes, [])
        self._checkUpType(2, 'RefBackType2', 3, modelTypes, [])
        self._checkUpType(3, 'TwoType', 3, modelTypes, [])
        self._checkUpType(4, 'AnotherType', 2, modelTypes, [])

    def testSimpleAllOf(self):
        modelFile = 'tests/resources/models/json/examples/simple_allof.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(6, len(modelTypes))
        self._checkUpType(2, 'SimpleAllOfSchema', 1, modelTypes, [])
        self._checkUpType(0, 'Address', 3, modelTypes, [])
        self._checkUpType(1, 'SimpleAllOfSchemaTypeEnum', 0, modelTypes, [])

        addressType = modelTypes[0]
        self.assertEqual(4, addressType.properties[0].ordinal)
        self.assertEqual(5, addressType.properties[1].ordinal)
        self.assertEqual(6, addressType.properties[2].ordinal)

    def testSophisticatedAllOf(self):
        modelFile = 'tests/resources/models/json/examples/more_sophisticated_allof.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(10, len(modelTypes))
        type = self._checkUpType(5, 'MoreSophisticatedAllOf', 1, modelTypes, [])
        self.assertIsNotNone(type.extendsType)
        address = self._checkUpType(0, 'Address', 3, modelTypes, [])
        self.assertEqual(type.extendsType, address)
        self._checkUpType(4, 'MoreSophisticatedAllOfTypeEnum', 0, modelTypes, [])
        self._checkUpType(9, 'MainAddress', 2, modelTypes, [])
        self._checkUpType(8, 'MainAddressComplex', 3, modelTypes, [])
        self.assertEqual(len(modelTypes[1].properties), 0)
        self.assertEqual(modelTypes[1].extendsType, modelTypes[0])
        self.assertEqual(len(modelTypes[0].properties), 3)

    def testTags(self):
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        metaModelTypes = []
        self.assertIsNotNone(modelTypes)
        tagType = None
        propertyType = None
        complexTypeType = None
        for type in modelTypes:
            if hasTag('metaModelType', type):
                metaModelTypes.append(type.name)
            if type.name == 'Tag':
                tagType = type
            elif type.name == 'Property':
                propertyType = type
            elif type.name == 'ComplexType':
                complexTypeType = type
            self.assertEqual('yacg.model.model', type.domain)
        self.assertIsNotNone(tagType)
        constructorValueProps1 = getPropertiesThatHasTag('constructorValue', tagType)
        self.assertEqual(2, len(constructorValueProps1))
        self.assertIsNotNone(propertyType)
        constructorValueProps2 = getPropertiesThatHasTag('constructorValue', propertyType)
        self.assertEqual(2, len(constructorValueProps2))
        self.assertIsNotNone(complexTypeType)
        constructorValueProps3 = getPropertiesThatHasTag('constructorValue', complexTypeType)
        self.assertEqual(0, len(constructorValueProps3))

        expectedMetaModelTypes = [
            'Type',
            'ObjectType',
            'IntegerType',
            'NumberType',
            'BooleanType',
            'StringType',
            'UuidType',
            'EnumType',
            'DateType',
            'TimeType',
            'DateTimeType',
            'DurationType',
            'BytesType',
            'ComplexType',
            'DictionaryType',
            'ArrayType'
        ]
        self.assertEqual(expectedMetaModelTypes, metaModelTypes)

    def _checkUpType(self, position, typeName, propCount, modelTypes, requiredArray, noArrayProperties=()):
        type = modelTypes[position]
        self.assertIsNotNone(type)
        self.assertIsNotNone(type.source)
        sourceExists = os.path.isfile(type.source)
        self.assertTrue('source file exists: ' + type.source, sourceExists)
        self.assertEqual(typeName, type.name)
        if isinstance(type, EnumType):
            return type
        self.assertEqual(propCount, len(type.properties))
        for prop in type.properties:
            self.assertIsNotNone(prop.type, "property w/o a type: %s.%s" % (typeName, prop.name))
            if prop.name.endswith('s') or prop.name.endswith('ed'):
                if prop.name not in noArrayProperties:
                    self.assertTrue(prop.isArray, "property has to be an array: %s.%s" % (typeName, prop.name))
            else:
                self.assertFalse(prop.isArray, "property should be no array: %s.%s" % (typeName, prop.name))
        if len(requiredArray) > 0:
            for required in requiredArray:
                found = False
                for prop in type.properties:
                    if prop.name == required:
                        found = True
                        self.assertTrue(prop.required)
                        break
                self.assertTrue(found)
        return type

    def testDictionary(self):
        modelFile = 'tests/resources/models/json/examples/simple_dictionary.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(1, len(modelTypes))
        self.assertTrue(isinstance(modelTypes[0], DictionaryType))
        self.assertIsNotNone(modelTypes[0].valueType)
        self.assertTrue(isinstance(modelTypes[0].valueType, StringType))

    def testDictionary2(self):
        modelFile = 'tests/resources/models/json/examples/simple_dictionary2.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(2, len(modelTypes))
        self.assertTrue(isinstance(modelTypes[0], DictionaryType))
        self.assertIsNotNone(modelTypes[0].valueType)
        self.assertTrue(isinstance(modelTypes[0].valueType, ComplexType))

    def testExternalEnum(self):
        modelFile = 'tests/resources/models/json/examples/ExternalEnum.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(1, len(modelTypes))
        self.assertTrue(modelTypes[0], EnumType)
        self.assertIsNone(modelTypes[0].valuesMap)

    def testExternalEnumWithValues(self):
        modelFile = 'tests/resources/models/json/examples/ExternalEnumWithValues.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(1, len(modelTypes))
        self.assertTrue(modelTypes[0], EnumType)
        self.assertIsNotNone(modelTypes[0].valuesMap)
        keys = modelTypes[0].valuesMap.keys()
        self.assertEqual(3, len(keys))
        self.assertEqual('10', modelTypes[0].valuesMap['A'])
        self.assertEqual('20', modelTypes[0].valuesMap['B'])
        self.assertEqual('30', modelTypes[0].valuesMap['C'])

    def testExternalEnumWithValues2(self):
        modelFile = 'tests/resources/models/json/examples/openapi_v3_example_refs2.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes[4].valuesMap)
        keys = modelTypes[4].valuesMap.keys()
        self.assertEqual(3, len(keys))
        self.assertEqual('10', modelTypes[4].valuesMap['A'])
        self.assertEqual('20', modelTypes[4].valuesMap['B'])
        self.assertEqual('30', modelTypes[4].valuesMap['C'])

    def testEvilEnum2(self):
        modelFile = 'tests/resources/models/json/examples/evil_enum_with_values.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])

        self.assertTrue(modelTypes[0], EnumType)
        self.assertIsNotNone(modelTypes[0].valuesMap)
        self.assertEqual('true', modelTypes[0].valuesMap['1'])

    def testEvilIntEnum(self):
        modelFile = 'tests/resources/models/json/examples/evil_int_enum.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertTrue(modelTypes[0], EnumType)
        self.assertIsNotNone(modelTypes[0].type)
        self.assertTrue(isinstance(modelTypes[0].type, IntegerType))
        self.assertEqual(len(modelTypes[0].numValues), 3)
        self.assertEqual(modelTypes[0].numValues[0], 1)
        self.assertEqual(modelTypes[0].numValues[1], 2)
        self.assertEqual(modelTypes[0].numValues[2], 3)

    def testEvilFloatEnum(self):
        modelFile = 'tests/resources/models/json/examples/evil_float_enum.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertEqual(len(modelTypes), 4)
        self.assertTrue(modelTypes[0], EnumType)
        self.assertIsNotNone(modelTypes[0].type)
        self.assertTrue(isinstance(modelTypes[0].type, NumberType))
        self.assertEqual(len(modelTypes[0].numValues), 4)
        self.assertEqual(modelTypes[0].numValues[0], 0.4)
        self.assertEqual(modelTypes[0].numValues[1], 2.3)
        self.assertEqual(modelTypes[0].numValues[2], 3.5)
        self.assertEqual(modelTypes[0].numValues[3], 4.2)

        self.assertTrue(isinstance(modelTypes[1].type, DateTimeType))
        self.assertEqual(len(modelTypes[1].values), 2)
        self.assertTrue(isinstance(modelTypes[2].type, DateType))
        self.assertEqual(len(modelTypes[2].values), 3)
        self.assertTrue(isinstance(modelTypes[3].type, TimeType))
        self.assertEqual(len(modelTypes[3].values), 4)


    def testEvilArray(self):
        modelFile = 'tests/resources/models/json/examples/evil_array.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(len(modelTypes), 3)
        self.assertEqual(len(modelTypes[0].properties), 3)
        self.assertEqual(modelTypes[0].properties[0].arrayDimensions, 1)
        self.assertIsNotNone(modelTypes[0].properties[0].type)
        self.assertEqual(modelTypes[0].properties[1].arrayDimensions, 2)
        self.assertIsNotNone(modelTypes[0].properties[1].type)
        self.assertEqual(modelTypes[0].properties[2].arrayDimensions, 3)
        self.assertIsNotNone(modelTypes[0].properties[2].type)

    def testDictionary4(self):
        modelFile = 'tests/resources/models/json/examples/simple_allof_with_dictionary.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(5, len(modelTypes))
        self.assertTrue(isinstance(modelTypes[0], ComplexType))
        self.assertTrue(isinstance(modelTypes[1], EnumType))
        self.assertTrue(isinstance(modelTypes[2], ComplexType))
        self.assertTrue(isinstance(modelTypes[3], DictionaryType))
        self.assertTrue(isinstance(modelTypes[4], DictionaryType))

        self.assertTrue(isinstance(modelTypes[3].valueType, IntegerType))
        self.assertTrue(isinstance(modelTypes[4].valueType, StringType))

        self.assertTrue(isinstance(modelTypes[0].properties[2].type, StringType))
        self.assertTrue(isinstance(modelTypes[0].properties[3].type, ObjectType))
        self.assertTrue(isinstance(modelTypes[0].properties[4].type, DictionaryType))
        self.assertTrue(isinstance(modelTypes[0].properties[4].type.valueType, IntegerType))
        self.assertTrue(isinstance(modelTypes[0].properties[5].type, DictionaryType))
        self.assertTrue(isinstance(modelTypes[0].properties[5].type.valueType, StringType))

    def testEndlessRecursion(self):
        modelFile = 'resources/models/json/yacg_asyncapi_types.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)

    def testForDoubleTypeNames(self):
        modelFile = 'tests/resources/models/json/examples/simple_allof_with_dictionary.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(5, len(modelTypes))
        self.assertEqual([], (getNotUniqueTypeNames(modelTypes)))
        modelTypes.append(modelTypes[0])
        self.assertEqual(6, len(modelTypes))
        self.assertEqual(['Address'], (getNotUniqueTypeNames(modelTypes)))
        modelTypes.append(modelTypes[0])
        self.assertEqual(7, len(modelTypes))
        self.assertEqual(['Address'], (getNotUniqueTypeNames(modelTypes)))
        modelTypes.append(modelTypes[2])
        self.assertEqual(8, len(modelTypes))
        self.assertEqual(['Address', 'SimpleAllOfSchema'], (getNotUniqueTypeNames(modelTypes)))

    def testFixDoubleTypeNames(self):
        modelFile = 'tests/resources/models/json/examples/schema_with_external_ref_2.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(7, len(modelTypes))
        notUniqueTypeNames = getNotUniqueTypeNames(modelTypes)
        self.assertEqual(2, len(notUniqueTypeNames))
        makeTypeNamesUnique(modelTypes, notUniqueTypeNames)
        self.assertEqual(7, len(modelTypes))
        notUniqueTypeNames2 = getNotUniqueTypeNames(modelTypes)
        self.assertEqual(0, len(notUniqueTypeNames2))
        self.assertEqual('AnotherType_2', modelTypes[3].name)
        self.assertEqual('MySecondType_2', modelTypes[6].name)

    def testTopLevelArrayType(self):
        modelFile = 'tests/resources/models/json/examples/top_level_array_type.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(1, len(modelTypes))
        arrayType = modelTypes[0]
        self.assertTrue(isinstance(arrayType, ArrayType))
        self.assertEqual(arrayType.name, 'DemoArrayType')
        self.assertEqual(arrayType.arrayConstraints[0].arrayMinItems, 2)
        self.assertEqual(arrayType.arrayConstraints[0].arrayMaxItems, 10)
        self.assertEqual(arrayType.arrayConstraints[0].arrayUniqueItems, True)
        self.assertIsNotNone(arrayType.itemsType)
        self.assertTrue(isinstance(arrayType.itemsType, IntegerType))
        self.assertEqual(len(arrayType.tags), 3)
        self.assertEqual(arrayType.tags[0].name, "test")
        self.assertEqual(arrayType.tags[0].value, True)
        self.assertEqual(arrayType.tags[1].name, "another-one")
        self.assertEqual(arrayType.tags[1].value, "a value")
        self.assertEqual(arrayType.tags[2].name, "thirdTag")
        self.assertEqual(arrayType.tags[2].value, 233)

    def testTopLevelArrayType2(self):
        modelFile = 'tests/resources/models/json/examples/top_level_array_type2.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(2, len(modelTypes))
        arrayType = modelTypes[1]
        self.assertTrue(isinstance(arrayType, ArrayType))
        self.assertEqual(arrayType.name, 'DemoArrayType2')
        self.assertEqual(arrayType.arrayConstraints[0].arrayMinItems, 2)
        self.assertEqual(arrayType.arrayConstraints[0].arrayMaxItems, 2)
        self.assertEqual(arrayType.arrayConstraints[0].arrayUniqueItems, False)
        self.assertIsNotNone(arrayType.itemsType)
        self.assertEqual(arrayType.itemsType.name, 'SomeOtherType')

    def testTopLevelArrayType3(self):
        modelFile = 'tests/resources/models/json/examples/top_level_array_type3.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(3, len(modelTypes))
        arrayType = modelTypes[1]
        self.assertTrue(isinstance(arrayType, ArrayType))
        self.assertEqual(arrayType.name, 'InnerArrayType')
        self.assertEqual(len(arrayType.arrayConstraints), 1)
        self.assertIsNotNone(arrayType.itemsType)
        refType = modelTypes[2]
        self.assertEqual(refType.properties[2].name, 'things')
        self.assertEqual(refType.properties[2].isArray, True)
        self.assertEqual(refType.properties[2].arrayDimensions, 1)
        self.assertEqual(refType.properties[2].type.name, 'SomeOtherType')

    def testTopLevelDictionaryType(self):
        modelFile = 'tests/resources/models/json/examples/top_level_dictionary_type.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(1, len(modelTypes))
        dictType = modelTypes[0]
        self.assertTrue(isinstance(dictType, DictionaryType))
        self.assertEqual(dictType.name, 'DemoDictType')
        self.assertIsNotNone(dictType.valueType)
        self.assertTrue(isinstance(dictType.valueType, IntegerType))

    def testTopLevelDictType2(self):
        modelFile = 'tests/resources/models/json/examples/top_level_dictionary_type2.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(2, len(modelTypes))
        dictType = modelTypes[0]
        self.assertTrue(isinstance(dictType, DictionaryType))
        self.assertEqual(dictType.name, 'DemoDictType2')
        self.assertIsNotNone(dictType.valueType)
        self.assertTrue(isinstance(dictType.valueType, ComplexType))
        self.assertEqual(dictType.valueType.name, 'SomeOtherType')

    def testTopLevelDictType3(self):
        modelFile = 'tests/resources/models/json/examples/top_level_dictionary_type3.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(3, len(modelTypes))
        dictType = modelTypes[0]
        self.assertTrue(isinstance(dictType, DictionaryType))
        self.assertEqual(dictType.name, 'InnerDictionaryType')
        self.assertIsNotNone(dictType.valueType)
        refType = modelTypes[2]
        self.assertEqual(refType.properties[2].name, 'things')
        self.assertEqual(refType.properties[2].isArray, False)
        self.assertEqual(refType.properties[2].type.name, 'InnerDictionaryType')
        self.assertTrue(isinstance(refType.properties[2].type, DictionaryType))

    def testMultiDimensionalArraysConstraints(self):
        modelFile = 'tests/resources/models/yaml/examples/layer_small.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(len(modelTypes), 4)
        self.assertEqual(modelTypes[0].arrayDimensions, 1)
        self.assertEqual(len(modelTypes[0].arrayConstraints), 1)
        self.assertEqual(modelTypes[0].arrayConstraints[0].arrayMinItems, 2)
        self.assertEqual(modelTypes[0].arrayConstraints[0].arrayMaxItems, 2)

        self.assertEqual(modelTypes[1].arrayDimensions, 2)
        self.assertEqual(len(modelTypes[1].arrayConstraints), 2)
        self.assertIsNone(modelTypes[1].arrayConstraints[0].arrayMinItems)
        self.assertIsNone(modelTypes[1].arrayConstraints[0].arrayMaxItems)
        self.assertEqual(modelTypes[1].arrayConstraints[1].arrayMinItems, 2)
        self.assertEqual(modelTypes[1].arrayConstraints[1].arrayMaxItems, 2)

        self.assertEqual(modelTypes[2].arrayDimensions, 3)
        self.assertEqual(len(modelTypes[2].arrayConstraints), 3)
        self.assertIsNone(modelTypes[2].arrayConstraints[0].arrayMinItems)
        self.assertIsNone(modelTypes[2].arrayConstraints[0].arrayMaxItems)
        self.assertIsNone(modelTypes[2].arrayConstraints[1].arrayMinItems)
        self.assertIsNone(modelTypes[2].arrayConstraints[1].arrayMaxItems)
        self.assertEqual(modelTypes[2].arrayConstraints[2].arrayMinItems, 2)
        self.assertEqual(modelTypes[2].arrayConstraints[2].arrayMaxItems, 2)

        self.assertEqual(modelTypes[3].arrayDimensions, 4)
        self.assertEqual(len(modelTypes[3].arrayConstraints), 4)
        self.assertIsNone(modelTypes[3].arrayConstraints[0].arrayMinItems)
        self.assertIsNone(modelTypes[3].arrayConstraints[0].arrayMaxItems)
        self.assertIsNone(modelTypes[3].arrayConstraints[1].arrayMinItems)
        self.assertIsNone(modelTypes[3].arrayConstraints[1].arrayMaxItems)
        self.assertIsNone(modelTypes[3].arrayConstraints[2].arrayMinItems)
        self.assertIsNone(modelTypes[3].arrayConstraints[2].arrayMaxItems)
        self.assertEqual(modelTypes[3].arrayConstraints[3].arrayMinItems, 2)
        self.assertEqual(modelTypes[3].arrayConstraints[3].arrayMaxItems, 2)

    def testMultiDimensionalArraysConstraintsMixed(self):
        modelFile = 'tests/resources/models/yaml/examples/layer_small2.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(len(modelTypes), 4)
        self.assertEqual(modelTypes[0].arrayDimensions, 3)
        self.assertEqual(len(modelTypes[0].arrayConstraints), 3)
        self.assertIsNone(modelTypes[0].arrayConstraints[0].arrayMinItems)
        self.assertIsNone(modelTypes[0].arrayConstraints[0].arrayMaxItems)
        self.assertIsNone(modelTypes[0].arrayConstraints[1].arrayMinItems)
        self.assertIsNone(modelTypes[0].arrayConstraints[1].arrayMaxItems)
        self.assertEqual(modelTypes[0].arrayConstraints[2].arrayMinItems, 2)
        self.assertEqual(modelTypes[0].arrayConstraints[2].arrayMaxItems, 2)

        self.assertEqual(modelTypes[1].arrayDimensions, 4)
        self.assertEqual(len(modelTypes[1].arrayConstraints), 4)
        self.assertIsNone(modelTypes[1].arrayConstraints[0].arrayMinItems)
        self.assertIsNone(modelTypes[1].arrayConstraints[0].arrayMaxItems)
        self.assertIsNone(modelTypes[1].arrayConstraints[1].arrayMinItems)
        self.assertIsNone(modelTypes[1].arrayConstraints[1].arrayMaxItems)
        self.assertIsNone(modelTypes[1].arrayConstraints[2].arrayMinItems)
        self.assertIsNone(modelTypes[1].arrayConstraints[2].arrayMaxItems)
        self.assertEqual(modelTypes[1].arrayConstraints[3].arrayMinItems, 2)
        self.assertEqual(modelTypes[1].arrayConstraints[3].arrayMaxItems, 2)

        self.assertEqual(modelTypes[2].arrayDimensions, 1)
        self.assertEqual(len(modelTypes[2].arrayConstraints), 1)
        self.assertEqual(modelTypes[2].arrayConstraints[0].arrayMinItems, 2)
        self.assertEqual(modelTypes[2].arrayConstraints[0].arrayMaxItems, 2)

        self.assertEqual(modelTypes[3].arrayDimensions, 2)
        self.assertEqual(len(modelTypes[3].arrayConstraints), 2)
        self.assertIsNone(modelTypes[3].arrayConstraints[0].arrayMinItems)
        self.assertIsNone(modelTypes[3].arrayConstraints[0].arrayMaxItems)
        self.assertEqual(modelTypes[3].arrayConstraints[1].arrayMinItems, 2)
        self.assertEqual(modelTypes[3].arrayConstraints[1].arrayMaxItems, 2)

    def testMultiDimensionalArrays(self):
        modelFile = 'resources/models/yaml/layer.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(12, len(modelTypes))
        arrayType1 = modelTypes[8]
        arrayType2 = modelTypes[9]
        arrayType3 = modelTypes[10]
        self.assertTrue(isinstance(arrayType1, ArrayType))
        self.assertTrue(isinstance(arrayType2, ArrayType))
        self.assertTrue(isinstance(arrayType3, ArrayType))
        self.assertEqual(arrayType1.arrayDimensions, 1)
        self.assertEqual(arrayType2.arrayDimensions, 2)
        self.assertEqual(arrayType3.arrayDimensions, 3)
        self.assertTrue(isinstance(arrayType1.itemsType, NumberType))
        self.assertTrue(isinstance(arrayType2.itemsType, NumberType))
        self.assertTrue(isinstance(arrayType3.itemsType, NumberType))
        geometry = modelTypes[2]
        self.assertEqual(geometry.properties[0].name, 'point')
        self.assertEqual(geometry.properties[0].arrayDimensions, 1)
        self.assertEqual(geometry.properties[1].name, 'multiPoint')
        self.assertEqual(geometry.properties[1].arrayDimensions, 2)
        self.assertEqual(geometry.properties[2].name, 'lineString')
        self.assertEqual(geometry.properties[2].arrayDimensions, 2)
        self.assertEqual(geometry.properties[3].name, 'multiLineString')
        self.assertEqual(geometry.properties[3].arrayDimensions, 3)
        self.assertEqual(geometry.properties[4].name, 'polygon')
        self.assertEqual(geometry.properties[4].arrayDimensions, 3)
        self.assertEqual(geometry.properties[5].name, 'multiPolygon')
        self.assertEqual(geometry.properties[5].arrayDimensions, 4)

    def testEnumValues(self):
        modelFile = 'tests/resources/models/json/examples/query-info.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        foundEnumTypes = 0
        for t in modelTypes:
            if isinstance(t, EnumType):
                foundEnumTypes = foundEnumTypes + 1
                self.assertTrue(len(t.values) > 0)
        self.assertEqual(foundEnumTypes, 2)


if __name__ == '__main__':
    unittest.main()
