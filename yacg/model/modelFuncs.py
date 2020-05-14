'''Compfort function for model classes'''

import yacg.model.model as model


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


def isEnumType(typeObj):
    """checks if the given type object is an EnumType. If that's the
    case then True is returned, else the return is false

    Keyword arguments:
    typeObj -- type or property object to check up
    """

    return isinstance(typeObj, model.EnumType)


def getTypeName(type):
    return type.name if hasattr(type, 'name') else type.__class__.__name__


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
    return domainList
