import unittest
import os

import yacg.builder.impl.dictionaryBuilder as dictionaryBuilder
import yacg.model.openapi as openapi
import yacg.model.asyncapi as asyncapi


class TestAsyncApiParsing (unittest.TestCase):
    def test_asyncApiExample(self):
        modelFile = 'tests/resources/models/json/examples/asyncapi_test.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        print(modelTypes)

