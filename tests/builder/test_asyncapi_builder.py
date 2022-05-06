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

    def checkChannelBinding(
            self,
            channelBinding,
            name,
            isType,
            exchangeName,
            exchangeType,
            exchangeDurable,
            exchangeAutoDelete,
            queueName,
            queueDurable,
            queueExclusive,
            queueAutoDelete):
        self.assertEqual(channelBinding.name, name)
        self.assertEqual(channelBinding.isType, isType)
        if exchangeName is None:
            self.assertIsNone(channelBinding.exchange)
        else:
            self.assertEqual(channelBinding.exchange.name, exchangeName)
            self.assertEqual(channelBinding.exchange.type, exchangeType)
            self.assertEqual(channelBinding.exchange.durable, exchangeDurable)
            self.assertEqual(channelBinding.exchange.autoDelete, exchangeAutoDelete)
        if queueName is None:
            self.assertIsNone(channelBinding.queue)
        else:
            self.assertEqual(channelBinding.queue.name, queueName)
            self.assertEqual(channelBinding.queue.autoDelete, queueAutoDelete)
            self.assertEqual(channelBinding.queue.durable, queueDurable)
            self.assertEqual(channelBinding.queue.exclusive, queueExclusive)

    def checkChannelBindings(self, channelBindings):
        self.assertEqual(len(channelBindings), 3)  # 4 are given in the test file, but one isn't amqp
        self.checkChannelBinding(
            channelBindings[0],
            'myChannelBinding1',
            asyncapi.ChannelBindingsAmqpIsTypeEnum.ROUTINGKEY,
            'xxx',
            asyncapi.ChannelBindingsAmqpExchangeTypeEnum.TOPIC,
            True,
            False,
            'myQueue-xxx',
            True,
            True,
            True)
        self.checkChannelBinding(
            channelBindings[1],
            'myChannelBinding2',
            asyncapi.ChannelBindingsAmqpIsTypeEnum.QUEUE,
            None,
            None,
            None,
            None,
            'myQueue-1',
            False,
            False,
            False)
        self.checkChannelBinding(
            channelBindings[2],
            'myChannelBinding4',
            asyncapi.ChannelBindingsAmqpIsTypeEnum.ROUTINGKEY,
            'xxy',
            asyncapi.ChannelBindingsAmqpExchangeTypeEnum.FANOUT,
            True,
            True,
            None,
            None,
            None,
            None)

    def checkMessageBindings(self, messageBindings):
        self.assertEqual(len(messageBindings), 1)

    def checkOperationBindings(self, operationBindings):
        self.assertEqual(len(operationBindings), 2)

    def checkParameters(self, parameters):
        self.assertEqual(len(parameters), 7)

    def test_asyncApiExample(self):
        modelFile = 'tests/resources/models/json/examples/asyncapi_test.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        parsedSchema = dictionaryBuilder.getParsedSchemaFromJson(modelFile)
        modelTypes = dictionaryBuilder.extractTypes(parsedSchema, modelFile, [])
        self.assertTrue(len(modelTypes)>0)
        serverTypes = []
        infoTypes = []
        channelBindings = []
        operationBindings = []
        messageBindings = []
        parameters = []
        for type in modelTypes:
            if isinstance(type, asyncapi.AsyncApiServer):
                serverTypes.append(type)
            if isinstance(type, asyncapi.AsyncApiInfo):
                infoTypes.append(type)
            if isinstance(type, asyncapi.ChannelBindingsAmqp):
                channelBindings.append(type)
            if isinstance(type, asyncapi.MessageBindingsAmqp):
                messageBindings.append(type)
            if isinstance(type, asyncapi.OperationBindingsAmqp):
                operationBindings.append(type)
            if isinstance(type, asyncapi.Parameter):
                parameters.append(type)
        self.assertEqual(len(serverTypes), 2)
        self.checkServerTypes(serverTypes)
        self.assertEqual(len(infoTypes), 1)
        self.checkInfoType(infoTypes[0])
        self.checkChannelBindings(channelBindings)
        self.checkMessageBindings(messageBindings)
        self.checkOperationBindings(operationBindings)


