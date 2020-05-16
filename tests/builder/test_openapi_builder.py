import unittest
import os

import yacg.builder.impl.dictionaryBuilder as dictionaryBuilder


class TestOpenApiParsing (unittest.TestCase):
    def test_defaultOpenApiExample(self):
        modelFile = 'tests/resources/models/json/examples/openapi_v3_example_small.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertIsNotNone(modelTypes)
