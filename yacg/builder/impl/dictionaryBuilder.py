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
from yacg.model.model import StringType, UuidType, BytesType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType, Tag
from yacg.util.fileUtils import doesFileExist

import yacg.model.openapi as openapi


class ModelFileContainer:
    def __init__(self, fileName, parsedSchema):
        self.fileName = fileName
        self.parsedSchema = parsedSchema
        self.version = parsedSchema.get('version', None)
        self.domain = parsedSchema.get('x-domain', None)


def getParsedSchemaFromJson(model):
    """reads a JSON schema file in json format
    and returns the parsed dictionary from it

    Keyword arguments:
    model -- file name and path to the model to load or model content from stdin
    """

    if doesFileExist(model):
        # model is treaten as file to input
        with open(model) as json_schema:
            return json.load(json_schema)
    else:
        # model is treaten as string content to get parsed
        return json.loads(model)


def getParsedSchemaFromYaml(model):
    """reads a JSON schema file in yaml format
    and returns the parsed dictionary from it

    Keyword arguments:
    model -- file name and path to the model to load or model content from stdin
    """

    if doesFileExist(model):
        # model is treaten as file to input
        with open(model) as json_schema:
            return yaml.load(json_schema, Loader=yaml.FullLoader)
    else:
        # model is treaten as string content to get parsed
        return yaml.load(model, Loader=yaml.FullLoader)


def extractTypes(parsedSchema, modelFile, modelTypes, skipOpenApi=False):
    """extract the types from the parsed schema


    Keyword arguments:
    parsedSchema -- dictionary with the loaded schema
    modelFile -- file name and path to the model to load
    skipOpenApi -- if true, then openApi paths are not extracted for the model
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
            tags = parsedSchema.get('x-tags', None)
            if tags is not None:
                mainType.tags = _extractTags(tags)
        _markRequiredAttributes(mainType, parsedSchema.get('required', []))
    enumEntry = parsedSchema.get('enum', None)
    if enumEntry is not None:
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        mainType = _extractEnumType(typeNameStr, None, enumEntry, modelTypes, modelFileContainer)
        if len(mainType.tags) == 0:
            tags = parsedSchema.get('x-tags', None)
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
        if (hasattr(type, 'properties')) and (len(type.properties) == 0):
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

    # load additional types, e.g. openapi.PathType
    if not skipOpenApi:
        if (parsedSchema.get('openapi', None) is not None) or (parsedSchema.get('swagger', None) is not None):
            modelFileContainer = ModelFileContainer(modelFile, parsedSchema)
            extractOpenApiPathTypes(modelTypes, modelFileContainer)
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
        if titleStr is None:
            lastSlash = modelFileContainer.fileName.rfind('/')
            lastDot = modelFileContainer.fileName.rfind('.')
            lastSlash = lastSlash + 1
            titleStr = modelFileContainer.fileName[lastSlash: lastDot]
        typeNameStr = toUpperCamelCase(titleStr)
        if typeNameStr == desiredTypeName:
            description = modelFileContainer.parsedSchema.get('description', None)
            type = _extractObjectType(typeNameStr, schemaProperties, allOfEntry, description, modelTypes, modelFileContainer)
            if len(type.tags) == 0:
                tags = modelFileContainer.parsedSchema.get('x-tags', None)
                if tags is not None:
                    type.tags = _extractTags(tags)
            _markRequiredAttributes(type, modelFileContainer.parsedSchema.get('required', []))

    enumEntry = modelFileContainer.parsedSchema.get('enum', None)
    if enumEntry is not None:
        titleStr = modelFileContainer.parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        mainType = _extractEnumType(typeNameStr, None, enumEntry, modelTypes, modelFileContainer)
        if len(mainType.tags) == 0:
            tags = modelFileContainer.parsedSchema.get('x-tags', None)
            if tags is not None:
                mainType.tags = _extractTags(tags)

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

        enumEntry = object.get('enum', None)
        if enumEntry is not None:
            mainType = _extractEnumType(key, None, enumEntry, modelTypes, modelFileContainer)
            if len(mainType.tags) == 0:
                tags = modelFileContainer.parsedSchema.get('x-tags', None)
                if tags is not None:
                    mainType.tags = _extractTags(tags)
        else:
            type = _extractObjectType(key, properties, allOfEntry, description, modelTypes, modelFileContainer)
            if len(type.tags) == 0:
                tags = object.get('x-tags', None)
                if tags is not None:
                    type.tags = _extractTags(tags)
            _markRequiredAttributes(type, object.get('required', []))


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
        newType.version = modelFileContainer.version
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
                _markRequiredAttributes(type, allOfEntry.get('required', []))
            elif refEntry is not None:
                newType.extendsType = _extractReferenceType(refEntry, modelTypes, modelFileContainer)
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
        if not hasattr(alreadyCreatedType, 'name'):
            continue
        if (alreadyCreatedType.name == typeNameStr) and (alreadyCreatedType.source == modelFileContainer.fileName):
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
        newProperty.type = _extractAttribType(type.name, newProperty, propDict, modelTypes, modelFileContainer)
        if newProperty.type is not None:
            if hasattr(newProperty.type, 'default'):
                newProperty.type.default = propDict.get('default', None)
            if hasattr(newProperty.type, 'minimum'):
                newProperty.type.minimum = propDict.get('minimum', None)
            if hasattr(newProperty.type, 'exclusiveMinimum'):
                newProperty.type.exclusiveMinimum = propDict.get('exclusiveMinimum', None)
            if hasattr(newProperty.type, 'maximum'):
                newProperty.type.maximum = propDict.get('maximum', None)
            if hasattr(newProperty.type, 'exclusiveMaximum'):
                newProperty.type.exclusiveMaximum = propDict.get('exclusiveMaximum', None)

        newProperty.isKey = propDict.get('x-key', False)
        newProperty.isVisualKey = propDict.get('x-visualKey', False)
        implicitRefEntry = propDict.get('x-ref', None)
        if implicitRefEntry is not None:
            newProperty.foreignKey = _extractReferenceType(implicitRefEntry, modelTypes, modelFileContainer)
        tags = propDict.get('x-tags', None)
        if tags is not None:
            newProperty.tags = _extractTags(tags)
        newProperty.ordinal = propDict.get('x-ordinal', None)

        type.properties.append(newProperty)


def _extractAttribType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer):
    """extract the type from the parsed model file and
    returns the type of the property.

    Keyword arguments:
    newTypeName -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and stuff, instance of ModelFileContainer
    """

    newProperty.format = propDict.get('format', None)
    type = propDict.get('type', None)
    if type == 'integer':
        return IntegerType()
    elif type == 'number':
        return NumberType()
    elif type == 'boolean':
        return BooleanType()
    elif type == 'string':
        # DateType, DateTimeType, StringType, EnumType
        return _extractStringType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer)
    elif type == 'object':
        return _extractComplexType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer)
    else:
        refEntry = propDict.get('$ref', None)
        enumEntry = propDict.get('enum', None)
        if enumEntry is not None:
            return _extractEnumType(newTypeName, newProperty, enumEntry, modelTypes, modelFileContainer)
        elif refEntry is not None:
            return _extractReferenceType(refEntry, modelTypes, modelFileContainer)
        elif type == 'array':
            return _extractArrayType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer)
        else:
            logging.error(
                "modelFile: %s, type=%s, property=%s: unknown property type: %s" %
                (modelFileContainer.fileName, newTypeName, newProperty.name, type))
            return None


def _extractArrayType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer):
    """build array type reference
    and return it

    Keyword arguments:
    newTypeName -- current type name
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """
    itemsDict = propDict.get('items', None)
    if itemsDict is not None:
        newProperty.arrayMinItems = propDict.get('minItems', None)
        newProperty.arrayMaxItems = propDict.get('maxItems', None)
        newProperty.arrayUniqueItems = propDict.get('uniqueItems', None)
        newProperty.isArray = True
        return _extractAttribType(newTypeName, newProperty, itemsDict, modelTypes, modelFileContainer)
    # TODO
    pass


def _extractReferenceType(refEntry, modelTypes, modelFileContainer):
    """build or reload a type reference
    and return it

    Keyword arguments:
    refEntry -- $ref entry from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    localDefinitionsStr = '#/definitions/'
    openApiComponentsStr = '#/components/schemas/'
    if refEntry.startswith(localDefinitionsStr):
        # internal reference
        typeName = refEntry[len(localDefinitionsStr):]
        return _extractInternalReferenceType(typeName, modelTypes, modelFileContainer)
    elif refEntry.startswith(openApiComponentsStr):
        # internal reference
        typeName = refEntry[len(openApiComponentsStr):]
        return _extractInternalReferenceType(typeName, modelTypes, modelFileContainer)
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
                (refEntry))
    pass


def _extractFileNameFromRefEntry(refEntry, fileExt):
    startPosOfFileExt = refEntry.find(fileExt)
    endPosOfFileName = startPosOfFileExt + len(fileExt)
    return refEntry[:endPosOfFileName]


def _extractDesiredTypeNameFromRefEntry(refEntry, fileName, fullPathToFile):
    fileNameLen = len(fileName)
    if len(refEntry) == fileNameLen:
        # e.g.: "$ref": "../aFile.json"
        # in cases where the referenced type is the top-level type of a schema
        parsedSchema = None
        if fileName.find('.json') != -1:
            # load a new model from a json file
            parsedSchema = getParsedSchemaFromJson(fullPathToFile)
        elif (fileName.find('.yaml') != -1) or (fileName.find('.yml') != -1):
            # load new model from a yaml file
            parsedSchema = getParsedSchemaFromYaml(fullPathToFile)
        else:
            return None
        titleStr = parsedSchema.get('title', None)
        if titleStr is None:
            lastSlash = fileName.rfind('/')
            lastSlash = lastSlash + 1
            lastDot = fileName.rfind('.')
            titleStr = fileName[lastSlash:lastDot]
        return toUpperCamelCase(titleStr)
    else:
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

    refEntryFileName = _extractFileNameFromRefEntry(refEntry, '.json')
    fileName = refEntryFileName
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

    desiredTypeName = _extractDesiredTypeNameFromRefEntry(refEntry, refEntryFileName, fileName)
    alreadyLoadedType = _getTypeIfAlreadyLoaded(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
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

    refEntryFileName = _extractFileNameFromRefEntry(refEntry, '.json')
    fileName = refEntryFileName
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

    desiredTypeName = _extractDesiredTypeNameFromRefEntry(refEntry, refEntryFileName, fileName)

    alreadyLoadedType = _getTypeIfAlreadyLoaded(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
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


def _extractInternalReferenceType(refTypeName, modelTypes, modelFileContainer):
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
    dummyReference.version = modelFileContainer.version
    modelTypes.append(dummyReference)
    return dummyReference


def _extractComplexType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer):
    """builds a new inner complex type for that property
    and return it

    Keyword arguments:
    newTypeName -- current type name
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    innerTypeName = toUpperCamelCase(newTypeName + ' ' + newProperty.name)
    newInnerType = ComplexType()
    newInnerType.domain = modelFileContainer.domain
    newInnerType.name = innerTypeName
    newInnerType.source = modelFileContainer.fileName
    newInnerType.version = modelFileContainer.version
    modelTypes.append(newInnerType)
    description = propDict.get('description', None)
    if description is not None:
        newInnerType.description = description
    tags = propDict.get('x-tags', None)
    if tags is not None:
        newInnerType.tags = _extractTags(tags)
    properties = propDict.get('properties', None)
    if properties is not None:
        _extractAttributes(newInnerType, properties, modelTypes, modelFileContainer)
        _markRequiredAttributes(newInnerType, propDict.get('required', []))
    else:
        logging.error(
            "modelFile: %s, type=%s, property=%s: inner complex type without properties"
            % (modelFileContainer.fileName, newTypeName, newProperty.name))
    return newInnerType


def _markRequiredAttributes(type, requiredArray):
    """interate over the requiredArray and mark all matching attributes
    in the properties type.

    Keyword arguments:
    type -- type object with the properties to check
    requiredArray -- string array with the names of the required attributes
    """

    for required in requiredArray:
        for prop in type.properties:
            if prop.name == required:
                prop.required = True
                break


def _extractStringType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current type name
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and stuff, instance of ModelFileContainer
    """

    formatValue = propDict.get('format', None)
    enumValue = propDict.get('enum', None)
    if (formatValue is None) and (enumValue is None):
        return StringType()
    elif enumValue is not None:
        return _extractEnumType(newTypeName, newProperty, enumValue, modelTypes, modelFileContainer)
    elif formatValue == 'date':
        return DateType()
    elif formatValue == 'date-time':
        return DateTimeType()
    elif formatValue == 'uuid':
        return UuidType()
    elif formatValue == 'byte':
        return BytesType()
    else:
        # TODO logging
        logging.error(
            "modelFile: %s, type=%s, property=%s: unknown string type format: %s"
            % (modelFileContainer.fileName, newTypeName, newProperty.name, formatValue))
        return StringType()


def _extractEnumType(newTypeName, newProperty, enumValue, modelTypes, modelFileContainer):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current type name
    newProperty -- current property
    enumValues -- list with allowed values
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    """

    enumTypeName = None
    if newProperty is not None:
        enumTypeName = toUpperCamelCase(newTypeName + ' ' + newProperty.name + 'Enum')
    else:
        enumTypeName = toUpperCamelCase(newTypeName)
    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(enumTypeName, modelTypes, modelFileContainer)
    if alreadyCreatedType is not None:
        if isinstance(alreadyCreatedType, EnumType):
            # the enum type is already created
            return alreadyCreatedType
        else:
            # a dummy type was pre-created. now it has been filled with the real values
            pass
    enumType = EnumType()
    enumType.domain = modelFileContainer.domain
    enumType.name = enumTypeName
    enumType.values = enumValue
    enumType.source = modelFileContainer.fileName
    enumType.version = modelFileContainer.version
    if alreadyCreatedType is not None:
        _replaceAllCurrentAppearencesOfAlreadyCreatedType(alreadyCreatedType, enumType, modelTypes)
    else:
        modelTypes.append(enumType)
    return enumType


def _replaceAllCurrentAppearencesOfAlreadyCreatedType(alreadyCreatedType, enumType, modelTypes):
    for n, type in enumerate(modelTypes):
        if type == alreadyCreatedType:
            modelTypes[n] = enumType
        elif isinstance(type, ComplexType):
            for property in type.properties:
                if property.type == alreadyCreatedType:
                    property.type = enumType


def _extractTags(tagArray):
    """extracts the tags attached to types or properties and returns them as
    list

    Keyword arguments:
    tagArray -- dictionary of models 'x-tags' entry
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


def extractOpenApiPathTypes(modelTypes, modelFileContainer):
    pathDict = modelFileContainer.parsedSchema.get('paths', None)
    if pathDict is None:
        return
    for pathKey in pathDict:
        pathType = openapi.PathType()
        pathType.pathPattern = pathKey
        commandDict = pathDict[pathKey]
        _extractOpenApiCommandsForPath(pathType, commandDict, modelTypes, modelFileContainer)
        modelTypes.append(pathType)


def _extractOpenApiCommandsForPath(pathType, commandsDict, modelTypes, modelFileContainer):
    for commandKey in commandsDict:
        commandDict = commandsDict[commandKey]
        command = openapi.Command()
        command.command = openapi.CommandCommandEnum.valueForString(commandKey)
        command.description = commandDict.get('description', None)
        command.summary = commandDict.get('summary', None)
        command.operationId = commandDict.get('operationId', None)
        command.tags = commandDict.get('tags', [])
        __extractOpenApiCommandParameters(command, commandDict.get('parameters', {}), modelTypes, modelFileContainer)
        __extractOpenApiRequestBody(command, commandDict.get('requestBody', None), modelTypes, modelFileContainer)
        __extractOpenApiCommandResponses(command, commandDict.get('responses', {}), modelTypes, modelFileContainer)
        __extractOpenApiCommandSecurity(command, commandDict.get('x-security', {}), modelTypes, modelFileContainer)
        pathType.commands.append(command)


def __extractOpenApiCommandSecurity(command, securityDict, modelTypes, modelFileContainer):
    scopes = securityDict.get("scopes", None)
    if scopes is None:
        return
    command.security = openapi.CommandSecurity()
    for scope in scopes:
        command.security.scopes.append(scope)


def __extractOpenApiRequestBody(command, requestBodyDict, modelTypes, modelFileContainer):
    if requestBodyDict is None:
        return
    requestBody = openapi.RequestBody()
    command.requestBody = requestBody
    requestBody.description = requestBodyDict.get('description', None)
    requestBody.required = requestBodyDict.get('required', None)
    contentDict = requestBodyDict.get('content', None)
    __extractOpenApiContentSectionAndAppend(contentDict, requestBody, modelTypes, modelFileContainer)


def __extractOpenApiContentSectionAndAppend(contentDict, contentHost, modelTypes, modelFileContainer):
    if contentDict is None:
        return
    for contentDictKey in contentDict.keys():
        content = contentDict[contentDictKey]
        contentEntry = openapi.ContentEntry()
        contentEntry.mimeType = contentDictKey
        schema = content.get('schema', None)
        __getTypeFromSchemaDictAndAsignId(schema, contentEntry, modelTypes, modelFileContainer)
        contentHost.content.append(contentEntry)


def __getTypeFromSchemaDictAndAsignId(schema, typeHost, modelTypes, modelFileContainer):
    if schema is None:
        return
    itemsEntry = schema.get("items", None)
    refEntry = None
    if (itemsEntry is not None):
        typeHost.isArray = True
        refEntry = itemsEntry.get('$ref', None)
    else:
        refEntry = schema.get('$ref', None)
    if refEntry is not None:
        typeHost.type = _extractReferenceType(refEntry, modelTypes, modelFileContainer)
    else:
        errorMsg = 'Missing refEntry for requestBody entry!'
        errorMsg2 = ' Attention, inner type declarations are currently not implemented for PathTypes.'
        logging.error(errorMsg + errorMsg2)


def __extractOpenApiCommandParameters(command, parametersList, modelTypes, modelFileContainer):
    for param in parametersList:
        originalInType = param.get('in', None)
        if originalInType == 'body':
            # swagger v2
            requestBody = openapi.RequestBody()
            command.requestBody = requestBody
            requestBody.description = param.get('description', None)
            requestBody.required = param.get('required', 'True')
            schema = param.get('schema', None)
            if schema is not None:
                contentEntry = openapi.ContentEntry()
                requestBody.content.append(contentEntry)
                __getTypeFromSchemaDictAndAsignId(schema, contentEntry, modelTypes, modelFileContainer)
        else:
            parameter = openapi.Parameter()
            command.parameters.append(parameter)
            parameter.inType = openapi.ParameterInTypeEnum.valueForString(originalInType)
            parameter.name = param.get('name', None)
            parameter.description = param.get('description', None)
            parameter.required = param.get('required', False)
            paramSchema = param.get('schema', None)
            paramType = param.get('type', None)
            if (paramSchema is None) and (paramType is None):
                logging.error(
                    "modelFile: %s, path=%s: missing schema or type entry" %
                    (modelFileContainer.fileName, command.path))
                continue
            if paramSchema is not None:
                parameter.type = _extractAttribType(
                    command.operationId.capitalize(),
                    parameter,
                    paramSchema,
                    modelTypes,
                    modelFileContainer)
            elif paramType is not None:
                parameter.type = _extractAttribType(
                    command.operationId.capitalize(),
                    parameter,
                    param,
                    modelTypes,
                    modelFileContainer)


def __extractOpenApiCommandResponses(command, responsesDict, modelTypes, modelFileContainer):
    if responsesDict is None:
        return
    for key in responsesDict.keys():
        responseDict = responsesDict[key]
        response = openapi.Response()
        command.responses.append(response)
        response.returnCode = key
        response.description = responseDict.get('description', None)
        contentDict = responseDict.get('content', None)
        if contentDict is not None:
            __extractOpenApiContentSectionAndAppend(contentDict, response, modelTypes, modelFileContainer)
        else:
            # swagger v2
            schema = responseDict.get('schema', None)
            if schema is not None:
                contentEntry = openapi.ContentEntry()
                response.content.append(contentEntry)
                __getTypeFromSchemaDictAndAsignId(schema, contentEntry, modelTypes, modelFileContainer)
