import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType
from yacg.model.model import DateTimeType, BytesType
from yacg.model.model import EnumType, ComplexType
from yacg.model.modelFuncs import hasTag, getPropertiesThatHasTag

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

    def testSingleTypeSchema3(self):
        modelFile = 'tests/resources/models/json/examples/model_with_bytes.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(16, len(modelTypes))
        self._checkUpType(0, 'Job', 4, modelTypes, ['models', 'tasks'])
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
        self.assertIsNotNone(modelTypes[1].properties[3].foreignKey)
        self.assertEqual(modelTypes[1].properties[2].type, modelTypes[1].properties[3].foreignKey)
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
        self.assertEqual(3, len(modelTypes))
        self._checkUpType(0, 'SimpleAllOfSchema', 1, modelTypes, [])
        self._checkUpType(1, 'Address', 3, modelTypes, [])
        self._checkUpType(2, 'SimpleAllOfSchemaTypeEnum', 0, modelTypes, [])

        addressType = modelTypes[1]
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
        self.assertEqual(7, len(modelTypes))
        type = self._checkUpType(0, 'MoreSophisticatedAllOf', 1, modelTypes, [])
        self.assertIsNotNone(type.extendsType)
        address = self._checkUpType(1, 'Address', 3, modelTypes, [])
        self.assertEqual(type.extendsType, address)
        self._checkUpType(2, 'MoreSophisticatedAllOfTypeEnum', 0, modelTypes, [])
        self._checkUpType(3, 'MainAddress', 2, modelTypes, [])
        self._checkUpType(6, 'MainAddressComplex', 3, modelTypes, [])

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
            'IntegerType',
            'NumberType',
            'BooleanType',
            'StringType',
            'UuidType',
            'EnumType',
            'DateType',
            'DateTimeType',
            'BytesType',
            'ComplexType'
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


if __name__ == '__main__':
    unittest.main()
