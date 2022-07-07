"""Set of functions to smooth model handling for templates that create
Java code
"""

import yacg.model.model as model


def getJavaType(typeObj, isArray):
    """This method returns the name of Java class representing the model type 'typeObj'.
    If the type defined via 'typeObj' is used as array, then the name of a parameterize
    List is returned.

    Keyword arguments:
    typeObj -- type object to propcess
    isArray -- indicates whether the type is to be used as array.
    """
    if typeObj is None:
        return '???'
    elif isinstance(typeObj, model.IntegerType):
        if typeObj.format is None or typeObj.format == model.IntegerTypeFormatEnum.INT32:
            return 'Integer' if not isArray else 'java.util.List<Integer>'
        else:
            return 'Long' if not isArray else 'java.util.List<Long>'
    elif isinstance(typeObj, model.ObjectType):
        return 'Object'
    elif isinstance(typeObj, model.NumberType):
        if typeObj.format is None or typeObj.format == model.NumberTypeFormatEnum.DOUBLE:
            return 'Double' if not isArray else 'java.util.List<Double>'
        else:
            return 'Float' if not isArray else 'java.util.List<Float>'
    elif isinstance(typeObj, model.BooleanType):
        return 'Boolean' if not isArray else 'java.util.List<Boolean>'
    elif isinstance(typeObj, model.StringType):
        return 'String' if not isArray else 'java.util.List<String>'
    elif isinstance(typeObj, model.BytesType):
        return 'byte[]' if not isArray else 'java.util.List<byte[]>'
    elif isinstance(typeObj, model.UuidType):
        return 'java.util.UUID' if not isArray else 'java.util.List<java.util.UUID>'
    elif isinstance(typeObj, model.EnumType):
        return typeObj.name if not isArray else 'java.util.List<{}>'.format(typeObj.name)
    elif isinstance(typeObj, model.DateType):
        return 'java.time.LocalDate' if not isArray else 'java.util.List<java.time.LocalDate>'
    elif isinstance(typeObj, model.TimeType):
        return 'java.time.LocalTime' if not isArray else 'java.util.List<java.time.LocalTime>'
    elif isinstance(typeObj, model.DateTimeType):
        return 'java.time.LocalDateTime' if not isArray else 'java.util.List<java.time.LocalDateTime>'
    elif isinstance(typeObj, model.DictionaryType):
        return 'java.util.Map<String, {}>'.format(getJavaType(typeObj.valueType, False))
    elif isinstance(typeObj, model.ComplexType):
        return typeObj.name if not isArray else 'java.util.List<{}>'.format(typeObj.name)
    else:
        return '???'


def isInteger(typeObj):
    """Returns true if the type 'typeObj' represents the Java type Integer, false otherwise.

    Keyword arguments:
    typeObj -- type object to propcess
    """
    if isinstance(typeObj, model.IntegerType):
        return typeObj.format is None or typeObj.format == model.IntegerTypeFormatEnum.INT32
    return False


def isLong(typeObj):
    """Returns true if the type 'typeObj' represents the Java type Long, false otherwise.

    Keyword arguments:
    typeObj -- type object to propcess
    """
    return isinstance(typeObj, model.IntegerType) and model.IntegerTypeFormatEnum.INT64 == typeObj.format


def isDouble(typeObj):
    """Returns true if the type 'typeObj' represents the Java type Double, false otherwise.

    Keyword arguments:
    typeObj -- type object to propcess
    """
    if isinstance(typeObj, model.NumberType):
        return typeObj.format is None or typeObj.format == model.NumberTypeFormatEnum.DOUBLE 
    return False


def isFloat(typeObj):
    """Returns true if the type 'typeObj' represents the Java type Float, false otherwise.

    Keyword arguments:
    typeObj -- type object to propcess
    """
    return isinstance(typeObj, model.NumberType) and model.NumberTypeFormatEnum.FLOAT == typeObj.format


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

