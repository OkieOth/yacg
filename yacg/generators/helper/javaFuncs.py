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


def sanitizePropertyNames(typeObj):
    """This method will visit all properties of the (ComplexType) 'typeObj' and
    check, whether the property name is not suited for java attribute (class, enum, for etc)
    It will replace thes property name in-place with unproblematic ones.
    These changes are recorded in a Dictionary object and returned to the call so
    that the original property names can be restore, see method 'restorePropertyNames(typeObj, propIdx2originalName)'

    Keyword arguments:
    typeObj -- type object to propcess
    """
    propIdx2originalName = {}
    if isinstance(typeObj, model.ComplexType):
        illegalNames = ['enum', 'class']
        alternativeNames = ['enumValue', 'clazz']
        for idxProp, prop in enumerate(typeObj.properties):
            for idxName, name in enumerate(illegalNames):
                if prop.name == name:
                    print('altering prop #{}: {}->{}'.format(idxProp, prop.name, alternativeNames[idxName]))
                    propIdx2originalName[idxProp] = prop.name
                    prop.name = alternativeNames[idxName]
                    break
    return propIdx2originalName


def restorePropertyNames(typeObj, propIdx2originalName):
    """This method can be used to restore the original property names of the (Complex) 'typeObj',
    which were altered by method 'sanitizePropertyNames(typeObj)' as they are not suited for java
    attribute (class, enum, for etc). 
    It needs the Dictionary with the records of the changes, which was returned by said function,
    for restoring the property names.

    Keyword arguments:
    typeObj -- type object to propcess
    propIdx2originalName -- The record of the rename operations, which are to be reverted.
    """
    if isinstance(typeObj, model.ComplexType):
        for idx, name in propIdx2originalName.items():
            typeObj.properties[idx].name = name

