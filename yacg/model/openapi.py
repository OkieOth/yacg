# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum
import yacg.model.model


class PathType (yacg.model.model.Type):
    """ base type that contains all REST path information
    """

    def __init__(self, dictObj=None):
        super(yacg.model.model.Type, self).__init__()

        #: REST path with parameter pattern if existing
        self.pathPattern = None

        self.commands = []

        if dictObj is not None:
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

    def __init__(self, dictObj=None):

        #: HTTP command that is executed on the path
        self.command = None

        #: tags array of the open api path section
        self.tags = []

        self.summary = None

        self.description = None

        self.operationId = None

        self.parameters = []

        #: content of the request body that is passed to the back-end
        self.requestBody = None

        self.responses = []

        self.security = None

        if dictObj is not None:
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

        self.requestBody = RequestBody(dictObj.get('requestBody', None))

        arrayResponses = dictObj.get('responses', [])
        for elemResponses in arrayResponses:
            self.responses.append(
                Response(elemResponses))

        self.security = CommandSecurity(dictObj.get('security', None))


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

    def __init__(self, dictObj=None):

        #: how is the parameter passed to the back-end, attention
        self.inType = None

        #: name of the parameter
        self.name = None

        self.isArray = None

        #: some more words to explain for what this parameter is good for
        self.description = None

        #: tells if is this parameter optional
        self.required = None

        #: type that is passed as parameter
        self.type = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.inType = ParameterInTypeEnum.valueForString(dictObj.get('inType', None))

        self.name = dictObj.get('name', None)

        self.isArray = dictObj.get('isArray', None)

        self.description = dictObj.get('description', None)

        self.required = dictObj.get('required', None)

        self.type = yacg.model.model.Type(dictObj.get('type', None))


class RequestBody:
    """ definition of a parameter that is used in the request
    """

    def __init__(self, dictObj=None):

        #: some more words to explain for what this parameter is good for
        self.description = None

        #: tells if is this parameter optional
        self.required = None

        self.content = []

        if dictObj is not None:
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

    def __init__(self, dictObj=None):

        #: HTTP return code for the specific case
        self.returnCode = None

        self.description = None

        self.content = []

        if dictObj is not None:
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
    def __init__(self, dictObj=None):

        self.scopes = []

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        arrayScopes = dictObj.get('scopes', [])
        for elemScopes in arrayScopes:
            self.scopes.append(elemScopes)


class ContentEntry:
    def __init__(self, dictObj=None):

        #: mime type that is passed as request body
        self.mimeType = None

        #: meta model type that is passed in the body
        self.type = None

        self.isArray = False

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.mimeType = dictObj.get('mimeType', None)

        self.type = yacg.model.model.Type(dictObj.get('type', None))

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



