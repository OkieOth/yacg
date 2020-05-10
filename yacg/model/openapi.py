# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum

import yacg.model.model as model


class PathType (model.ComplexType):
    """ base type that contains all REST path information
    """

    def __init__(self):
        super(model.ComplexType, self).__init__()

        #: base type that contains all REST path information
        self.pathPattern = None

        #: base type that contains all REST path information
        self.commands = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = PathType()

        obj.pathPattern = dict.get('pathPattern', None)

        arrayCommands = dict.get('commands', [])
        for elemCommands in arrayCommands:
            obj.commands.append(
                Command.dictToObject(elemCommands))
        return obj


class Command:
    """ information to a specific HTTP command
    """

    def __init__(self):

        #: information to a specific HTTP command
        self.command = None

        #: information to a specific HTTP command
        self.tags = []

        #: information to a specific HTTP command
        self.summary = None

        #: information to a specific HTTP command
        self.description = None

        #: information to a specific HTTP command
        self.operationId = None

        #: information to a specific HTTP command
        self.consumes = []

        #: information to a specific HTTP command
        self.produces = []

        #: information to a specific HTTP command
        self.parameters = []

        #: information to a specific HTTP command
        self.requestBody = None

        #: information to a specific HTTP command
        self.responses = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Command()

        obj.command = CommandCommandEnum.valueForString(dict.get('command', None))

        arrayTags = dict.get('tags', [])
        for elemTags in arrayTags:
            obj.tags.append(elemTags)

        obj.summary = dict.get('summary', None)

        obj.description = dict.get('description', None)

        obj.operationId = dict.get('operationId', None)

        arrayConsumes = dict.get('consumes', [])
        for elemConsumes in arrayConsumes:
            obj.consumes.append(
                CommandConsumesEnum.valueForString(elemConsumes))

        arrayProduces = dict.get('produces', [])
        for elemProduces in arrayProduces:
            obj.produces.append(
                CommandProducesEnum.valueForString(elemProduces))

        arrayParameters = dict.get('parameters', [])
        for elemParameters in arrayParameters:
            obj.parameters.append(
                Parameter.dictToObject(elemParameters))

        obj.requestBody = RequestBody.dictToObject(dict.get('requestBody', None))

        arrayResponses = dict.get('responses', [])
        for elemResponses in arrayResponses:
            obj.responses.append(
                Response.dictToObject(elemResponses))
        return obj


class CommandCommandEnum(Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        elif stringValue == 'GET':
            return CommandCommandEnum.GET
        elif stringValue == 'PUT':
            return CommandCommandEnum.PUT
        elif stringValue == 'POST':
            return CommandCommandEnum.POST
        elif stringValue == 'DELETE':
            return CommandCommandEnum.DELETE
        elif stringValue == 'OPTIONS':
            return CommandCommandEnum.OPTIONS
        else:
            return None


class CommandConsumesEnum(Enum):
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        elif stringValue == 'application/json':
            return CommandConsumesEnum.APPLICATION_JSON
        elif stringValue == 'application/xml':
            return CommandConsumesEnum.APPLICATION_XML
        else:
            return None


class CommandProducesEnum(Enum):
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        elif stringValue == 'application/json':
            return CommandProducesEnum.APPLICATION_JSON
        elif stringValue == 'application/xml':
            return CommandProducesEnum.APPLICATION_XML
        else:
            return None


class Parameter:
    """ definition of a parameter that is used in the request
    """

    def __init__(self):

        #: definition of a parameter that is used in the request
        self.inType = None

        #: definition of a parameter that is used in the request
        self.name = None

        #: definition of a parameter that is used in the request
        self.description = None

        #: definition of a parameter that is used in the request
        self.required = None

        #: definition of a parameter that is used in the request
        self.type = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Parameter()

        obj.inType = ParameterInTypeEnum.valueForString(dict.get('inType', None))

        obj.name = dict.get('name', None)

        obj.description = dict.get('description', None)

        obj.required = dict.get('required', None)

        obj.type = Type.dictToObject(dict.get('type', None))
        return obj


class RequestBody:
    """ definition of a parameter that is used in the request
    """

    def __init__(self):

        #: definition of a parameter that is used in the request
        self.description = None

        #: definition of a parameter that is used in the request
        self.required = None

        #: definition of a parameter that is used in the request
        self.content = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = RequestBody()

        obj.description = dict.get('description', None)

        obj.required = dict.get('required', None)

        arrayContent = dict.get('content', [])
        for elemContent in arrayContent:
            obj.content.append(
                RequestBodyContent.dictToObject(elemContent))
        return obj


class Response:
    """ description of a response option for a request
    """

    def __init__(self):

        #: description of a response option for a request
        self.returnCode = None

        #: description of a response option for a request
        self.description = None

        #: description of a response option for a request
        self.type = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Response()

        obj.returnCode = dict.get('returnCode', None)

        obj.description = dict.get('description', None)

        obj.type = Type.dictToObject(dict.get('type', None))
        return obj


class RequestBodyContent:
    def __init__(self):

        self.mimeType = None

        self.type = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = RequestBodyContent()

        obj.mimeType = dict.get('mimeType', None)

        obj.type = Type.dictToObject(dict.get('type', None))
        return obj


class ParameterInTypeEnum(Enum):
    PATH = 'path'
    QUERY = 'query'
    HEADER = 'header'
    COOKIE = 'cookie'

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        elif stringValue == 'path':
            return ParameterInTypeEnum.PATH
        elif stringValue == 'query':
            return ParameterInTypeEnum.QUERY
        elif stringValue == 'header':
            return ParameterInTypeEnum.HEADER
        elif stringValue == 'cookie':
            return ParameterInTypeEnum.COOKIE
        else:
            return None


