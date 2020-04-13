"""This file bundles all the functions use to build a model list from
parsed JSON/YAML dictionaries. The usage of this helper functions for
JSON and YAML schemas depends on the equality of parsed dictionaries
of JSON and YAML sources.
"""

import logging
import os.path
import json
import yaml

from yacg.model.model import Property
from yacg.util.stringUtils import toUpperCamelCase
from yacg.model.model import IntegerType, NumberType, BooleanType
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType, Tag


def getParsedSchemaFromJson(modelFile):
    """reads a JSON schema file in json format
    and returns the parsed dictionary from it

    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    with open(modelFile) as json_schema:
        return json.load(json_schema)


def getParsedSchemaFromYaml(modelFile):
    """reads a JSON schema file in yaml format
    and returns the parsed dictionary from it

    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    with open(modelFile) as json_schema:
        return yaml.load(json_schema, Loader=yaml.FullLoader)


def extractTypes(parsedSchema, modelFile, modelTypes):
    """extract the types from the parsed schema


    Keyword arguments:
    parsedSchema -- dictionary with the loaded schema
    modelFile -- file name and path to the model to load
    """

    schemaProperties = parsedSchema.get('properties', None)
    allOfEntry = parsedSchema.get('allOf', None)
    if (schemaProperties is not None) or (allOfEntry is not None):
        # extract top level type
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        description = parsedSchema.get('description', None)
        mainType = _extractObjectType(typeNameStr, schemaProperties, allOfEntry, description, modelTypes, modelFile)
        if len(mainType.tags) == 0:
            tags = parsedSchema.get('__tags', None)
            if tags is not None:
                mainType.tags = _extractTags(tags)

    schemaDefinitions = parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        _extractDefinitionsTypes(schemaDefinitions, modelTypes, modelFile, None)
    # there could be situations with circular type dependencies where are some
    # types not properly loaded ... so I search
    for type in modelTypes:
        if (hasattr(type, 'property')) and (len(type.properties) == 0):
            sourceFile = type.source
            parsedSchema = None
            if sourceFile.find('.json') != -1:
                # load a new model from a json file
                parsedSchema = getParsedSchemaFromJson(sourceFile)
            elif (sourceFile.find('.yaml') != -1) or (sourceFile.find('.yml') != -1):
                # load new model from a yaml file
                parsedSchema = getParsedSchemaFromYaml(sourceFile)
            # eiko
            _getTypeFromParsedSchema(parsedSchema, type.name, sourceFile, modelTypes)
    return modelTypes


def _extractTypeAndRelatedTypes(parsedSchema, desiredTypeName, modelFile, modelTypes):
    """extract the types from the parsed schema

    Keyword arguments:
    parsedSchema -- dictionary with the loaded schema
    desiredTypeName -- name of the type that should be loaded
    modelFile -- file name and path to the model to load
    """

    schemaProperties = parsedSchema.get('properties', None)
    allOfEntry = parsedSchema.get('allOf', None)
    if (schemaProperties is not None) or (allOfEntry is not None):
        # extract top level type
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        if typeNameStr == desiredTypeName:
            description = parsedSchema.get('description', None)
            type = _extractObjectType(typeNameStr, schemaProperties, allOfEntry, description, modelTypes, modelFile)
            if len(type.tags) == 0:
                tags = parsedSchema.get('__tags', None)
                if tags is not None:
                    type.tags = _extractTags(tags)

    schemaDefinitions = parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        _extractDefinitionsTypes(schemaDefinitions, modelTypes, modelFile, desiredTypeName)
    return modelTypes


def _extractDefinitionsTypes(definitions, modelTypes, modelFile, desiredTypeName):
    """build types from definitions section

    Keyword arguments:
    definitions -- dict of a schema definitions-block
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    for key in definitions.keys():
        if (desiredTypeName is not None) and (key != desiredTypeName):
            continue
        object = definitions[key]
        properties = object.get('properties', None)
        allOfEntry = object.get('allOf', None)
        description = object.get('description', None)
        type = _extractObjectType(key, properties, allOfEntry, description, modelTypes, modelFile)
        if len(type.tags) == 0:
            tags = object.get('__tags', None)
            if tags is not None:
                type.tags = _extractTags(tags)


def _extractObjectType(typeNameStr, properties, allOfEntries, description, modelTypes, modelFile):
    """build a type object

    Keyword arguments:
    typeNameStr -- Name of the new type
    properties -- dict of a schema properties-block
    allOfEntries -- dict of allOf block
    description -- optional description of that type
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    # check up that no dummy for this type is already created.
    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(typeNameStr, modelTypes, modelFile)
    # This can be the case in situations where attributes refer to another complex type
    newType = None
    if alreadyCreatedType is None:
        newType = ComplexType()
        newType.name = typeNameStr
    else:
        newType = alreadyCreatedType
    newType.source = modelFile
    if description is not None:
        newType.description = description
    if alreadyCreatedType is None:
        modelTypes.append(newType)
    if allOfEntries is not None:
        for allOfEntry in allOfEntries:
            refEntry = allOfEntry.get('$ref', None)
            propertiesEntry = allOfEntry.get('properties', None)
            if (propertiesEntry is not None):
                _extractAttributes(newType, propertiesEntry, modelTypes, modelFile)
            elif refEntry is not None:
                # TODO extract reference to the base class
                # TODO load external file and set
                newType.extendsType = _extractReferenceType(newType, refEntry, modelTypes, modelFile)
    if (hasattr(newType, 'properties')) and (len(newType.properties) == 0):
        _extractAttributes(newType, properties, modelTypes, modelFile)
    return newType


def _getAlreadyCreatedTypesWithThatName(typeNameStr, modelTypes, modelFile):
    """searches in the modelTypes list for a already created Type with that Name
    and return it if found

    Keyword arguments:
    typeNameStr -- Name of the new type
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    for alreadyCreatedType in modelTypes:
        if alreadyCreatedType.name == typeNameStr and alreadyCreatedType.source == modelFile:
            return alreadyCreatedType
    return None


def _extractAttributes(type, properties, modelTypes, modelFile):
    """extract the attributes of a type from the parsed model file

    Keyword arguments:
    type -- type that contains the properties
    properties -- dict of a schema properties-block
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    if properties is None:
        return
    for key in properties.keys():
        propDict = properties[key]
        propName = key
        description = propDict.get('description', None)
        newProperty = Property()
        newProperty.name = propName
        if description is not None:
            newProperty.description = description
        newProperty.type = _extractAttribType(type, newProperty, propDict, modelTypes, modelFile)
        tags = propDict.get('__tags', None)
        if tags is not None:
            newProperty.tags = _extractTags(tags)
        type.properties.append(newProperty)


def _extractAttribType(newType, newProperty, propDict, modelTypes, modelFile):
    """extract the type from the parsed model file and
    returns the type of the property.

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    type = propDict.get('type', None)
    if type == 'integer':
        return IntegerType()
    elif type == 'number':
        return NumberType()
    elif type == 'boolean':
        return BooleanType()
    elif type == 'string':
        # DateType, DateTimeType, StringType, EnumType
        return _extractStringType(newType, newProperty, propDict, modelTypes, modelFile)
    elif type == 'object':
        return _extractComplexType(newType, newProperty, propDict, modelTypes, modelFile)
    else:
        refEntry = propDict.get('$ref', None)
        enumEntry = propDict.get('enum', None)
        if enumEntry is not None:
            return _extractEnumType(newType, newProperty, enumEntry, modelTypes, modelFile)
        elif refEntry is not None:
            return _extractReferenceType(newType, refEntry, modelTypes, modelFile)
        elif type == 'array':
            return _extractArrayType(newType, newProperty, propDict, modelTypes, modelFile)
        else:
            logging.error(
                "modelFile: %s, type=%s, property=%s: unknown property type: %s" %
                (modelFile, newType.name, newProperty.name, type))
            return None


def _extractArrayType(newType, newProperty, propDict, modelTypes, modelFile):
    """build array type reference
    and return it

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """
    itemsDict = propDict.get('items', None)
    if itemsDict is not None:
        newProperty.isArray = True
        return _extractAttribType(newType, newProperty, itemsDict, modelTypes, modelFile)

    # TODO
    pass


def _extractReferenceType(newType, refEntry, modelTypes, modelFile):
    """build or reload a type reference
    and return it

    Keyword arguments:
    newType -- current Type
    refEntry -- $ref entry from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    localDefinitionsStr = '#/definitions/'
    if refEntry.startswith(localDefinitionsStr):
        # internal reference
        typeName = refEntry[len(localDefinitionsStr):]
        return _extractInternalReferenceType(newType, typeName, modelTypes, modelFile)
    else:
        if refEntry.find('.json') != -1:
            # load a new model from a json file
            return _extractExternalReferenceTypeFromJson(refEntry, modelTypes, modelFile)
        elif (refEntry.find('.yaml') != -1) or (refEntry.find('.yml') != -1):
            # load new model from a yaml file
            return _extractExternalReferenceTypeFromYaml(refEntry, modelTypes, modelFile)
        else:
            logging.error(
                "external reference from unknown type: %s, type=%s" %
                (refEntry, newType.name))
    pass


def _extractFileNameFromRefEntry(refEntry, fileExt):
    startPosOfFileExt = refEntry.find(fileExt)
    endPosOfFileName = startPosOfFileExt + len(fileExt)
    return refEntry[:endPosOfFileName]


def _extractDesiredTypeNameFromRefEntry(refEntry, fileName):
    fileNameLen = len(fileName)
    if len(refEntry) == fileNameLen:
        # e.g.: "$ref": "../aFile.json"
        return None
    lastSlash = refEntry.rfind('/', fileNameLen)
    return refEntry[lastSlash + 1:]


def _extractExternalReferenceTypeFromJson(refEntry, modelTypes, originModelFile):
    """load a reference type from an external JSON file. Before loading
    it is checked up, that the type isn't already loaded.
    The new created or already loaded type is returned.

    Keyword arguments:
    refEntry -- content of the $ref entry in the schema
    modelTypes -- list of already loaded models
    originModelFile -- file name and path to the model to load
    """

    fileName = _extractFileNameFromRefEntry(refEntry, '.json')
    desiredTypeName = _extractDesiredTypeNameFromRefEntry(refEntry, fileName)
    alreadyLoadedType = _getTypeIfAlreadyLoaded(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    if not os.path.isfile(fileName):
        # maybe the path is relative to the current type file
        originPathLength = originModelFile.rfind('/')
        originPath = originModelFile[:originPathLength + 1]
        fileName = originPath + fileName
        if not os.path.isfile(fileName):
            logging.error(
                "can't find external model file: modelFile=%s, refStr=%s, desiredFile=%s"
                % (originModelFile, refEntry, fileName))
            return None
        fileName = os.path.abspath(fileName)
    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    parsedSchema = getParsedSchemaFromJson(fileName)
    return _getTypeFromParsedSchema(parsedSchema, desiredTypeName, fileName, modelTypes)
    # TODO


def _extractExternalReferenceTypeFromYaml(refEntry, modelTypes, originModelFile):
    """load a reference type from an external YAML file. Before loading
    it is checked up, that the type isn't already loaded.
    The new created or already loaded type is returned.

    Keyword arguments:
    refEntry -- content of the $ref entry in the schema
    modelTypes -- list of already loaded models
    originModelFile -- file name and path to the model to load
    """

    fileExt = '.yaml' if refEntry.find('.yaml') != -1 else '.yml'
    fileName = _extractFileNameFromRefEntry(refEntry, fileExt)
    desiredTypeName = _extractDesiredTypeNameFromRefEntry(refEntry, fileName)
    alreadyLoadedType = _getTypeIfAlreadyLoaded(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    if not os.path.isfile(fileName):
        # maybe the path is relative to the current type file
        originPathLength = originModelFile.rfind('/')
        originPath = originModelFile[:originPathLength + 1]
        fileName = originPath + fileName
        if not os.path.isfile(fileName):
            logging.error(
                "can't find external model file: modelFile=%s, refStr=%s, desiredFile=%s"
                % (originModelFile, refEntry, fileName))
            return None
    # to handle circular dependencies
    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    parsedSchema = getParsedSchemaFromYaml(fileName)
    return _getTypeFromParsedSchema(parsedSchema, desiredTypeName, fileName, modelTypes)


def _getTypeFromParsedSchema(parsedSchema, desiredTypeName, fileName, modelTypes):
    """loads a desired type from a parsed schema
    and return it.
    The desired type and all over attributes related will be added to the
    list of the current loaded types.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    parsedSchema -- dictionary of the parsed schema
    desiredTypeName -- name of the type to look for
    fileName -- file where the type is loaded from
    modelTypes -- list of already loaded models
    """

    newModelTypes = _extractTypeAndRelatedTypes(parsedSchema, desiredTypeName, fileName, modelTypes)
    desiredType = None
    for type in newModelTypes:
        if (type.name == desiredTypeName) and (type.source == fileName):
            desiredType = type
            break
    if desiredType is None:
        logging.error("can't find external type: desiredTypeName=%s, file=%s" % (desiredTypeName, fileName))
        return None
    # _putAllNewRelatedTypesToAlreadyLoadedTypes(desiredType,modelTypes)
    return desiredType


def _putAllNewRelatedTypesToAlreadyLoadedTypes(desiredType, alreadyLoadedModelTypes):
    """Search in new model types for all related types to the desired type and
    put them the already loaded model types.

    Keyword arguments:
    desiredType -- desired type
    alreadyLoadedModelTypes -- list with already loaded types
    """

    _appendToAlreadyLoadedTypes(desiredType, alreadyLoadedModelTypes)
    for property in desiredType.properties:
        if not property.type.isBaseType:
            _putAllNewRelatedTypesToAlreadyLoadedTypes(property.type, alreadyLoadedModelTypes)


def _getAlreadyLoadedType(typeName, typeSource, alreadyLoadedModelTypes):
    """Tests if the type is already contained in the list of
    loaded types. If that is the case it is returned.

    Keyword arguments:
    typeName -- name of the type to check up
    typeSource -- model file that contains that type
    alreadyLoadedModelTypes -- list with already loaded types
    """

    for type in alreadyLoadedModelTypes:
        if (typeName == type.name) and (typeSource == type.source):
            return type
    return None


def _appendToAlreadyLoadedTypes(newType, alreadyLoadedModelTypes):
    """Tests if the new type is already contained in the list of
    loaded types. If not then the new type is appended.

    Keyword arguments:
    newType -- new type that should be added
    alreadyLoadedModelTypes -- list with already loaded types
    """

    newTypeName = newType.name
    newTypeSource = newType.source
    for type in alreadyLoadedModelTypes:
        if (newTypeName == type.name) and (newTypeSource == type.source):
            return
    alreadyLoadedModelTypes.append(newType)


def _getTypeIfAlreadyLoaded(typeName, fileName, modelTypes):
    """builds or relaod a type reference in the current file
    and return it.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    typeName -- name of the type to look for
    fileName -- file where the type is loaded from
    modelTypes -- list of already loaded models
    """

    for type in modelTypes:
        if (type.name == typeName) and (fileName == type.source):
            return type
    return None


def _extractInternalReferenceType(newType, refTypeName, modelTypes, modelFile):
    """builds or relaod a type reference in the current file
    and return it.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    newType -- current Type
    refTypeName -- name of the referenced type
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(refTypeName, modelTypes, modelFile)
    if alreadyCreatedType is not None:
        return alreadyCreatedType
    dummyReference = ComplexType()
    dummyReference.name = refTypeName
    dummyReference.source = modelFile
    modelTypes.append(dummyReference)
    return dummyReference


def _extractComplexType(newType, newProperty, propDict, modelTypes, modelFile):
    """builds a new inner complex type for that property
    and return it

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    innerTypeName = toUpperCamelCase(newType.name + ' ' + newProperty.name)
    newInnerType = ComplexType()
    newInnerType.name = innerTypeName
    newInnerType.source = modelFile
    modelTypes.append(newInnerType)
    description = propDict.get('description', None)
    if description is not None:
        newInnerType.description = description
    tags = propDict.get('__tags', None)
    if tags is not None:
        newInnerType.tags = _extractTags(tags)
    properties = propDict.get('properties', None)
    if properties is not None:
        _extractAttributes(newInnerType, properties, modelTypes, modelFile)
    else:
        logging.error(
            "modelFile: %s, type=%s, property=%s: inner complex type without properties"
            % (modelFile, newType.name, newProperty.name))
    return newInnerType


def _extractStringType(newType, newProperty, propDict, modelTypes, modelFile):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    formatValue = propDict.get('format', None)
    enumValue = propDict.get('enum', None)
    if (formatValue is None) and (enumValue is None):
        return StringType()
    elif enumValue is not None:
        return _extractEnumType(newType, newProperty, enumValue, modelTypes, modelFile)
    elif formatValue == 'date':
        return DateType()
    elif formatValue == 'date-time':
        return DateTimeType()
    elif formatValue == 'uuid':
        return UuidType()
    else:
        # TODO logging
        logging.error(
            "modelFile: %s, type=%s, property=%s: unknown string type format: %s"
            % (modelFile, newType.name, newProperty.name, formatValue))
        return StringType()


def _extractEnumType(newType, newProperty, enumValue, modelTypes, modelFile):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    enumValues -- list with allowed values
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load
    """

    enumTypeName = toUpperCamelCase(newType.name + ' ' + newProperty.name + 'Enum')
    enumType = EnumType()
    enumType.name = enumTypeName
    enumType.values = enumValue
    enumType.source = modelFile
    modelTypes.append(enumType)
    return enumType


def _extractTags(tagArray):
    """extracts the tags attached to types or properties and returns them as
    list

    Keyword arguments:
    tagArray -- dictionary of models '__tags' entry
    """

    tags = []
    for tag in tagArray:
        if isinstance(tag, str):
            tagObj = Tag()
            tagObj.name = tag
            tags.append(tagObj)
        elif isinstance(tag, dict):
            keyArray = list(tag.keys())
            if len(keyArray) > 0:
                tagName = keyArray[0]
                tagValue = tag.get(tagName, None)
                tagObj = Tag()
                tagObj.name = tagName
                tagObj.value = tagValue
                tags.append(tagObj)
    return tags
