"""Set of functions to smooth model handling for templates that create
Json code
"""

import yacg.model.model as model


def getJsonType(type):
    if type is None:
        return '???'
    elif isinstance(type, model.IntegerType):
        return 'integer'
    elif isinstance(type, model.NumberType):
        return 'number'
    elif isinstance(type, model.BooleanType):
        return 'boolean'
    elif isinstance(type, model.StringType):
        return 'string'
    elif isinstance(type, model.UuidType):
        return 'string'
    elif isinstance(type, model.EnumType):
        return 'string'
    elif isinstance(type, model.DateType):
        return 'string'
    elif isinstance(type, model.DateTimeType):
        return 'string'
    elif isinstance(type, model.BytesType):
        return 'string'
    elif isinstance(type, model.ComplexType):
        return type.name
    else:
        return '???'


def printOpenApiJsonTypeEntry(type):
    if type is None:
        return '???'
    elif isinstance(type, model.ComplexType):
        return '"$ref": "#/components/schemas/{}"'.format(type.name)
    else:
        return '"type": "{}"'.format(getJsonType(type))


def isFormatRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.IntegerType) and (type.format is not None):
        return True
    elif isinstance(type, model.NumberType) and (type.format is not None):
        return True
    elif isinstance(type, model.UuidType):
        return True
    elif isinstance(type, model.DateType):
        return True
    elif isinstance(type, model.DateTimeType):
        return True
    elif isinstance(type, model.BytesType):
        return True
    else:
        return False


def printOpenApiJsonFormatEntry(type):
    if type is None:
        return ''
    elif isinstance(type, model.IntegerType) and (type.format is not None):
        return ',"format": "{}"'.format(type.format)
    elif isinstance(type, model.NumberType) and (type.format is not None):
        return ',"format": "{}"'.format(type.format)
    elif isinstance(type, model.UuidType):
        return ',"format": "uuid"'
    elif isinstance(type, model.DateType):
        return ',"format": "date"'
    elif isinstance(type, model.DateTimeType):
        return ',"format": "date-time"'
    elif isinstance(type, model.BytesType):
        return ',"format": "byte"'
    else:
        return ''


def isEnumRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.EnumType):
        return True
    else:
        return False


def printOpenApiJsonEnumEntry(type):
    if type is None:
        return '???'
    elif isinstance(type, model.EnumType):
        valueStr = None
        for value in type.values:
            if valueStr is None:
                valueStr = '"{}"'.format(value)
            else:
                valueStr = '{},"{}"'.format(valueStr, value)
        return '"enum": [{}]'.format(valueStr)
    else:
        return '???'


def isMinRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.IntegerType) and (type.minimum is not None):
        return True
    elif isinstance(type, model.NumberType) and (type.minimum is not None):
        return True
    elif isinstance(type, model.DateType) and (type.minimum is not None):
        return True
    elif isinstance(type, model.DateTimeType) and (type.minimum is not None):
        return True
    else:
        return False


def isExclusiveMinRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.IntegerType) and (type.exclusiveMinimum is not None):
        return True
    elif isinstance(type, model.NumberType) and (type.exclusiveMinimum is not None):
        return True
    elif isinstance(type, model.DateType) and (type.exclusiveMinimum is not None):
        return True
    elif isinstance(type, model.DateTimeType) and (type.exclusiveMinimum is not None):
        return True
    else:
        return False


def isMaxRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.IntegerType) and (type.maximum is not None):
        return True
    elif isinstance(type, model.NumberType) and (type.maximum is not None):
        return True
    elif isinstance(type, model.DateType) and (type.maximum is not None):
        return True
    elif isinstance(type, model.DateTimeType) and (type.maximum is not None):
        return True
    else:
        return False


def isExclusiveMaxRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.IntegerType) and (type.exclusiveMaximum is not None):
        return True
    elif isinstance(type, model.NumberType) and (type.exclusiveMaximum is not None):
        return True
    elif isinstance(type, model.DateType) and (type.exclusiveMaximum is not None):
        return True
    elif isinstance(type, model.DateTimeType) and (type.exclusiveMaximum is not None):
        return True
    else:
        return False


def isDefaultRequired(type):
    if type is None:
        return False
    elif isinstance(type, model.IntegerType) and (type.default is not None):
        return True
    elif isinstance(type, model.NumberType) and (type.default is not None):
        return True
    elif isinstance(type, model.BooleanType) and (type.default is not None):
        return True
    elif isinstance(type, model.StringType) and (type.default is not None):
        return True
    elif isinstance(type, model.UuidType) and (type.default is not None):
        return True
    elif isinstance(type, model.EnumType) and (type.default is not None):
        return True
    elif isinstance(type, model.DateType) and (type.default is not None):
        return True
    elif isinstance(type, model.DateTimeType) and (type.default is not None):
        return True
    else:
        return False
