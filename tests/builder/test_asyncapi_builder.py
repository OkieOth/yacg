import unittest
import os

import yacg.builder.impl.dictionaryBuilder as dictionaryBuilder
import yacg.model.openapi as openapi
import yacg.model.asyncapi as asyncapi
import yacg.model.model as model


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
        self.assertEqual(len(channelBindings), 4)  # 5 are given in the test file, but one isn't amqp
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
        self.assertEqual(len(messageBindings), 2)
        self.assertEqual(messageBindings[0].messageType, 'typenamestring')
        self.assertEqual(messageBindings[0].name, 'msgBinding1')
        self.assertEqual(messageBindings[0].contentEncoding, 'UTF-8')

    def checkOperationBinding(self, operationBinding, name, mandatory, expiration, replyTo):
        self.assertEqual(operationBinding.name, name)
        self.assertEqual(operationBinding.mandatory, mandatory)
        self.assertEqual(operationBinding.expiration, expiration)
        self.assertEqual(operationBinding.replyTo, replyTo)

    def checkOperationBindings(self, operationBindings):
        self.assertEqual(len(operationBindings), 6)
        self.checkOperationBinding(operationBindings[0], 'opBinding1', False, 10, 'test-reply-to')
        self.checkOperationBinding(operationBindings[1], 'opBinding2', True, None, 'amq.rabbitmq.reply-to')

    def checkParameter(self, parameter, name, description, type):
        self.assertEqual(parameter.name, name)
        self.assertEqual(parameter.description, description)
        self.assertTrue(isinstance(parameter.type, type))

    def checkParameters(self, parameters):
        self.assertEqual(len(parameters), 8)
        self.checkParameter(parameters[0], 'myParam1', 'I am a dummy parameter', model.UuidType)
        self.checkParameter(parameters[1], 'myParam2', 'I am a dummy complex parameter', model.ComplexType)
        self.checkParameter(parameters[2], 'param1', 'a param', model.UuidType)
        self.checkParameter(parameters[3], 'param2', 'another param', model.UuidType)
        self.checkParameter(parameters[4], 'param3', 'another param', model.NumberType)
        self.checkParameter(parameters[5], 'param1', 'a param', model.UuidType)
        self.checkParameter(parameters[6], 'param2', 'another param', model.UuidType)
        self.checkParameter(parameters[7], 'param3', 'yet another param', model.UuidType)

    def checkChannelObj(self, channels, key, channelBindings, parameterCount, publish):
        found = []
        for c in channels:
            if c.key == key:
                found.append(c)
        self.assertEqual(1, len(found))
        channelToCheck = found[0]
        self.assertEqual(parameterCount, len(channelToCheck.parameters))
        self.assertIsNotNone(channelToCheck.amqpBindings)
        if publish:
            self.assertIsNotNone(channelToCheck.publish)
            self.assertIsNotNone(channelToCheck.publish.amqpBindings)
        if channelBindings is not None:
            self.assertIsNotNone(channelToCheck.amqpBindings)
            bindingsToCheck = channelToCheck.amqpBindings
            self.assertEqual(channelBindings.isType, bindingsToCheck.isType)
            if channelBindings.exchange is not None:
                self.assertIsNotNone(bindingsToCheck.exchange)
                self.assertEqual(channelBindings.exchange.name, bindingsToCheck.exchange.name)
                self.assertEqual(channelBindings.exchange.type, bindingsToCheck.exchange.type)
                self.assertEqual(channelBindings.exchange.durable, bindingsToCheck.exchange.durable)
                self.assertEqual(channelBindings.exchange.autoDelete, bindingsToCheck.exchange.autoDelete)
            if channelBindings.queue is not None:
                self.assertIsNotNone(bindingsToCheck.queue)
                self.assertEqual(channelBindings.queue.name, bindingsToCheck.queue.name)
                self.assertEqual(channelBindings.queue.durable, bindingsToCheck.queue.durable)
                self.assertEqual(channelBindings.queue.exclusive, bindingsToCheck.queue.exclusive)
                self.assertEqual(channelBindings.queue.autoDelete, bindingsToCheck.queue.autoDelete)

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
        channels = []
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
            if isinstance(type, asyncapi.Channel):
                channels.append(type)
        self.assertEqual(len(serverTypes), 2)
        self.assertEqual(len(channels), 5)
        self.checkServerTypes(serverTypes)
        self.assertEqual(len(infoTypes), 1)
        self.checkInfoType(infoTypes[0])
        self.checkChannelBindings(channelBindings)
        self.checkMessageBindings(messageBindings)
        self.checkOperationBindings(operationBindings)
        self.checkParameters(parameters)
        channelBindings = asyncapi.ChannelBindingsAmqp()
        channelBindings.exchange = asyncapi.ChannelBindingsAmqpExchange()
        channelBindings.exchange.name = "myExchange"
        channelBindings.exchange.type = asyncapi.ChannelBindingsAmqpExchangeTypeEnum.TOPIC
        channelBindings.exchange.durable = True
        channelBindings.exchange.autoDelete = False
        channelBindings.queue = asyncapi.ChannelBindingsAmqpQueue()
        channelBindings.queue.name = "my-queue-name"
        channelBindings.queue.durable = True
        channelBindings.queue.exclusive = True
        channelBindings.queue.autoDelete = False
        self.checkChannelObj(channels, "xxy.{param1}.yyx.{param2}", channelBindings, 3, True)
        channelBindings = asyncapi.ChannelBindingsAmqp()
        channelBindings.exchange = asyncapi.ChannelBindingsAmqpExchange()
        channelBindings.exchange.name = "xxy"
        channelBindings.exchange.type = asyncapi.ChannelBindingsAmqpExchangeTypeEnum.FANOUT
        channelBindings.exchange.durable = True
        channelBindings.exchange.autoDelete = True
        self.checkChannelObj(channels, "xxz.{param1}.yyx.{param2}", channelBindings, 2, True)


