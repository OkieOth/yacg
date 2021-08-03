'''Compfort function for model classes'''

import yacg.model.model as model
import yacg.model.openapi as openapi


def hasTag(tagName, typeOrPropertyObj):
    """check up if the as parameter given object has a tag with the
    given name

    Keyword arguments:
    tagName -- name of the tag to look for
    typeOrPropertyObj -- type or property object to check up
    """

    if not hasattr(typeOrPropertyObj, 'tags'):
        return False
    for tag in typeOrPropertyObj.tags:
        if tag.name == tagName:
            return True
    return False


def hasProperty(propertyName, typeObj):
    """check up if the as parameter given type has a property with the
    given name

    Keyword arguments:
    propertyName -- name of the property to look for
    typeObj -- type object to check up
    """

    if not hasattr(typeObj, 'properties'):
        return False
    for property in typeObj.properties:
        if property.name == propertyName:
            return True
    return False


def getPropertiesThatHasTag(tagName, typeObj):
    """check up if the as parameter given type has attributes that
    contain tag with the given name

    Keyword arguments:
    tagName -- name of the tag to look for
    typeObj -- type or property object to check up
    """

    propertiesWithTag = []
    if typeObj.properties is None:
        return propertiesWithTag
    for property in typeObj.properties:
        if hasTag(tagName, property):
            propertiesWithTag.append(property)
    return propertiesWithTag


def getFlattenProperties(typeObj):
    """provides all properties of the type and all the properties of its base
    classes in a single list

    Keyword arguments:
    typeObj -- type or property object to check up
    """

    flattenProperties = []
    if typeObj.properties is not None:
        for property in typeObj.properties:
            flattenProperties.append(property)
    baseType = typeObj.extendsType
    while baseType is not None:
        for property in baseType.properties:
            flattenProperties.append(property)
        baseType = baseType.extendsType

    return flattenProperties


def hasEnumTypes(modelTypes):
    for type in modelTypes:
        if isEnumType(type):
            return True
    return False


def flattenTypes(loadedTypes):
    for type in loadedTypes:
        if isinstance(type, model.ComplexType):
            flattenProperties = getFlattenProperties(type)
            type.properties = flattenProperties
            type.extendsType = None
    return loadedTypes


def processYacgTags(loadedTypes):
    typesToReturn = []
    for type in loadedTypes:
        if isinstance(type, model.ComplexType):
            if hasTag("yacgIgnoreForModel", type):
                continue
            if hasTag("yacgFlattenType", type):
                flattenProperties = getFlattenProperties(type)
                type.properties = flattenProperties
                type.extendsType = None
        typesToReturn.append(type)
    return typesToReturn


def isEnumType(typeObj):
    """checks if the given type object is an EnumType. If that's the
    case then True is returned, else the return is false

    Keyword arguments:
    typeObj -- type or property object to check up
    """

    return isinstance(typeObj, model.EnumType)


def getTypeName(type):
    return type.name if hasattr(type, 'name') else type.__class__.__name__


def separateOpenApiPathTypes(types):
    """function returns a list that consists of three elems:
    1. OpenApi PathTypes
    2. Non enum types
    3. Enum types

    Keyword arguments:
    types -- list of model.Type instances
    """

    pathTypes = []
    nonEnumTypes = []
    enumTypes = []
    for type in types:
        if isinstance(type, openapi.PathType):
            pathTypes.append(type)
        elif isinstance(type, model.EnumType):
            enumTypes.append(type)
        else:
            nonEnumTypes.append(type)
    return (pathTypes, nonEnumTypes, enumTypes)


def getOpenApiTags(types):
    """function returns a list with used OpenApi operation tags.

    Keyword arguments:
    types -- list of model.Type instances
    """

    tags = []
    for type in types:
        if isinstance(type, openapi.PathType):
            for command in type.commands:
                for tag in command.tags:
                    if tag not in tags:
                        tags.append(tag)
    return tags


def isBaseType(type):
    if isinstance(type, model.EnumType):
        return False
    elif isinstance(type, model.ComplexType):
        return False
    else:
        return True


def getTypesWithTag(types, tags):
    """function returns all types that have a specific tag

    Keyword arguments:
    types -- list of model.Type instances
    tags -- list of strings with tag names
    """

    typesWithTag = []
    for type in types:
        for tag in tags:
            if hasTag(tag, type):
                typesWithTag.append(type)
                break
    return typesWithTag


def getTypesWithName(types, names):
    """function returns all types that have a specific name

    Keyword arguments:
    types -- list of model.Type instances
    names -- list of strings with names
    """

    typesWithName = []
    for type in types:
        for name in names:
            if type.name == name:
                typesWithName.append(type)
                break
    return typesWithName


def getNonEnumModelType(types):
    """function returns all types that are not EnumTypes

    Keyword arguments:
    types -- list of model.Type instances
    """

    nonEnumTypes = []
    for type in types:
        if not isEnumType(type):
            nonEnumTypes.append(type)
    return nonEnumTypes


def getDomainsAsList(modelTypes):
    """returns a list of domain strings from the model types

    Keyword arguments:
    modelTypes -- types of that model
    """

    domainList = []
    for type in modelTypes:
        if (type.domain is not None) and (type.domain not in domainList):
            domainList.append(type.domain)
        if (hasattr(type, 'extendsType')) and (type.extendsType is not None):
            if (type.extendsType.domain is not None) and (type.extendsType.domain not in domainList):
                domainList.append(type.extendsType.domain)
        if not hasattr(type, 'property'):
            continue
        for property in type.properties:
            if property.type is None:
                continue
            propDomain = property.type.domain
            if (propDomain is not None) and (propDomain not in domainList):
                domainList.append(propDomain)

    return domainList


def isTimestampContained(modelTypes):
    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.DateTimeType)):
                    return True
    return False


def isDateContained(modelTypes):
    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.DateType)):
                    return True
    return False
