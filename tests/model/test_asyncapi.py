# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

import yacg.model.asyncapi
import yacg.model.shared.info
import yacg.model.model


class TestYacgAsyncapiModel (unittest.TestCase):
    def testOperationBase(self):
        x = yacg.model.asyncapi.OperationBase()
        self.assertIsNotNone(x)

    def testMessage(self):
        x = yacg.model.asyncapi.Message()
        self.assertIsNotNone(x)

    def testOperationBindingsAmqp(self):
        x = yacg.model.asyncapi.OperationBindingsAmqp()
        self.assertIsNotNone(x)

    def testAsyncApiInfo(self):
        x = yacg.model.asyncapi.AsyncApiInfo()
        self.assertIsNotNone(x)

    def testAsyncApiServer(self):
        x = yacg.model.asyncapi.AsyncApiServer()
        self.assertIsNotNone(x)

    def testChannel(self):
        x = yacg.model.asyncapi.Channel()
        self.assertIsNotNone(x)

    def testParameter(self):
        x = yacg.model.asyncapi.Parameter()
        self.assertIsNotNone(x)

    def testChannelBindingsAmqp(self):
        x = yacg.model.asyncapi.ChannelBindingsAmqp()
        self.assertIsNotNone(x)

    def testChannelBindingsAmqpExchange(self):
        x = yacg.model.asyncapi.ChannelBindingsAmqpExchange()
        self.assertIsNotNone(x)

    def testChannelBindingsAmqpExchangeTypeEnum(self):
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpExchangeTypeEnum.TOPIC)
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpExchangeTypeEnum.DIRECT)
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpExchangeTypeEnum.FANOUT)
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpExchangeTypeEnum.DEFAULT)
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpExchangeTypeEnum.HEADERS)

    def testChannelBindingsAmqpQueue(self):
        x = yacg.model.asyncapi.ChannelBindingsAmqpQueue()
        self.assertIsNotNone(x)

    def testChannelBindingsAmqpIsTypeEnum(self):
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpIsTypeEnum.QUEUE)
        self.assertIsNotNone(yacg.model.asyncapi.ChannelBindingsAmqpIsTypeEnum.ROUTINGKEY)

    def testPayload(self):
        x = yacg.model.asyncapi.Payload()
        self.assertIsNotNone(x)

    def testMessageBindingsAmqp(self):
        x = yacg.model.asyncapi.MessageBindingsAmqp()
        self.assertIsNotNone(x)

    def testAsyncApiHeaders(self):
        x = yacg.model.asyncapi.AsyncApiHeaders()
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
