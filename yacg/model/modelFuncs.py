'''Compfort function for model classes'''

import yacg.model.model as model
import yacg.model.openapi as openapi
import os


def hasTag(tagName, typeOrPropertyObj):
    """check up if the type or property has a tag with the
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


def hasPropertyWithTag(tagName, typeObj):
    """check up if the type has a property that contains a tag with the
    given name

    Keyword arguments:
    tagName -- name of the tag to look for
    typeObj -- type to check up
    """

    for property in typeObj.properties:
        if hasTag(tagName, property):
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


def hasKey(typeObj):
    """checks if a specific type object has a property that is marked as
    unique key.
    Returns 'True' if a key property is contained, else 'False'

    Keyword arguments:
    typeObj -- type object to check up
    """

    if not hasattr(typeObj, 'properties'):
        return False
    for property in typeObj.properties:
        if property.isKey:
            return True
    return False


def getKeyProperty(typeObj):
    """Returns the Property object that is marked as key.
    Attention, key tupels are not supported.
    If no key is contained, the function returns 'None'

    Keyword arguments:
    typeObj -- type object to check up
    """

    if not hasattr(typeObj, 'properties'):
        return None
    for property in typeObj.properties:
        if property.isKey:
            return property
    return None


def getPropertiesThatHasTag(tagName, typeObj):
    """check up if the as parameter given type has properties that
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
    if isinstance(typeObj, model.DictionaryType):
        return flattenProperties
    if typeObj.properties is not None:
        for property in typeObj.properties:
            flattenProperties.append(property)
    baseType = typeObj.extendsType
    while baseType is not None:
        # currently only ComplexType has a field extendsType, and ComplexType.properties may be empty
        # but should never be None!
        for property in baseType.properties:
            alreadyIncluded = False
            for fp in flattenProperties:
                if (fp.name == property.name) and (fp.type == property.type):
                    alreadyIncluded = True
                    break
            if not alreadyIncluded:
                flattenProperties.append(property)
        baseType = baseType.extendsType

    return flattenProperties


def hasEnumTypes(modelTypes):
    for type in modelTypes:
        if isEnumType(type):
            return True
    return False


def hasTypeProperties(type):
    return hasattr(type, 'properties') and len(type.properties) > 0


def hasTypeExtendsType(type):
    return hasattr(type, 'extendsType') and type.extendsType is not None


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


def isDictionaryType(typeObj):
    """checks if the given type object is an DictionaryType. If that's the
    case then True is returned, else the return is false

    Keyword arguments:
    typeObj -- type or property object to check up
    """

    return isinstance(typeObj, model.DictionaryType)


def isComplexType(typeObj):
    """checks if the given type object is a ComplexType. If that's the
    case then True is returned, else the return is false

    Keyword arguments:
    typeObj -- type or property object to check up
    """

    return isinstance(typeObj, model.ComplexType)


def getTypeName(type):
    return type.name if hasattr(type, 'name') else type.__class__.__name__


def separateOpenApiPathTypes(types):
    """function returns a list that consists of three elems:
    1. OpenApi PathTypes
    2. Other types
    3. Enum types
    4. Info type
    5. Servers type

    Keyword arguments:
    types -- list of model.Type instances
    """

    pathTypes = []
    nonEnumTypes = []
    enumTypes = []
    infoType = None
    serverTypes = []
    for type in types:
        if isinstance(type, openapi.PathType):
            pathTypes.append(type)
        elif isinstance(type, model.EnumType):
            enumTypes.append(type)
        elif isinstance(type, openapi.OpenApiInfo):
            infoType = type
        elif isinstance(type, openapi.OpenApiServer):
            serverTypes.append(type)
        else:
            nonEnumTypes.append(type)
    return (pathTypes, nonEnumTypes, enumTypes, infoType, serverTypes)


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


def isBaseOrDictionaryType(type):
    if isDictionaryType(type):
        return True
    return isBaseType(type)


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
    """returns True, if at least one of model types contains a property of type model.DateTimeType, False otherwise.

    Keyword arguments:
    modelTypes -- types of the model
    """

    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.DateTimeType)):
                    return True
    return False


def isDateContained(modelTypes):
    """returns True, if at least one of model types contains a property of type model.DateType, False otherwise.

    Keyword arguments:
    modelTypes -- types of the model
    """

    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.DateType)):
                    return True
    return False


def isTimeContained(modelTypes):
    """returns True, if at least one of model types contains a property of type model.TimeType, False otherwise.

    Keyword arguments:
    modelTypes -- types of the model
    """

    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.TimeType)):
                    return True
    return False


def isUuidContained(modelTypes):
    """returns True, if at least one of model types contains a property of type model.UuidType, False otherwise.

    Keyword arguments:
    modelTypes -- types of the model
    """

    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.UuidType)):
                    return True
    return False


def isObjectContained(modelTypes):
    """returns True, if at least one of model types contains a property of type model.ObjectType, False otherwise.

    Keyword arguments:
    modelTypes -- types of the model
    """
    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, model.ObjectType)):
                    return True
    return False


def isTypeContained(modelTypes, targetType):
    """returns True, if at least one of model types contains a property of target type, e.g. model.ObjectType, False otherwise.

    Keyword arguments:
    modelTypes -- types of the model
    targetType -- the model type to look for, e.g. model.TimeType.
    """
    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for property in type.properties:
                if (property.type is not None) and (isinstance(property.type, targetType)):
                    return True
    return False


def doesTypeOrAttribContainsType(typeObj, type):
    if hasattr(typeObj, "properties"):
        for prop in typeObj.properties:
            if isinstance(prop.type, type):
                return True
            if isinstance(prop.type, model.ComplexType):
                if doesTypeOrAttribContainsType(prop.type, type):
                    return True
    return False


def getPropertyTagNamesForType(typeObj):
    ret = []
    if hasattr(typeObj, "properties"):
        for prop in typeObj.properties:
            for tag in prop.tags:
                if tag.name not in ret:
                    ret.append(tag.name)
    return ret


def __getTypeAndAllChildTypesImpl(type, alreadyFoundTypeNames, alreadyFoundTypes):
    if type.name not in alreadyFoundTypeNames:
        alreadyFoundTypeNames.append(type.name)
        alreadyFoundTypes.append(type)
        if hasattr(type, 'properties'):
            for prop in type.properties:
                if not isBaseType(prop.type):
                    __getTypeAndAllChildTypesImpl(prop.type, alreadyFoundTypeNames, alreadyFoundTypes)


def getTypeAndAllChildTypes(type):
    """returns the type and all non-base types that are related to direct childs
    or childs of childs

    Keyword arguments:
    type -- types to start to find the relations
    """

    alreadyFoundTypeNames = []
    ret = []
    __getTypeAndAllChildTypesImpl(type, alreadyFoundTypeNames, ret)
    return ret


def __getTypeAndAllRelatedTypesImpl(type, alreadyFoundTypeNames, alreadyFoundTypes):
    if type.name not in alreadyFoundTypeNames:
        alreadyFoundTypeNames.append(type.name)
        alreadyFoundTypes.append(type)
        if hasattr(type, 'extendsType') and type.extendsType is not None:
            if not isBaseType(type.extendsType):
                __getTypeAndAllRelatedTypesImpl(type.extendsType, alreadyFoundTypeNames, alreadyFoundTypes)
        if hasattr(type, 'properties'):
            for prop in type.properties:
                if not isBaseType(prop.type):
                    __getTypeAndAllRelatedTypesImpl(prop.type, alreadyFoundTypeNames, alreadyFoundTypes)


def getTypeAndAllRelatedTypes(type):
    """returns the type and all non-base types that are related to direct childs
    or childs of childs. Also allOf relations are included in the return list

    Keyword arguments:
    type -- types to start to find the relations
    """

    alreadyFoundTypeNames = []
    ret = []
    __getTypeAndAllRelatedTypesImpl(type, alreadyFoundTypeNames, ret)
    return ret


def __copyTypeAndAllChildTypes(type, alreadyFoundNamesList, alreadyFoundTypesList):
    if type.name not in alreadyFoundNamesList:
        alreadyFoundNamesList.append(type.name)
        alreadyFoundTypesList.append(type)
        if hasattr(type, 'properties'):
            for prop in type.properties:
                if not isBaseType(prop.type):
                    __copyTypeAndAllChildTypes(prop.type, alreadyFoundNamesList, alreadyFoundTypesList)


def getTypesRelatedTagName(types, tagName):
    """function returns all types that have a relation to a type that
    contains a specific tag

    Keyword arguments:
    types -- list of model.Type instances
    tagName -- name of the tag to search for
    """

    typesWithTag = getTypesWithTag(types, [tagName])
    alreadyFoundTypeNames = []
    ret = []
    for type in typesWithTag:
        __copyTypeAndAllChildTypes(type, alreadyFoundTypeNames, ret)
    return ret


def hasPropertyOfType(typeObj, propType):
    """This method checks, whether the (ComplexType) 'typeObj' contains
    at least one property of the type 'propType' (not recursive).

    Keyword arguments:
    typeObj -- type object to check up
    propType -- type to search in the object's properties"""

    for prop in getFlattenProperties(typeObj):
        if isinstance(prop.type, propType):
            return True
    return False


def hasSinglePropertyOfType(typeObj, propType):
    """This method checks, whether the (ComplexType) 'typeObj' contains
    at least one non-array property of the type 'propType' (not recursive).

    Keyword arguments:
    typeObj -- type object to check up
    propType -- type to search in the object's properties"""

    for prop in getFlattenProperties(typeObj):
        if isinstance(prop.type, propType) and not prop.isArray:
            return True
    return False


def hasArrayPropertyOfType(typeObj, propType):
    """This method checks, whether the (ComplexType) 'typeObj' contains
    at least one array property of the type 'propType' (not recursive).

    Keyword arguments:
    typeObj -- type object to check up
    propType -- type to search in the object's properties"""

    for prop in getFlattenProperties(typeObj):
        if prop.isArray and isinstance(prop.type, propType):
            return True
    return False


def getComplexTypesInProperties(typeObj):
    """This method takes a (ComplexType) 'typeObj', iterates through its properties (not recursive)
    and returns an ordered set of the complex types it encountered.
    May return an empty sets but never 'None'!

    Keyword arguments:
    typeObj -- type object to check up"""

    types = []
    for prop in getFlattenProperties(typeObj):
        if isinstance(prop.type, model.ComplexType):
            types.append(prop.type)
    return list(dict.fromkeys(types))


def mapComplexTypesInProperties(typeObj, mapFunction=None):
    """This method takes a (ComplexType) 'typeObj' iterates through its properties (not recursive)
    and creates an ordered set of the complex types it encountered.
    If an (optional) 'mapFunction' (e.g. a lambda) is provided, it is applied to the set of types,
    otherwise the types are returned as is.
    May return an empty sets but never 'None'!

    Keyword arguments:
    typeObj -- type object to check up
    mapFunction -- the (optional) function, which will be applied to all complex types"""

    unique = getComplexTypesInProperties(typeObj)
    if mapFunction is None:
        return unique
    return list(map(mapFunction, unique))


def filterProps(typeObj, func):
    """This method returns a list with all propertis of the type 'typeObj',
    which match the provided predicate 'func' (e.g. lambda).
    May return an empty list but never 'None'!

    Keyword arguments:
    typeObj -- type object to check up
    func -- the function, which will be used to filter the properties"""

    props = getFlattenProperties(typeObj)
    if not any(props):
        return []
    return list(filter(func, props))


def getNotUniqueTypeNames(typeList):
    """This method returns a list of names that are not unique in the given
    typeList.

    Keyword arguments:
    typeList -- list of types to check for unique names"""

    typeNamesList = []
    notUniqueNames = []
    for t in typeList:
        if not hasattr(t, 'name'):
            continue
        if (t.name in typeNamesList) and (t.name not in notUniqueNames):
            notUniqueNames.append(t.name)
        typeNamesList.append(t.name)
    return notUniqueNames


def makeTypeNamesUnique(typeList, redundantNamesList):
    """This function goes over a list of loaded types and makes redundant names unique.
    Attention, this is a dangerous function because it changes the original input,
    instead of creating a copy
    """

    redundantTypesDict = {}
    for redundantName in redundantNamesList:
        for t in typeList:
            if t.name == redundantName:
                alreadyLoadedList = redundantTypesDict.get(redundantName, [])
                if len(alreadyLoadedList) == 0:
                    redundantTypesDict[redundantName] = alreadyLoadedList
                alreadyLoadedList.append(t)
    for key, redundantTypesList in redundantTypesDict.items():
        counter = 1
        for t in redundantTypesList:
            if t == redundantTypesList[0]:
                continue
            counter = counter + 1
            # sure a really simple approach, can later extracted in a more sophisticated working function
            t.name = "{}_{}".format(t.name, counter)


def getExternalRefStringsFromDict(schemaDict, foundReferencesList):
    """Travers a dictionary with a parsed schema and find all values to
    '$ref' entries. The found values are added to foundReferencesList.

    Keyword arguments:
    schemaDict -- dictionary parsed directly from JSON or YAML
    foundReferencesList -- string list with found references"""

    for key, value in schemaDict.items():
        if isinstance(value, dict):
            getExternalRefStringsFromDict(value, foundReferencesList)
        if isinstance(value, list):
            _getExternalRefStringsFromList(value, foundReferencesList)
        else:
            if (key == '$ref') and isinstance(value, str):
                lowerValue = value.lower()
                externalRef = (lowerValue.find('.json') != -1) or (lowerValue.find('.yaml') != -1) or (lowerValue.find('.yml') != -1)
                if externalRef and (value not in foundReferencesList):
                    foundReferencesList.append(value)


def _getExternalRefStringsFromList(schemaListPart, foundReferencesList):
    for elem in schemaListPart:
        if isinstance(elem, dict):
            getExternalRefStringsFromDict(elem, foundReferencesList)
        if isinstance(elem, list):
            _getExternalRefStringsFromList(elem, foundReferencesList)


def initReferenceHelperDict(foundReferencesList, modelFile):
    absPath = os.path.abspath(modelFile)
    lastSlash = absPath.rfind("/")
    absDirPath = absPath[:lastSlash]
    ret = {}
    for f in foundReferencesList:
        ret[f] = ReferenceHelper()
        sepIndex = f.find('#')
        fileName = f if sepIndex == -1 else f[:sepIndex]
        ret[f].fileName = os.path.abspath(absDirPath + "/" + fileName)
        ret[f].topLevelType = True if sepIndex == -1 else False
        if not ret[f].topLevelType:
            restStr = f[sepIndex:]
            lastSlash2 = restStr.rfind("/")
            ret[f].typeName = restStr[lastSlash2 + 1:]
    return ret


def _traversModelTypesForRefAndTypeName(modelTypes, refFile, typeName):
    for t in modelTypes:
        if (hasattr(t, "source")) and (t.source == refFile) and (t.name == typeName):
            return t
    return None


def _traversModelTypesForRefAndTopLevelType(modelTypes, refFile):
    for t in modelTypes:
        if (hasattr(t, "source")) and (t.source == refFile) and t.topLevelType:
            return t
    return None


def initTypesInReferenceHelperDict(refHelperDict, modelTypes):
    for ref, helperObj in refHelperDict.items():
        if helperObj.topLevelType:
            helperObj.type = _traversModelTypesForRefAndTopLevelType(modelTypes, helperObj.fileName)
            helperObj.typeName = helperObj.type.name if helperObj.type is not None else None
        else:
            helperObj.type = _traversModelTypesForRefAndTypeName(modelTypes, helperObj.fileName, helperObj.typeName)


def getLocalTypePrefix(schemaAsDict):
    schemaDefinitions = schemaAsDict.get('definitions', None)
    if schemaDefinitions is not None:
        return "#/definitions/"
    else:
        componentsDict = schemaAsDict.get('components', None)
        if componentsDict is not None:
            return "#/components/schemas/"
    return None


def _getTypeType(type):
    if isinstance(type, model.ComplexType):
        return "object"
    elif isinstance(type, model.DictionaryType):
        return "object"
    elif isinstance(type, model.ArrayType):
        return "array"
    elif isinstance(type, model.EnumType):
        return "string"
    elif isinstance(type, model.IntegerType):
        return 'integer'
    elif isinstance(type, model.ObjectType):
        return 'object'
    elif isinstance(type, model.NumberType):
        return 'number'
    elif isinstance(type, model.BooleanType):
        return 'boolean'
    elif isinstance(type, model.StringType):
        return 'string'
    elif isinstance(type, model.UuidType):
        return 'string'
    elif isinstance(type, model.DateType):
        return 'string'
    elif isinstance(type, model.TimeType):
        return 'string'
    elif isinstance(type, model.DateTimeType):
        return 'string'
    elif isinstance(type, model.BytesType):
        return 'string'
    else:
        return "object"


def __printComplexTypeProperties(type, localTypePrefix):
    propertiesDict = {}
    requiredArray = []
    for p in type.properties:
        propertiesDict[p.name] = {}
        curDict = propertiesDict[p.name]
        if p.isArray:
            propertiesDict[p.name] = {}
            curDict = propertiesDict[p.name]
            for i in range(p.arrayDimensions):
                curDict["type"] = "array"
                curDict["items"] = {}
                curDict = curDict["items"]

        if isinstance(p.type, model.ComplexType):
            curDict["$ref"] = "{}{}".format(localTypePrefix, p.type.name)
        elif isinstance(p.type, model.EnumType):
            curDict["$ref"] = "{}{}".format(localTypePrefix, p.type.name)
        else:
            propertiesDict[p.name] = typeToJSONDict(p.type, localTypePrefix)
        if p.required:
            requiredArray.append(p.name)
    return propertiesDict, requiredArray


def _initComplexTypeDict(type, ret, localTypePrefix):
    if type.extendsType is not None:
        allOfArray = []
        allOfArray.append({})
        allOfArray[0]["$ref"] = "{}{}".format(localTypePrefix, type.extendsType.name)
        allOfArray.append({})
        allOfArray[1]["properties"], requiredArray = __printComplexTypeProperties(type, localTypePrefix)
        ret["allOf"] = allOfArray
    else:
        ret["properties"], requiredArray = __printComplexTypeProperties(type, localTypePrefix)
    if len(requiredArray) > 0:
        ret["required"] = requiredArray


def _initDictionaryTypeDict(type, ret, localTypePrefix):
    ret["additionalProperties"] = typeToJSONDict(type.valueType, localTypePrefix)


def _initArrayTypeDict(type, ret, localTypePrefix):
    __initArrayConstraints(type, ret, 0)
    if (type.arrayDimensions is not None) and (type.arrayDimensions > 1):
        realItemsDict = ret
        for i in range(type.arrayDimensions - 1):
            subDict = {}
            subDict["type"] = "array"
            __initArrayConstraints(type, subDict, i + 1)
            realItemsDict["items"] = subDict
            realItemsDict = subDict
        realItemsDict["items"] = typeToJSONDict(type.itemsType, localTypePrefix)
    else:
        ret["items"] = typeToJSONDict(type.itemsType, localTypePrefix)


def _initEnumTypeDict(type, ret):
    __initDefaultValue(type, ret)
    ret["enum"] = type.values


def _initIntegerTypeDict(type, ret):
    if type.format is not None:
        ret["format"] = model.IntegerTypeFormatEnum.valueAsString(type.format)
    __initNumConstraints(type, ret)
    __initDefaultValue(type, ret)


def _initNumberTypeDict(type, ret):
    if type.format is not None:
        ret["format"] = model.NumberTypeFormatEnum.valueAsString(type.format)
    __initNumConstraints(type, ret)
    __initDefaultValue(type, ret)


def _initBoolTypeDict(type, ret):
    __initDefaultValue(type, ret)


def _initStringTypeDict(type, ret):
    __initDefaultValue(type, ret)
    if type.minLength is not None:
        ret["minLength"] = type.minLength
    if type.maxLength is not None:
        ret["maxLength"] = type.maxLength
    if type.pattern is not None:
        ret["pattern"] = type.pattern


def _initUuidTypeDict(type, ret):
    ret["format"] = "uuid"
    __initDefaultValue(type, ret)


def _initDateTypeDict(type, ret):
    ret["format"] = "date"
    __initNumConstraints(type, ret)
    __initDefaultValue(type, ret)


def _initTimeTypeDict(type, ret):
    ret["format"] = "time"
    __initNumConstraints(type, ret)
    __initDefaultValue(type, ret)


def _initDateTimeTypeDict(type, ret):
    ret["format"] = "date-time"
    __initNumConstraints(type, ret)
    __initDefaultValue(type, ret)


def _initBytesTypeDict(type, ret):
    ret["format"] = "byte"
    __initDefaultValue(type, ret)


def __initDefaultValue(type, ret):
    if type.default is not None:
        ret["default"] = type.default


def __initArrayConstraints(type, ret, index):
    if len(type.arrayConstraints) > index:
        constraints = type.arrayConstraints[index]
        if constraints.arrayMinItems is not None:
            ret["minItems"] = constraints.arrayMinItems
        if constraints.arrayMaxItems is not None:
            ret["maxItems"] = constraints.arrayMaxItems
        if constraints.arrayUniqueItems is not None:
            ret["uniqueItems"] = constraints.arrayUniqueItems


def __initNumConstraints(type, ret):
    if type.minimum is not None:
        ret["mininum"] = type.minimum
    if type.maximum is not None:
        ret["maxinum"] = type.maximum
    if type.exclusiveMinimum is not None:
        ret["exclusiveMininum"] = type.exclusiveMinimum
    if type.exclusiveMaximum is not None:
        ret["exclusiveMaxinum"] = type.exclusiveMaximum


def typeToJSONDict(type, localTypePrefix):
    ret = {}
    if hasattr(type, "description") and type.description is not None:
        ret["description"] = type.description
    ret["type"] = _getTypeType(type)
    if isinstance(type, model.ComplexType):
        _initComplexTypeDict(type, ret, localTypePrefix)
    elif isinstance(type, model.DictionaryType):
        _initDictionaryTypeDict(type, ret, localTypePrefix)
    elif isinstance(type, model.ArrayType):
        _initArrayTypeDict(type, ret, localTypePrefix)
    elif isinstance(type, model.EnumType):
        _initEnumTypeDict(type, ret)
    elif isinstance(type, model.IntegerType):
        _initIntegerTypeDict(type, ret)
    elif isinstance(type, model.ObjectType):
        pass # nothing to do
    elif isinstance(type, model.NumberType):
        _initNumberTypeDict(type, ret)
    elif isinstance(type, model.BooleanType):
        _initBoolTypeDict(type, ret)
    elif isinstance(type, model.StringType):
        _initStringTypeDict(type, ret)
    elif isinstance(type, model.UuidType):
        _initUuidTypeDict(type, ret)
    elif isinstance(type, model.DateType):
        _initDateTypeDict(type, ret)
    elif isinstance(type, model.TimeType):
        _initTimeTypeDict(type, ret)
    elif isinstance(type, model.DateTimeType):
        _initDateTimeTypeDict(type, ret)
    elif isinstance(type, model.BytesType):
        _initBytesTypeDict(type, ret)
    return ret


class ReferenceHelper:
    def __init__(self):
        self.fileName = None
        self.type = None
        self.typeName = None
        self.topLevelType = False
