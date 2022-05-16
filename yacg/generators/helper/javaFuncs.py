"""Set of functions to smooth model handling for templates that create
Java code
"""

import yacg.model.model as model


def getJavaType(type, isArray):
    if type is None:
        return '???'
    elif isinstance(type, model.IntegerType):
        if type.format is None or type.format == model.IntegerTypeFormatEnum.INT32:
            return 'Integer' if not isArray else 'java.util.List<Integer>'
        else:
            return 'Long' if not isArray else 'java.util.List<Long>'
    elif isinstance(type, model.ObjectType):
        return 'Object'
    elif isinstance(type, model.NumberType):
        if type.format is None or type.format == model.NumberTypeFormatEnum.DOUBLE:
            return 'Double' if not isArray else 'java.util.List<Double>'
        else:
            return 'Float' if not isArray else 'java.util.List<Float>'
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
        return 'java.time.LocalDate' if not isArray else 'java.util.List<java.time.LocalDate>'
    elif isinstance(type, model.DateTimeType):
        return 'java.time.LocalDateTime' if not isArray else 'java.util.List<java.time.LocalDateTime>'
    elif isinstance(type, model.DictionaryType):
        return 'java.util.Map<String, {}>'.format(getJavaType(type.valueType, False))
    elif isinstance(type, model.ComplexType):
        return type.name if not isArray else 'java.util.List<{}>'.format(type.name)
    else:
        return '???'


def printExtendsType(type):
    if (not hasattr(type, 'extendsType')) or (type.extendsType is None):
        return ''
    return 'extends {} '.format(type.extendsType.name)
