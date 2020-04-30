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


class ModelFileContainer:
    def __init__(self, fileName, parsedSchema):
        self.fileName = fileName
        self.parsedSchema = parsedSchema
        self.domain = parsedSchema.get('__domain', None)


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

    modelFileContainer = ModelFileContainer(modelFile, parsedSchema)
    schemaProperties = parsedSchema.get('properties', None)
    allOfEntry = parsedSchema.get('allOf', None)
    if (schemaProperties is not None) or (allOfEntry is not None):
        # extract top level type
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        description = parsedSchema.get('description', None)
        mainType = _extractObjectType(typeNameStr, schemaProperties, allOfEntry, description, modelTypes, modelFileContainer)
        if len(mainType.tags) == 0:
            tags = parsedSchema.get('__tags', None)
            if tags is not None:
                mainType.tags = _extractTags(tags)

    schemaDefinitions = parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        _extractDefinitionsTypes(schemaDefinitions, modelTypes, modelFileContainer, None)
    else:
        openApiComponents = parsedSchema.get('components', None)
        if openApiComponents is not None:
            schemas = openApiComponents.get('schemas', None)
            if schemas is not None:
                # extract types from extra components section (OpenApi v3)
                _extractDefinitionsTypes(schemas, modelTypes, modelFileContainer, None)

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
            modelFileContainer = ModelFileContainer(sourceFile, parsedSchema)
            _getTypeFromParsedSchema(modelFileContainer, type.name, modelTypes)
    return modelTypes


def _extractTypeAndRelatedTypes(modelFileContainer, desiredTypeName, modelTypes):
    """extract the types from the parsed schema

    Keyword arguments:
    modelFileContainer -- file name and path to the model to load
    desiredTypeName -- name of the type that should be loaded
    """

    schemaProperties = modelFileContainer.parsedSchema.get('properties', None)
    allOfEntry = modelFileContainer.parsedSchema.get('allOf', None)
    if (schemaProperties is not None) or (allOfEntry is not None):
        # extract top level type
        titleStr = modelFileContainer.parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        if typeNameStr == desiredTypeName:
            description = modelFileContainer.parsedSchema.get('description', None)
            type = _extractObjectType(typeNameStr, schemaProperties, allOfEntry, description, modelTypes, modelFileContainer)
            if len(type.tags) == 0:
                tags = modelFileContainer.parsedSchema.get('__tags', None)
                if tags is not None:
                    type.tags = _extractTags(tags)

    schemaDefinitions = modelFileContainer.parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        _extractDefinitionsTypes(schemaDefinitions, modelTypes, modelFileContainer, desiredTypeName)
    else:
        openApiComponents = modelFileContainer.parsedSchema.get('components', None)
        if openApiComponents is not None:
            schemas = openApiComponents.get('schemas', None)
            if schemas is not None:
                # extract types from extra components section (OpenApi v3)
                _extractDefinitionsTypes(openApiComponents, modelTypes, modelFileContainer, desiredTypeName)
    return modelTypes


def _extractDefinitionsTypes(definitions, modelTypes, modelFileContainer, desiredTypeName):
    """build types from definitions section

    Keyword arguments:
    definitions -- dict of a schema definitions-block
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load, instance of ModelFileContainer
    """

    for key in definitions.keys():
        if (desiredTypeName is not None) and (key != desiredTypeName):
            continue
        object = definitions[key]
        properties = object.get('properties', None)
        allOfEntry = object.get('allOf', None)
        description = object.get('description', None)
        type = _extractObjectType(key, properties, allOfEntry, description, modelTypes, modelFileContainer)
        if len(type.tags) == 0:
            tags = object.get('__tags', None)
            if tags is not None:
                type.tags = _extractTags(tags)


def _extractObjectType(typeNameStr, properties, allOfEntries, description, modelTypes, modelFileContainer):
    """build a type object

    Keyword arguments:
    typeNameStr -- Name of the new type
    properties -- dict of a schema properties-block
    allOfEntries -- dict of allOf block
    description -- optional description of that type
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load, instance of ModelFileContainer
    """

    # check up that no dummy for this type is already created.
    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(typeNameStr, modelTypes, modelFileContainer)
    # This can be the case in situations where attributes refer to another complex type
    newType = None
    if alreadyCreatedType is None:
        newType = ComplexType()
        newType.domain = modelFileContainer.domain
        newType.name = typeNameStr
    else:
        newType = alreadyCreatedType
    newType.source = modelFileContainer.fileName
    if description is not None:
        newType.description = description
    if alreadyCreatedType is None:
        modelTypes.append(newType)
    if allOfEntries is not None:
        for allOfEntry in allOfEntries:
            refEntry = allOfEntry.get('$ref', None)
            propertiesEntry = allOfEntry.get('properties', None)
            if (propertiesEntry is not None):
                _extractAttributes(newType, propertiesEntry, modelTypes, modelFileContainer)
            elif refEntry is not None:
                # TODO extract reference to the base class
                # TODO load external file and set
                newType.extendsType = _extractReferenceType(newType, refEntry, modelTypes, modelFileContainer)
    if (hasattr(newType, 'properties')) and (len(newType.properties) == 0):
        _extractAttributes(newType, properties, modelTypes, modelFileContainer)
    return newType


def _getAlreadyCreatedTypesWithThatName(typeNameStr, modelTypes, modelFileContainer):
    """searches in the modelTypes list for a already created Type with that Name
    and return it if found

    Keyword arguments:
    typeNameStr -- Name of the new type
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load, instance of ModelFileContainer
    """

    for alreadyCreatedType in modelTypes:
        if alreadyCreatedType.name == typeNameStr and alreadyCreatedType.source == modelFileContainer.fileName:
            return alreadyCreatedType
    return None


def _extractAttributes(type, properties, modelTypes, modelFileContainer):
    """extract the attributes of a type from the parsed model file

    Keyword arguments:
    type -- type that contains the properties
    properties -- dict of a schema properties-block
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and stuff, instance of ModelFileContainer
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
        newProperty.default = propDict.get('default', None)
        newProperty.type = _extractAttribType(type, newProperty, propDict, modelTypes, modelFileContainer)
        tags = propDict.get('__tags', None)
        if tags is not None:
            newProperty.tags = _extractTags(tags)
        type.properties.append(newProperty)


def _extractAttribType(newType, newProperty, propDict, modelTypes, modelFileContainer):
    """extract the type from the parsed model file and
    returns the type of the property.

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and stuff, instance of ModelFileContainer
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
        return _extractStringType(newType, newProperty, propDict, modelTypes, modelFileContainer)
    elif type == 'object':
        return _extractComplexType(newType, newProperty, propDict, modelTypes, modelFileContainer)
    else:
        refEntry = propDict.get('$ref', None)
        enumEntry = propDict.get('enum', None)
        if enumEntry is not None:
            return _extractEnumType(newType, newProperty, enumEntry, modelTypes, modelFileContainer)
        elif refEntry is not None:
            return _extractReferenceType(newType, refEntry, modelTypes, modelFileContainer)
        elif type == 'array':
            return _extractArrayType(newType, newProperty, propDict, modelTypes, modelFileContainer)
        else:
            logging.error(
                "modelFile: %s, type=%s, property=%s: unknown property type: %s" %
                (modelFileContainer.fileName, newType.name, newProperty.name, type))
            return None


def _extractArrayType(newType, newProperty, propDict, modelTypes, modelFileContainer):
    """build array type reference
    and return it

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """
    itemsDict = propDict.get('items', None)
    if itemsDict is not None:
        newProperty.isArray = True
        return _extractAttribType(newType, newProperty, itemsDict, modelTypes, modelFileContainer)

    # TODO
    pass


def _extractReferenceType(newType, refEntry, modelTypes, modelFileContainer):
    """build or reload a type reference
    and return it

    Keyword arguments:
    newType -- current Type
    refEntry -- $ref entry from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    localDefinitionsStr = '#/definitions/'
    openApiComponentsStr = '#/components/schemas/'
    if refEntry.startswith(localDefinitionsStr):
        # internal reference
        typeName = refEntry[len(localDefinitionsStr):]
        return _extractInternalReferenceType(newType, typeName, modelTypes, modelFileContainer)
    elif refEntry.startswith(openApiComponentsStr):
        # internal reference
        typeName = refEntry[len(openApiComponentsStr):]
        return _extractInternalReferenceType(newType, typeName, modelTypes, modelFileContainer)
    else:
        if refEntry.find('.json') != -1:
            # load a new model from a json file
            return _extractExternalReferenceTypeFromJson(refEntry, modelTypes, modelFileContainer)
        elif (refEntry.find('.yaml') != -1) or (refEntry.find('.yml') != -1):
            # load new model from a yaml file
            return _extractExternalReferenceTypeFromYaml(refEntry, modelTypes, modelFileContainer)
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


def _extractExternalReferenceTypeFromJson(refEntry, modelTypes, originModelFileContainer):
    """load a reference type from an external JSON file. Before loading
    it is checked up, that the type isn't already loaded.
    The new created or already loaded type is returned.

    Keyword arguments:
    refEntry -- content of the $ref entry in the schema
    modelTypes -- list of already loaded models
    originModelFileContainer -- file name and path to the model to load
    """

    fileName = _extractFileNameFromRefEntry(refEntry, '.json')
    desiredTypeName = _extractDesiredTypeNameFromRefEntry(refEntry, fileName)
    alreadyLoadedType = _getTypeIfAlreadyLoaded(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    if not os.path.isfile(fileName):
        # maybe the path is relative to the current type file
        originPathLength = originModelFileContainer.fileName.rfind('/')
        originPath = originModelFileContainer.fileName[:originPathLength + 1]
        fileName = originPath + fileName
        if not os.path.isfile(fileName):
            logging.error(
                "can't find external model file: modelFile=%s, refStr=%s, desiredFile=%s"
                % (originModelFileContainer.fileName, refEntry, fileName))
            return None
        fileName = os.path.abspath(fileName)
    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    parsedSchema = getParsedSchemaFromJson(fileName)
    modelFileContainer = ModelFileContainer(fileName, parsedSchema)
    return _getTypeFromParsedSchema(modelFileContainer, desiredTypeName, modelTypes)
    # TODO


def _extractExternalReferenceTypeFromYaml(refEntry, modelTypes, originModelFileContainer):
    """load a reference type from an external YAML file. Before loading
    it is checked up, that the type isn't already loaded.
    The new created or already loaded type is returned.

    Keyword arguments:
    refEntry -- content of the $ref entry in the schema
    modelTypes -- list of already loaded models
    originModelFileContainer -- file name and path to the model to load
    """

    fileExt = '.yaml' if refEntry.find('.yaml') != -1 else '.yml'
    fileName = _extractFileNameFromRefEntry(refEntry, fileExt)
    desiredTypeName = _extractDesiredTypeNameFromRefEntry(refEntry, fileName)
    alreadyLoadedType = _getTypeIfAlreadyLoaded(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    if not os.path.isfile(fileName):
        # maybe the path is relative to the current type file
        originPathLength = originModelFileContainer.fileName.rfind('/')
        originPath = originModelFileContainer.fileName[:originPathLength + 1]
        fileName = originPath + fileName
        if not os.path.isfile(fileName):
            logging.error(
                "can't find external model file: modelFile=%s, refStr=%s, desiredFile=%s"
                % (originModelFileContainer.fileName, refEntry, fileName))
            return None
    # to handle circular dependencies
    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    parsedSchema = getParsedSchemaFromYaml(fileName)
    modelFileContainer = ModelFileContainer(fileName, parsedSchema)
    return _getTypeFromParsedSchema(modelFileContainer, desiredTypeName, modelTypes)


def _getTypeFromParsedSchema(modelFileContainer, desiredTypeName, modelTypes):
    """loads a desired type from a parsed schema
    and return it.
    The desired type and all over attributes related will be added to the
    list of the current loaded types.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    modelFileContainer -- instance of ModelFileContainer to pass some data through the functions
    desiredTypeName -- name of the type to look for
    modelTypes -- list of already loaded models
    """

    newModelTypes = _extractTypeAndRelatedTypes(modelFileContainer, desiredTypeName, modelTypes)
    desiredType = None
    for type in newModelTypes:
        if (type.name == desiredTypeName) and (type.source == modelFileContainer.fileName):
            desiredType = type
            break
    if desiredType is None:
        logging.error("can't find external type: desiredTypeName=%s, file=%s" % (desiredTypeName, modelFileContainer.fileName))
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


def _extractInternalReferenceType(newType, refTypeName, modelTypes, modelFileContainer):
    """builds or relaod a type reference in the current file
    and return it.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    newType -- current Type
    refTypeName -- name of the referenced type
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(refTypeName, modelTypes, modelFileContainer)
    if alreadyCreatedType is not None:
        return alreadyCreatedType
    dummyReference = ComplexType()
    dummyReference.domain = modelFileContainer.domain
    dummyReference.name = refTypeName
    dummyReference.source = modelFileContainer.fileName
    modelTypes.append(dummyReference)
    return dummyReference


def _extractComplexType(newType, newProperty, propDict, modelTypes, modelFileContainer):
    """builds a new inner complex type for that property
    and return it

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    innerTypeName = toUpperCamelCase(newType.name + ' ' + newProperty.name)
    newInnerType = ComplexType()
    newInnerType.domain = modelFileContainer.domain
    newInnerType.name = innerTypeName
    newInnerType.source = modelFileContainer.fileName
    modelTypes.append(newInnerType)
    description = propDict.get('description', None)
    if description is not None:
        newInnerType.description = description
    tags = propDict.get('__tags', None)
    if tags is not None:
        newInnerType.tags = _extractTags(tags)
    properties = propDict.get('properties', None)
    if properties is not None:
        _extractAttributes(newInnerType, properties, modelTypes, modelFileContainer)
    else:
        logging.error(
            "modelFile: %s, type=%s, property=%s: inner complex type without properties"
            % (modelFileContainer.fileName, newType.name, newProperty.name))
    return newInnerType


def _extractStringType(newType, newProperty, propDict, modelTypes, modelFileContainer):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContaier -- file name and stuff, instance of ModelFileContainer
    """

    formatValue = propDict.get('format', None)
    enumValue = propDict.get('enum', None)
    if (formatValue is None) and (enumValue is None):
        return StringType()
    elif enumValue is not None:
        return _extractEnumType(newType, newProperty, enumValue, modelTypes, modelFileContainer)
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
            % (modelFileContainer.fileName, newType.name, newProperty.name, formatValue))
        return StringType()


def _extractEnumType(newType, newProperty, enumValue, modelTypes, modelFileContainer):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    enumValues -- list with allowed values
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    enumTypeName = toUpperCamelCase(newType.name + ' ' + newProperty.name + 'Enum')
    enumType = EnumType()
    enumType.domain = modelFileContainer.domain
    enumType.name = enumTypeName
    enumType.values = enumValue
    enumType.source = modelFileContainer.fileName
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
