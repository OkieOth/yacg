import unittest
import os

import yacg.builder.impl.dictionaryBuilder as dictionaryBuilder
import yacg.model.openapi as openapi
import yacg.model.asyncapi as asyncapi


class TestAsyncApiParsing (unittest.TestCase):
    def checkServerTypes(self, serverTypes):
        self.assertEqual(serverTypes[0].name, 'dev')
        self.assertEqual(serverTypes[0].url, 'broker.dev:5672')
        self.assertEqual(serverTypes[0].description, 'Development server')
        self.assertEqual(serverTypes[0].protocol, 'amqp')
        self.assertEqual(serverTypes[0].protocolVersion, '0.9.1')
        self.assertEqual(serverTypes[1].name, 'test')
        self.assertEqual(serverTypes[1].url, 'broker.test:5672')
        self.assertEqual(serverTypes[1].description, 'Test server')
        self.assertEqual(serverTypes[1].protocol, 'amqp')
        self.assertEqual(serverTypes[1].protocolVersion, '0.9.1')

    def checkInfoType(self, infoType):
        self.assertEqual(infoType.title, 'AsyncAPI Test')
        self.assertEqual(infoType.description, 'The file is an example')
        self.assertEqual(infoType.version, '1.0.0')

    def test_asyncApiExample(self):
        modelFile = 'tests/resources/models/json/examples/asyncapi_test.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertTrue(len(modelTypes)>0)
        serverTypes = []
        for type in modelTypes:
            if isinstance(type, asyncapi.AsyncApiServer):
                serverTypes.append(type)
        self.assertEqual(len(serverTypes), 2)
        self.checkServerTypes(serverTypes)
        infoTypes = []
        for type in modelTypes:
            if isinstance(type, asyncapi.AsyncApiInfo):
                infoTypes.append(type)
        self.assertEqual(len(infoTypes), 1)
        self.checkInfoType(infoTypes[0])


