import unittest
import os

from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.model.model import ComplexType


class TestSwagger (unittest.TestCase):
    def test_swaggerV2Json(self):
        modelFile = 'resources/models/json/examples/swagger_v2_example.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        modelTypes = getModelFromJson(modelFile, [])
        self._checkUpTypes(modelTypes)

    def test_openApiV3Json(self):
        modelFile = 'resources/models/json/examples/openapi_v3_example.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        modelTypes = getModelFromJson(modelFile, [])
        self._checkUpTypes(modelTypes)

    def test_swaggerV2Yaml(self):
        modelFile = 'resources/models/yaml/examples/swagger_v2_example.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        modelTypes = getModelFromYaml(modelFile, [])
        self._checkUpTypes(modelTypes)

    def test_openApiV3Yaml(self):
        modelFile = 'resources/models/yaml/examples/openapi_v3_example.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        modelTypes = getModelFromYaml(modelFile, [])
        self._checkUpTypes(modelTypes)

    def test_compareSwaggerV2(self):
        modelFileJson = 'resources/models/json/examples/swagger_v2_example.json'
        modelTypesJson = getModelFromJson(modelFileJson, [])
        modelFileYaml = 'resources/models/yaml/examples/swagger_v2_example.yaml'
        modelTypesYaml = getModelFromYaml(modelFileYaml, [])
        self.assertEqual(len(modelTypesJson), len(modelTypesYaml))
        for i in range(len(modelTypesJson)):
            typeJson = modelTypesJson[i]
            typeYaml = modelTypesYaml[i]
            self.assertEqual(str(type(typeJson)), str(type(typeYaml)))
            if isinstance(typeJson, ComplexType):
                self.assertEqual(len(typeJson.properties), len(typeYaml.properties))

    def _checkUpTypes(self, modelTypes):
        self.assertIsNotNone(modelTypes)
        self.assertEqual(8, len(modelTypes))
        for type in modelTypes:
            if not isinstance(type, ComplexType):
                continue
            self.assertTrue(len(type.properties) > 0)
            for prop in type.properties:
                self.assertIsNotNone(prop.type, "property w/o a type: %s.%s" % (type.name, prop.name))
        return type
