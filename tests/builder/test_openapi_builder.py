import unittest
import os

import yacg.builder.impl.dictionaryBuilder as dictionaryBuilder
import yacg.model.openapi as openapi


class TestOpenApiParsing (unittest.TestCase):
    def test_defaultOpenApiExample(self):
        modelFile = 'tests/resources/models/json/examples/openapi_v3_example_small.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(12, len(modelTypes))
        pathTypes = []
        for type in modelTypes:
            if isinstance(type, openapi.PathType):
                pathTypes.append(type)
        self.assertEqual(4, len(pathTypes))
