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
        self.assertEqual(15, len(modelTypes))
        pathTypes = []
        coreModelTypes = []
        for type in modelTypes:
            if isinstance(type, openapi.PathType):
                pathTypes.append(type)
            else:
                coreModelTypes.append(type)
        self.assertEqual(4, len(pathTypes))
        for path in pathTypes:
            self.assertTrue(len(path.commands) > 0)
            self.assertIsNotNone(path.pathPattern)
            for command in path.commands:
                self.assertTrue(len(command.tags) > 0)
                self.assertTrue(
                    (len(command.parameters) > 0) or
                    (command.requestBody is not None))
                for param in command.parameters:
                    self.assertIsNotNone(param.name)
                    self.assertIsNotNone(param.type)
                if command.requestBody is not None:
                    self.assertTrue(len(command.requestBody.content) > 0)
                    for cont in command.requestBody.content:
                        self.assertIsNotNone(cont.mimeType)
                        self.assertIsNotNone(cont.type)

                self.assertTrue(len(command.responses) > 0)

