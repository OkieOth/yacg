import unittest
import os.path
from yacg.builder.impl.dictionaryBuilder import getParsedSchemaFromJson, getParsedSchemaFromYaml


class TestJsonBuilder (unittest.TestCase):
    def _testYamlAndJsonEquality(self, jsonModelFile, yamlModelFile):
        jsonModelFileExists = os.path.isfile(jsonModelFile)
        self.assertTrue('json model file exists: ' + jsonModelFile, jsonModelFileExists)

        yamlModelFileExists = os.path.isfile(yamlModelFile)
        self.assertTrue('yaml model file exists: ' + yamlModelFile, yamlModelFileExists)

        parsedJsonSchema = getParsedSchemaFromJson(jsonModelFile)
        self.assertIsNotNone(parsedJsonSchema)
        parsedYamlSchema = getParsedSchemaFromYaml(yamlModelFile)
        self.assertIsNotNone(parsedYamlSchema)

        self.assertEqual(parsedYamlSchema, parsedYamlSchema)

    def testConfigSchemaEquality(self):
        jsonModelFile = 'resources/models/json/config_schema.json'
        yamlModelFile = 'resources/models/yaml/config_schema.yaml'
        self._testYamlAndJsonEquality(jsonModelFile, yamlModelFile)

    def testSwagger2Equality(self):
        jsonModelFile = 'tests/resources/models/json/examples/swagger_v2_example.json'
        yamlModelFile = 'tests/resources/models/yaml/examples/swagger_v2_example.yaml'
        self._testYamlAndJsonEquality(jsonModelFile, yamlModelFile)

    def testOpenApi3Equality(self):
        jsonModelFile = 'tests/resources/models/json/examples/openapi_v3_example.json'
        yamlModelFile = 'tests/resources/models/yaml/examples/openapi_v3_example.yaml'
        self._testYamlAndJsonEquality(jsonModelFile, yamlModelFile)
