'''Compfort function for model classes'''


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


def getPropertiesThatHasTag(tagName, typeObj):
    """check up if the as parameter given type has attributes that
    contain tag with the given name

    Keyword arguments:
    tagName -- name of the tag to look for
    typeObj -- type or property object to check up
    """

    propertiesWithTag = []
    for property in typeObj.properties:
        if hasTag(tagName, property):
            propertiesWithTag.append(property)
    return propertiesWithTag
