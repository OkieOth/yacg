"""Set of functions to smooth model handling for templates that create
Java code
"""

import yacg.model.model as model


def getJavaType(type, isArray):
    if type is None:
        return '???'
    elif isinstance(type, model.IntegerType):
        return 'Integer' if not isArray else 'java.util.List<Integer>'
    elif isinstance(type, model.NumberType):
        return 'Double' if not isArray else 'java.util.List<Double>'
    elif isinstance(type, model.BooleanType):
        return 'Boolean' if not isArray else 'java.util.List<Boolean>'
    elif isinstance(type, model.StringType):
        return 'String' if not isArray else 'java.util.List<String>'
    elif isinstance(type, model.BytesType):
        return 'byte[]' if not isArray else 'java.util.List<byte[]>'
    elif isinstance(type, model.UuidType):
        return 'java.util.UUID' if not isArray else 'java.util.List<java.util.UUID>'
    elif isinstance(type, model.EnumType):
        return type.name if not isArray else 'java.util.List<{}>'.format(type.name)
    elif isinstance(type, model.DateType):
        return 'java.time.LocalDate' if not isArray else 'java.util.List<java.time.LocalData>'
    elif isinstance(type, model.DateTimeType):
        return 'java.time.LocalDateTime' if not isArray else 'java.util.List<java.time.LocalDataTime>'
    elif isinstance(type, model.ComplexType):
        return type.name if not isArray else 'java.util.List<{}>'.format(type.name)
    else:
        return '???'


def printExtendsType(type):
    if (not hasattr(type, 'extendsType')) or (type.extendsType is None):
        return ''
    return 'extends {} '.format(type.extendsType.name)
