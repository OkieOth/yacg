# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum
import yacg.model.model


class PathType (yacg.model.model.Type):
    """ base type that contains all REST path information
    """

    def __init__(self):
        super(yacg.model.model.Type, self).__init__()

        #: base type that contains all REST path information
        self.pathPattern = None

        #: base type that contains all REST path information
        self.commands = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

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
        self.parameters = []

        #: information to a specific HTTP command
        self.requestBody = None

        #: information to a specific HTTP command
        self.responses = []

        #: information to a specific HTTP command
        self.security = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.command = CommandCommandEnum.valueForString(dict.get('command', None))

        arrayTags = dict.get('tags', [])
        for elemTags in arrayTags:
            obj.tags.append(elemTags)

        obj.summary = dict.get('summary', None)

        obj.description = dict.get('description', None)

        obj.operationId = dict.get('operationId', None)

        arrayParameters = dict.get('parameters', [])
        for elemParameters in arrayParameters:
            obj.parameters.append(
                Parameter.dictToObject(elemParameters))

        obj.requestBody = RequestBody.dictToObject(dict.get('requestBody', None))

        arrayResponses = dict.get('responses', [])
        for elemResponses in arrayResponses:
            obj.responses.append(
                Response.dictToObject(elemResponses))

        obj.security = CommandSecurity.dictToObject(dict.get('security', None))
        return obj


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

    def __init__(self):

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

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.inType = ParameterInTypeEnum.valueForString(dict.get('inType', None))

        obj.name = dict.get('name', None)

        obj.isArray = dict.get('isArray', None)

        obj.description = dict.get('description', None)

        obj.required = dict.get('required', None)

        obj.type = yacg.model.model.Type.dictToObject(dict.get('type', None))
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
        obj = cls()

        obj.description = dict.get('description', None)

        obj.required = dict.get('required', None)

        arrayContent = dict.get('content', [])
        for elemContent in arrayContent:
            obj.content.append(
                ContentEntry.dictToObject(elemContent))
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
        self.content = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.returnCode = dict.get('returnCode', None)

        obj.description = dict.get('description', None)

        arrayContent = dict.get('content', [])
        for elemContent in arrayContent:
            obj.content.append(
                ContentEntry.dictToObject(elemContent))
        return obj


class CommandSecurity:
    def __init__(self):

        self.scopes = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        arrayScopes = dict.get('scopes', [])
        for elemScopes in arrayScopes:
            obj.scopes.append(elemScopes)
        return obj


class ContentEntry:
    def __init__(self):

        self.mimeType = None

        self.type = None

        self.isArray = False

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.mimeType = dict.get('mimeType', None)

        obj.type = yacg.model.model.Type.dictToObject(dict.get('type', None))

        obj.isArray = dict.get('isArray', False)
        return obj


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



