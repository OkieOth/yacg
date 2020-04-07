import unittest
import os.path
from yacg.builder.impl.dictionaryBuilder import getParsedSchemaFromJson, getParsedSchemaFromYaml


class TestJsonBuilder (unittest.TestCase):
    def testYamlAndJsonEquality(self):
        jsonModelFile = 'resources/models/json/config_schema.json'
        jsonModelFileExists = os.path.isfile(jsonModelFile)
        self.assertTrue('json model file exists: ' + jsonModelFile, jsonModelFileExists)

        yamlModelFile = 'resources/models/yaml/config_schema.yaml'
        yamlModelFileExists = os.path.isfile(yamlModelFile)
        self.assertTrue('yaml model file exists: ' + yamlModelFile, yamlModelFileExists)

        parsedJsonSchema = getParsedSchemaFromJson(jsonModelFile)
        self.assertIsNotNone(parsedJsonSchema)
        parsedYamlSchema = getParsedSchemaFromYaml(yamlModelFile)
        self.assertIsNotNone(parsedYamlSchema)

        self.assertEqual(parsedYamlSchema, parsedYamlSchema)
