# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

from enum import Enum
import yacg.model.shared.info
import yacg.model.model


class OpenApiServer:
    def __init__(self, dictObj=None):
        self.url = None
        self.description = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.url is not None:
            ret["url"] = self.url
        if self.description is not None:
            ret["description"] = self.description
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.url = dictObj.get('url', None)

        self.description = dictObj.get('description', None)


class OpenApiInfo (yacg.model.shared.info.InfoSection):
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


class Command:
    """information to a specific HTTP command
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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.command is not None:
            ret["command"] = CommandCommandEnum.valueAsString(self.command)
        if (self.tags is not None) and (len(self.tags) > 0):
            ret["tags"] = self.tags
        if self.summary is not None:
            ret["summary"] = self.summary
        if self.description is not None:
            ret["description"] = self.description
        if self.operationId is not None:
            ret["operationId"] = self.operationId
        if (self.parameters is not None) and (len(self.parameters) > 0):
            ret["parameters"] = self.parameters.toDict()
        if self.requestBody is not None:
            ret["requestBody"] = self.requestBody.toDict()
        if (self.responses is not None) and (len(self.responses) > 0):
            ret["responses"] = self.responses.toDict()
        if self.security is not None:
            ret["security"] = self.security.toDict()
        return ret


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

        subDictObj = dictObj.get('requestBody', None)
        if subDictObj is not None:
            self.requestBody = RequestBody(subDictObj)

        arrayResponses = dictObj.get('responses', [])
        for elemResponses in arrayResponses:
            self.responses.append(
                Response(elemResponses))

        subDictObj = dictObj.get('security', None)
        if subDictObj is not None:
            self.security = CommandSecurity(subDictObj)


class PathType (yacg.model.model.Type):
    """base type that contains all REST path information
    """

    def __init__(self, dictObj=None):
        yacg.model.model.Type.__init__(self)

        #: REST path with parameter pattern if existing
        self.pathPattern = None
        self.commands = []

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.pathPattern is not None:
            ret["pathPattern"] = self.pathPattern
        if (self.commands is not None) and (len(self.commands) > 0):
            ret["commands"] = self.commands.toDict()
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.pathPattern = dictObj.get('pathPattern', None)

        arrayCommands = dictObj.get('commands', [])
        for elemCommands in arrayCommands:
            self.commands.append(
                Command(elemCommands))


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
    """definition of a parameter that is used in the request
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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.inType is not None:
            ret["inType"] = ParameterInTypeEnum.valueAsString(self.inType)
        if self.name is not None:
            ret["name"] = self.name
        if self.isArray is not None:
            ret["isArray"] = self.isArray
        if self.description is not None:
            ret["description"] = self.description
        if self.required is not None:
            ret["required"] = self.required
        if self.type is not None:
            ret["type"] = self.type.toDict()
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.inType = ParameterInTypeEnum.valueForString(dictObj.get('inType', None))

        self.name = dictObj.get('name', None)

        self.isArray = dictObj.get('isArray', None)

        self.description = dictObj.get('description', None)

        self.required = dictObj.get('required', None)

        subDictObj = dictObj.get('type', None)
        if subDictObj is not None:
            self.type = yacg.model.model.Type(subDictObj)


class RequestBody:
    """definition of a parameter that is used in the request
    """

    def __init__(self, dictObj=None):

        #: some more words to explain for what this parameter is good for
        self.description = None

        #: tells if is this parameter optional
        self.required = None
        self.content = []

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.description is not None:
            ret["description"] = self.description
        if self.required is not None:
            ret["required"] = self.required
        if (self.content is not None) and (len(self.content) > 0):
            ret["content"] = self.content.toDict()
        return ret


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
    """description of a response option for a request
    """

    def __init__(self, dictObj=None):

        #: HTTP return code for the specific case
        self.returnCode = None
        self.description = None
        self.content = []

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.returnCode is not None:
            ret["returnCode"] = self.returnCode
        if self.description is not None:
            ret["description"] = self.description
        if (self.content is not None) and (len(self.content) > 0):
            ret["content"] = self.content.toDict()
        return ret


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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if (self.scopes is not None) and (len(self.scopes) > 0):
            ret["scopes"] = self.scopes
        return ret


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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.mimeType is not None:
            ret["mimeType"] = self.mimeType
        if self.type is not None:
            ret["type"] = self.type.toDict()
        if self.isArray is not None:
            ret["isArray"] = self.isArray
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.mimeType = dictObj.get('mimeType', None)

        subDictObj = dictObj.get('type', None)
        if subDictObj is not None:
            self.type = yacg.model.model.Type(subDictObj)

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



