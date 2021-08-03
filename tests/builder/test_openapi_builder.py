import unittest
import os

import yacg.builder.impl.dictionaryBuilder as dictionaryBuilder
import yacg.model.openapi as openapi
import yacg.model.modelFuncs as modelFuncs


class TestOpenApiParsing (unittest.TestCase):

    def test_openApiExample(self):
        modelFile = 'tests/resources/models/json/examples/openapi_v3_example_small.json'
        self.__doTest(modelFile, False)

    def test_swaggerExample(self):
        modelFile = 'tests/resources/models/json/examples/swagger_v2_example_small.json'
        self.__doTest(modelFile, True, True)

    def test_separateOpenApiPathTypes(self):
        modelFile = 'tests/resources/models/json/examples/openapi_v3_example_small.json'
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(15, len(modelTypes))
        (pathTypes, otherTypes, enumTypes) = modelFuncs.separateOpenApiPathTypes(modelTypes)
        self.assertEqual(4, len(pathTypes))
        self.assertEqual(6, len(otherTypes))
        self.assertEqual(5, len(enumTypes))

    def test_getOpenApiTags(self):
        modelFile = 'tests/resources/models/json/examples/openapi_v3_example_small.json'
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(15, len(modelTypes))
        tags = modelFuncs.getOpenApiTags(modelTypes)
        self.assertEqual(1, len(tags))

    def __doTest(self, modelFile, skipScopeTest, requestBodyMimeTypeCanBeNone=False):
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(15, len(modelTypes))
        pathTypes = []
        coreModelTypes = []
        foundScopedCommand = False
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
                self.assertIsNotNone(command.command)
                self.assertTrue(len(command.tags) > 0)
                self.assertTrue(
                    (len(command.parameters) > 0) or
                    (command.requestBody is not None))
                for param in command.parameters:
                    self.assertIsNotNone(param.name)
                    self.assertIsNotNone(param.type)
                if command.requestBody is not None:
                    self._checkContent(command.requestBody, requestBodyMimeTypeCanBeNone)
                self.assertTrue(len(command.responses) > 0)
                for response in command.responses:
                    self.assertIsNotNone(response.returnCode)
                    if response.returnCode == '200':
                        self._checkContent(response, requestBodyMimeTypeCanBeNone)
                if skipScopeTest:
                    continue
                if (path.pathPattern == '/pet/{petId}') and (command.command == openapi.CommandCommandEnum.GET):
                    foundScopedCommand = True
                    self.assertEqual(2, len(command.security.scopes))
                    self.assertEqual('scope1', command.security.scopes[0])
                    self.assertEqual('scope2', command.security.scopes[1])
        if not skipScopeTest:
            self.assertTrue(foundScopedCommand)

    def _checkContent(self, contentHost, requestBodyMimeTypeCanBeNone):
        self.assertTrue(len(contentHost.content) > 0)
        for cont in contentHost.content:
            if not requestBodyMimeTypeCanBeNone:
                self.assertIsNotNone(cont.mimeType)
            self.assertIsNotNone(cont.type)
