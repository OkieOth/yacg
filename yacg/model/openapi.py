# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum
import yacg.model.model


class PathType (yacg.model.model.Type):
    """ base type that contains all REST path information
    """

    def __init__(self, dictObj = None):
        super(yacg.model.model.Type, self).__init__()
        if dictObj is None:

            #: base type that contains all REST path information
            self.pathPattern = None

            #: base type that contains all REST path information
            self.commands = []
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.pathPattern = dictObj.get('pathPattern', None)

        arrayCommands = dictObj.get('commands', [])
        for elemCommands in arrayCommands:
            self.commands.append(
                Command(elemCommands))


class Command:
    """ information to a specific HTTP command
    """

    def __init__(self, dictObj = None):
        if dictObj is None:

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
            self.parameters = []

            #: information to a specific HTTP command
            self.requestBody = None

            #: information to a specific HTTP command
            self.responses = []

            #: information to a specific HTTP command
            self.security = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.command = CommandCommandEnum.valueForString(dictObj.get('command', None))

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(elemTags)

        self.summary = dictObj.get('summary', None)

        self.description = dictObj.get('description', None)

        self.operationId = dictObj.get('operationId', None)

        arrayParameters = dictObj.get('parameters', [])
        for elemParameters in arrayParameters:
            self.parameters.append(
                Parameter(elemParameters))

        self.requestBody = RequestBody(dict.get('requestBody', None))

        arrayResponses = dictObj.get('responses', [])
        for elemResponses in arrayResponses:
            self.responses.append(
                Response(elemResponses))

        self.security = CommandSecurity(dict.get('security', None))


class CommandCommandEnum(Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'get':
            return CommandCommandEnum.GET
        elif lowerStringValue == 'put':
            return CommandCommandEnum.PUT
        elif lowerStringValue == 'post':
            return CommandCommandEnum.POST
        elif lowerStringValue == 'delete':
            return CommandCommandEnum.DELETE
        elif lowerStringValue == 'options':
            return CommandCommandEnum.OPTIONS
        elif lowerStringValue == 'patch':
            return CommandCommandEnum.PATCH
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == CommandCommandEnum.GET:
            return 'GET'
        elif enumValue == CommandCommandEnum.PUT:
            return 'PUT'
        elif enumValue == CommandCommandEnum.POST:
            return 'POST'
        elif enumValue == CommandCommandEnum.DELETE:
            return 'DELETE'
        elif enumValue == CommandCommandEnum.OPTIONS:
            return 'OPTIONS'
        elif enumValue == CommandCommandEnum.PATCH:
            return 'PATCH'
        else:
            return ''



class Parameter:
    """ definition of a parameter that is used in the request
    """

    def __init__(self, dictObj = None):
        if dictObj is None:

            #: definition of a parameter that is used in the request
            self.inType = None

            #: definition of a parameter that is used in the request
            self.name = None

            #: definition of a parameter that is used in the request
            self.isArray = None

            #: definition of a parameter that is used in the request
            self.description = None

            #: definition of a parameter that is used in the request
            self.required = None

            #: definition of a parameter that is used in the request
            self.type = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.inType = ParameterInTypeEnum.valueForString(dictObj.get('inType', None))

        self.name = dictObj.get('name', None)

        self.isArray = dictObj.get('isArray', None)

        self.description = dictObj.get('description', None)

        self.required = dictObj.get('required', None)

        self.type = yacg.model.model.Type(dict.get('type', None))


class RequestBody:
    """ definition of a parameter that is used in the request
    """

    def __init__(self, dictObj = None):
        if dictObj is None:

            #: definition of a parameter that is used in the request
            self.description = None

            #: definition of a parameter that is used in the request
            self.required = None

            #: definition of a parameter that is used in the request
            self.content = []
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.description = dictObj.get('description', None)

        self.required = dictObj.get('required', None)

        arrayContent = dictObj.get('content', [])
        for elemContent in arrayContent:
            self.content.append(
                ContentEntry(elemContent))


class Response:
    """ description of a response option for a request
    """

    def __init__(self, dictObj = None):
        if dictObj is None:

            #: description of a response option for a request
            self.returnCode = None

            #: description of a response option for a request
            self.description = None

            #: description of a response option for a request
            self.content = []
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.returnCode = dictObj.get('returnCode', None)

        self.description = dictObj.get('description', None)

        arrayContent = dictObj.get('content', [])
        for elemContent in arrayContent:
            self.content.append(
                ContentEntry(elemContent))


class CommandSecurity:
    def __init__(self, dictObj = None):
        if dictObj is None:

            self.scopes = []
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        arrayScopes = dictObj.get('scopes', [])
        for elemScopes in arrayScopes:
            self.scopes.append(elemScopes)


class ContentEntry:
    def __init__(self, dictObj = None):
        if dictObj is None:

            self.mimeType = None

            self.type = None

            self.isArray = False
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.mimeType = dictObj.get('mimeType', None)

        self.type = yacg.model.model.Type(dict.get('type', None))

        self.isArray = dictObj.get('isArray', False)


class ParameterInTypeEnum(Enum):
    PATH = 'path'
    QUERY = 'query'
    HEADER = 'header'
    COOKIE = 'cookie'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'path':
            return ParameterInTypeEnum.PATH
        elif lowerStringValue == 'query':
            return ParameterInTypeEnum.QUERY
        elif lowerStringValue == 'header':
            return ParameterInTypeEnum.HEADER
        elif lowerStringValue == 'cookie':
            return ParameterInTypeEnum.COOKIE
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == ParameterInTypeEnum.PATH:
            return 'path'
        elif enumValue == ParameterInTypeEnum.QUERY:
            return 'query'
        elif enumValue == ParameterInTypeEnum.HEADER:
            return 'header'
        elif enumValue == ParameterInTypeEnum.COOKIE:
            return 'cookie'
        else:
            return ''



