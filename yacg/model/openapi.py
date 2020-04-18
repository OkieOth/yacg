# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Path:
    """ base type that contains all REST path information
    """

    def __init__(self):

        #: base type that contains all REST path information
        self.pathPattern = None

        #: base type that contains all REST path information
        self.commands = []


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


class CommandCommandEnum(Enum):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'


class CommandConsumesEnum(Enum):
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'


class CommandProducesEnum(Enum):
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'


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


class RequestBodyContent:
    def __init__(self):

        self.mimeType = None

        self.type = None


class Type:
    """ Dummy base class to implement strong typed references
    """

    def __init__(self):
        pass


class ParameterInTypeEnum(Enum):
    PATH = 'path'
    QUERY = 'query'
    HEADER = 'header'
    COOKIE = 'cookie'


