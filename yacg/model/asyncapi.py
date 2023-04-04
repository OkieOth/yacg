# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

from enum import Enum
import yacg.model.shared.info
import yacg.model.model


class OperationBase:
    def __init__(self, dictObj=None):

        #: unique identifier for this operation
        self.operationId = None

        #: some words to explain to topic
        self.summary = None

        #: some words to explain to topic
        self.description = None

        #: some words to explain to topic
        self.message = None

        #: amqp 0.9.1 related binding parameters
        self.amqpBindings = None

        #: covers the responded message in RPC style communication, custom extension
        self.xResponseMessage = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.operationId is not None:
            ret["operationId"] = self.operationId
        if self.summary is not None:
            ret["summary"] = self.summary
        if self.description is not None:
            ret["description"] = self.description
        if self.message is not None:
            ret["message"] = self.message.toDict()
        if self.amqpBindings is not None:
            ret["amqpBindings"] = self.amqpBindings.toDict()
        if self.xResponseMessage is not None:
            ret["xResponseMessage"] = self.xResponseMessage.toDict()
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "operationId":
            self.operationId = value
        if attribName == "summary":
            self.summary = value
        if attribName == "description":
            self.description = value
        self.message.initFlatValue(attribName, value)
        self.amqpBindings.initFlatValue(attribName, value)
        self.xResponseMessage.initFlatValue(attribName, value)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.operationId = dictObj.get('operationId', None)

        self.summary = dictObj.get('summary', None)

        self.description = dictObj.get('description', None)

        subDictObj = dictObj.get('message', None)
        if subDictObj is not None:
            self.message = Message(subDictObj)

        subDictObj = dictObj.get('amqpBindings', None)
        if subDictObj is not None:
            self.amqpBindings = OperationBindingsAmqp(subDictObj)

        subDictObj = dictObj.get('xResponseMessage', None)
        if subDictObj is not None:
            self.xResponseMessage = Message(subDictObj)


def createOperationBaseFromFlatDict(flatDict={}):
    ret = OperationBase()
    for key, value in flatDict.items():
        if key == "operationId":
            ret.operationId = value
        if key == "summary":
            ret.summary = value
        if key == "description":
            ret.description = value
        ret.message.initFlatValue(key, value)
        ret.amqpBindings.initFlatValue(key, value)
        ret.xResponseMessage.initFlatValue(key, value)
    return ret

class Message:
    """Container that describes the messages are sent
    """

    def __init__(self, dictObj=None):

        #: optional name, is used when defined in the components section
        self.name = None

        #: either a basic or a complex type
        self.payload = None

        #: additional message parameters
        self.amqpBindings = None

        #: mime type of the content, e.g. application/json
        self.contentType = None

        #: this is basically a complex type, whos top-level properties are used as keys for AMQP headers
        self.headers = None

        self.description = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.payload is not None:
            ret["payload"] = self.payload.toDict()
        if self.amqpBindings is not None:
            ret["amqpBindings"] = self.amqpBindings.toDict()
        if self.contentType is not None:
            ret["contentType"] = self.contentType
        if self.headers is not None:
            ret["headers"] = self.headers.toDict()
        if self.description is not None:
            ret["description"] = self.description
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        self.payload.initFlatValue(attribName, value)
        self.amqpBindings.initFlatValue(attribName, value)
        if attribName == "contentType":
            self.contentType = value
        self.headers.initFlatValue(attribName, value)
        if attribName == "description":
            self.description = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        subDictObj = dictObj.get('payload', None)
        if subDictObj is not None:
            self.payload = Payload(subDictObj)

        subDictObj = dictObj.get('amqpBindings', None)
        if subDictObj is not None:
            self.amqpBindings = MessageBindingsAmqp(subDictObj)

        self.contentType = dictObj.get('contentType', None)

        subDictObj = dictObj.get('headers', None)
        if subDictObj is not None:
            self.headers = AsyncApiHeaders(subDictObj)

        self.description = dictObj.get('description', None)


def createMessageFromFlatDict(flatDict={}):
    ret = Message()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        ret.payload.initFlatValue(key, value)
        ret.amqpBindings.initFlatValue(key, value)
        if key == "contentType":
            ret.contentType = value
        ret.headers.initFlatValue(key, value)
        if key == "description":
            ret.description = value
    return ret

class OperationBindingsAmqp:
    """specific AMQP binding properties
    """

    def __init__(self, dictObj=None):

        #: optional name, is used when defined in the components section
        self.name = None

        self.expiration = None

        self.mandatory = False

        self.replyTo = "amq.rabbitmq.reply-to"

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.expiration is not None:
            ret["expiration"] = self.expiration
        if self.mandatory is not None:
            ret["mandatory"] = self.mandatory
        if self.replyTo is not None:
            ret["replyTo"] = self.replyTo
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "expiration":
            self.expiration = value
        if attribName == "mandatory":
            self.mandatory = value
        if attribName == "replyTo":
            self.replyTo = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.expiration = dictObj.get('expiration', None)

        self.mandatory = dictObj.get('mandatory', False)

        self.replyTo = dictObj.get('replyTo', "amq.rabbitmq.reply-to")


def createOperationBindingsAmqpFromFlatDict(flatDict={}):
    ret = OperationBindingsAmqp()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "expiration":
            ret.expiration = value
        if key == "mandatory":
            ret.mandatory = value
        if key == "replyTo":
            ret.replyTo = value
    return ret

class AsyncApiInfo (yacg.model.shared.info.InfoSection):
    """Subset of the info object attribs: https://www.asyncapi.com/docs/specifications/v2.0.0#infoObject
    """

    def __init__(self, dictObj=None):
        yacg.model.shared.info.InfoSection.__init__(self)
        pass

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return



class AsyncApiServer:
    """one entry of the servers section
    """

    def __init__(self, dictObj=None):

        self.name = None

        self.url = None

        self.description = None

        self.protocol = None

        self.protocolVersion = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.url is not None:
            ret["url"] = self.url
        if self.description is not None:
            ret["description"] = self.description
        if self.protocol is not None:
            ret["protocol"] = self.protocol
        if self.protocolVersion is not None:
            ret["protocolVersion"] = self.protocolVersion
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "url":
            self.url = value
        if attribName == "description":
            self.description = value
        if attribName == "protocol":
            self.protocol = value
        if attribName == "protocolVersion":
            self.protocolVersion = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.url = dictObj.get('url', None)

        self.description = dictObj.get('description', None)

        self.protocol = dictObj.get('protocol', None)

        self.protocolVersion = dictObj.get('protocolVersion', None)


def createAsyncApiServerFromFlatDict(flatDict={}):
    ret = AsyncApiServer()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "url":
            ret.url = value
        if key == "description":
            ret.description = value
        if key == "protocol":
            ret.protocol = value
        if key == "protocolVersion":
            ret.protocolVersion = value
    return ret

class Channel:
    """one entry of the channels section
    """

    def __init__(self, dictObj=None):

        self.key = None

        self.description = None

        self.parameters = []

        self.publish = None

        self.subscribe = None

        self.amqpBindings = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.key is not None:
            ret["key"] = self.key
        if self.description is not None:
            ret["description"] = self.description
        if (self.parameters is not None) and (len(self.parameters) > 0):
            ret["parameters"] = self.parameters.toDict()
        if self.publish is not None:
            ret["publish"] = self.publish.toDict()
        if self.subscribe is not None:
            ret["subscribe"] = self.subscribe.toDict()
        if self.amqpBindings is not None:
            ret["amqpBindings"] = self.amqpBindings.toDict()
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "key":
            self.key = value
        if attribName == "description":
            self.description = value
        self.parameters.initFlatValue(attribName, value)
        self.publish.initFlatValue(attribName, value)
        self.subscribe.initFlatValue(attribName, value)
        self.amqpBindings.initFlatValue(attribName, value)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.key = dictObj.get('key', None)

        self.description = dictObj.get('description', None)

        arrayParameters = dictObj.get('parameters', [])
        for elemParameters in arrayParameters:
            self.parameters.append(
                Parameter(elemParameters))

        subDictObj = dictObj.get('publish', None)
        if subDictObj is not None:
            self.publish = OperationBase(subDictObj)

        subDictObj = dictObj.get('subscribe', None)
        if subDictObj is not None:
            self.subscribe = OperationBase(subDictObj)

        subDictObj = dictObj.get('amqpBindings', None)
        if subDictObj is not None:
            self.amqpBindings = ChannelBindingsAmqp(subDictObj)


def createChannelFromFlatDict(flatDict={}):
    ret = Channel()
    for key, value in flatDict.items():
        if key == "key":
            ret.key = value
        if key == "description":
            ret.description = value
        ret.parameters.initFlatValue(key, value)
        ret.publish.initFlatValue(key, value)
        ret.subscribe.initFlatValue(key, value)
        ret.amqpBindings.initFlatValue(key, value)
    return ret

class Parameter:
    """Parameters contained in the channel key
    """

    def __init__(self, dictObj=None):

        self.name = None

        self.description = None

        self.type = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.description is not None:
            ret["description"] = self.description
        if self.type is not None:
            ret["type"] = self.type
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "description":
            self.description = value
        if attribName == "type":
            self.type = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        self.type = dictObj.get('type', None)


def createParameterFromFlatDict(flatDict={}):
    ret = Parameter()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "description":
            ret.description = value
        if key == "type":
            ret.type = value
    return ret

class ChannelBindingsAmqp:
    """https://github.com/asyncapi/bindings/blob/master/amqp/README.md#channel
    """

    def __init__(self, dictObj=None):

        #: optional name, is used when defined in the components section
        self.name = None

        self.isType = ChannelBindingsAmqpIsTypeEnum.ROUTINGKEY

        self.queue = None

        self.exchange = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.isType is not None:
            ret["isType"] = ChannelBindingsAmqpIsTypeEnum.valueAsString(self.isType)
        if self.queue is not None:
            ret["queue"] = self.queue.toDict()
        if self.exchange is not None:
            ret["exchange"] = self.exchange.toDict()
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "isType":
            self.isType = ChannelBindingsAmqpIsTypeEnum.valueForString(value)
        self.queue.initFlatValue(attribName, value)
        self.exchange.initFlatValue(attribName, value)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.isType = ChannelBindingsAmqpIsTypeEnum.valueForString(dictObj.get('isType', None))

        subDictObj = dictObj.get('queue', None)
        if subDictObj is not None:
            self.queue = ChannelBindingsAmqpQueue(subDictObj)

        subDictObj = dictObj.get('exchange', None)
        if subDictObj is not None:
            self.exchange = ChannelBindingsAmqpExchange(subDictObj)


def createChannelBindingsAmqpFromFlatDict(flatDict={}):
    ret = ChannelBindingsAmqp()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "isType":
            ret.isType = ChannelBindingsAmqpIsTypeEnum.valueForString(value)
        ret.queue.initFlatValue(key, value)
        ret.exchange.initFlatValue(key, value)
    return ret

class ChannelBindingsAmqpExchange:
    """channel exchange parameters
    """

    def __init__(self, dictObj=None):

        self.name = None

        self.type = None

        self.durable = False

        self.autoDelete = False

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.type is not None:
            ret["type"] = ChannelBindingsAmqpExchangeTypeEnum.valueAsString(self.type)
        if self.durable is not None:
            ret["durable"] = self.durable
        if self.autoDelete is not None:
            ret["autoDelete"] = self.autoDelete
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "type":
            self.type = ChannelBindingsAmqpExchangeTypeEnum.valueForString(value)
        if attribName == "durable":
            self.durable = value
        if attribName == "autoDelete":
            self.autoDelete = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.type = ChannelBindingsAmqpExchangeTypeEnum.valueForString(dictObj.get('type', None))

        self.durable = dictObj.get('durable', False)

        self.autoDelete = dictObj.get('autoDelete', False)


def createChannelBindingsAmqpExchangeFromFlatDict(flatDict={}):
    ret = ChannelBindingsAmqpExchange()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "type":
            ret.type = ChannelBindingsAmqpExchangeTypeEnum.valueForString(value)
        if key == "durable":
            ret.durable = value
        if key == "autoDelete":
            ret.autoDelete = value
    return ret

class ChannelBindingsAmqpExchangeTypeEnum(Enum):
    TOPIC = 'topic'
    DIRECT = 'direct'
    FANOUT = 'fanout'
    DEFAULT = 'default'
    HEADERS = 'headers'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'topic':
            return ChannelBindingsAmqpExchangeTypeEnum.TOPIC
        elif lowerStringValue == 'direct':
            return ChannelBindingsAmqpExchangeTypeEnum.DIRECT
        elif lowerStringValue == 'fanout':
            return ChannelBindingsAmqpExchangeTypeEnum.FANOUT
        elif lowerStringValue == 'default':
            return ChannelBindingsAmqpExchangeTypeEnum.DEFAULT
        elif lowerStringValue == 'headers':
            return ChannelBindingsAmqpExchangeTypeEnum.HEADERS
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == ChannelBindingsAmqpExchangeTypeEnum.TOPIC:
            return 'topic'
        elif enumValue == ChannelBindingsAmqpExchangeTypeEnum.DIRECT:
            return 'direct'
        elif enumValue == ChannelBindingsAmqpExchangeTypeEnum.FANOUT:
            return 'fanout'
        elif enumValue == ChannelBindingsAmqpExchangeTypeEnum.DEFAULT:
            return 'default'
        elif enumValue == ChannelBindingsAmqpExchangeTypeEnum.HEADERS:
            return 'headers'
        else:
            return ''




class ChannelBindingsAmqpQueue:
    """channel queue parameters
    """

    def __init__(self, dictObj=None):

        self.name = None

        self.durable = False

        self.exclusive = False

        self.autoDelete = False

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.durable is not None:
            ret["durable"] = self.durable
        if self.exclusive is not None:
            ret["exclusive"] = self.exclusive
        if self.autoDelete is not None:
            ret["autoDelete"] = self.autoDelete
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "durable":
            self.durable = value
        if attribName == "exclusive":
            self.exclusive = value
        if attribName == "autoDelete":
            self.autoDelete = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.durable = dictObj.get('durable', False)

        self.exclusive = dictObj.get('exclusive', False)

        self.autoDelete = dictObj.get('autoDelete', False)


def createChannelBindingsAmqpQueueFromFlatDict(flatDict={}):
    ret = ChannelBindingsAmqpQueue()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "durable":
            ret.durable = value
        if key == "exclusive":
            ret.exclusive = value
        if key == "autoDelete":
            ret.autoDelete = value
    return ret

class ChannelBindingsAmqpIsTypeEnum(Enum):
    QUEUE = 'queue'
    ROUTINGKEY = 'routingKey'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'queue':
            return ChannelBindingsAmqpIsTypeEnum.QUEUE
        elif lowerStringValue == 'routingkey':
            return ChannelBindingsAmqpIsTypeEnum.ROUTINGKEY
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == ChannelBindingsAmqpIsTypeEnum.QUEUE:
            return 'queue'
        elif enumValue == ChannelBindingsAmqpIsTypeEnum.ROUTINGKEY:
            return 'routingKey'
        else:
            return ''




class Payload:
    def __init__(self, dictObj=None):

        #: meta model type that is passed in the body
        self.type = None

        self.isArray = False

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.type is not None:
            ret["type"] = self.type.toDict()
        if self.isArray is not None:
            ret["isArray"] = self.isArray
        return ret

    def initFlatValue(self, attribName, value):
        self.type.initFlatValue(attribName, value)
        if attribName == "isArray":
            self.isArray = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        subDictObj = dictObj.get('type', None)
        if subDictObj is not None:
            self.type = yacg.model.model.Type(subDictObj)

        self.isArray = dictObj.get('isArray', False)


def createPayloadFromFlatDict(flatDict={}):
    ret = Payload()
    for key, value in flatDict.items():
        ret.type.initFlatValue(key, value)
        if key == "isArray":
            ret.isArray = value
    return ret

class MessageBindingsAmqp:
    """https://github.com/asyncapi/bindings/blob/master/amqp/README.md#message-binding-object
    """

    def __init__(self, dictObj=None):

        #: optional name, is used when defined in the components section
        self.name = None

        #: A MIME encoding for the message content.
        self.contentEncoding = None

        #: Application defined text
        self.messageType = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.contentEncoding is not None:
            ret["contentEncoding"] = self.contentEncoding
        if self.messageType is not None:
            ret["messageType"] = self.messageType
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "name":
            self.name = value
        if attribName == "contentEncoding":
            self.contentEncoding = value
        if attribName == "messageType":
            self.messageType = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.contentEncoding = dictObj.get('contentEncoding', None)

        self.messageType = dictObj.get('messageType', None)


def createMessageBindingsAmqpFromFlatDict(flatDict={}):
    ret = MessageBindingsAmqp()
    for key, value in flatDict.items():
        if key == "name":
            ret.name = value
        if key == "contentEncoding":
            ret.contentEncoding = value
        if key == "messageType":
            ret.messageType = value
    return ret

class AsyncApiHeaders (yacg.model.model.ComplexType):
    def __init__(self, dictObj=None):
        yacg.model.model.ComplexType.__init__(self)
        pass

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return



