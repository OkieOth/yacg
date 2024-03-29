"""This file bundles all the functions use to build a model list from
parsed JSON/YAML dictionaries. The usage of this helper functions for
JSON and YAML schemas depends on the equality of parsed dictionaries
of JSON and YAML sources.
"""

import logging
import os.path
import string
import urllib.request
import json
import yaml

from yacg.model.model import ArrayConstraints, ForeignKey, Property
from yacg.util.stringUtils import toLowerCamelCase, toName, toUpperCamelCase, toUpperCamelCase
from yacg.model.model import IntegerType, NumberType, BooleanType, NumberTypeFormatEnum, IntegerTypeFormatEnum
from yacg.model.model import StringType, UuidType, BytesType, ObjectType
from yacg.model.model import DateType, TimeType, DateTimeType, DurationType, ArrayType
from yacg.model.model import EnumType, ComplexType, DictionaryType, Tag
from yacg.util.fileUtils import doesFileExist
from yacg.model.modelFuncs import isBaseType
import yacg.model.openapi as openapi
import yacg.model.asyncapi as asyncapi


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

    if __isHttpLoadableModel(model):
        with urllib.request.urlopen(model) as url:
            return json.loads(url.read().decode())
    elif doesFileExist(model):
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

    if __isHttpLoadableModel(model):
        with urllib.request.urlopen(model) as url:
            return yaml.loads(url.read().decode(), Loader=yaml.FullLoader)
    elif doesFileExist(model):
        # model is treaten as file to input
        with open(model) as json_schema:
            return yaml.load(json_schema, Loader=yaml.FullLoader)
    else:
        # model is treaten as string content to get parsed
        return yaml.load(model, Loader=yaml.FullLoader)


def __isHttpLoadableModel(model):
    return model.startswith("https://") or model.startswith("http://")


def __initProcessing(mainType, parsedSchema):
    mainType.processing = parsedSchema.get('x-processing', None)


def __initTags(mainType, parsedSchema):
    if len(mainType.tags) == 0:
        tags = parsedSchema.get('x-tags', None)
        if tags is not None:
            mainType.tags = _extractTags(tags)


def __initEnumValues(mainType, parsedSchema):
    if mainType.valuesMap is None:
        mainType.valuesMap = parsedSchema.get('x-enumValues', None)


def __extractTopLevelObjectType(parsedSchema, modelTypes, modelFileContainer, ignoreXRefTypes):
    schemaProperties = parsedSchema.get('properties', None)
    allOfEntry = parsedSchema.get('allOf', None)
    refEntry = parsedSchema.get('$ref', None)
    additionalProperties = __getAdditionalPropertiesForDictionaryType(parsedSchema)
    if (schemaProperties is not None) or (allOfEntry is not None) or (additionalProperties is not None):
        # extract top level type
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        description = parsedSchema.get('description', None)
        mainType = _extractObjectType(
            typeNameStr, schemaProperties, additionalProperties,
            allOfEntry, refEntry, description, modelTypes, modelFileContainer, True, ignoreXRefTypes)
        __initProcessing(mainType, parsedSchema)
        __initTags(mainType, parsedSchema)
        _markRequiredAttributes(mainType, parsedSchema.get('required', []))
        mainType.topLevelType = True
        return True
    return False


def __extractTopLevelEnumType(parsedSchema, modelTypes, modelFileContainer):
    enumEntry = parsedSchema.get('enum', None)
    if enumEntry is not None:
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        typeStr = parsedSchema.get('type', None)
        formatStr = parsedSchema.get('format', None)
        mainType = _extractEnumType(typeNameStr, None, enumEntry, typeStr, formatStr, modelTypes, modelFileContainer)
        __initProcessing(mainType, parsedSchema)
        __initTags(mainType, parsedSchema)
        __initEnumValues(mainType, parsedSchema)
        mainType.topLevelType = True
        return True
    return False


def __extractTopLevelEnumType(parsedSchema, modelTypes, modelFileContainer):
    enumEntry = parsedSchema.get('enum', None)
    if enumEntry is not None:
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        typeStr = parsedSchema.get('type', None)
        formatStr = parsedSchema.get('format', None)
        mainType = _extractEnumType(typeNameStr, None, enumEntry, typeStr, formatStr, modelTypes, modelFileContainer)
        __initProcessing(mainType, parsedSchema)
        __initTags(mainType, parsedSchema)
        __initEnumValues(mainType, parsedSchema)
        mainType.topLevelType = True
        return True
    return False


def __extractPureArrayType(typeName, parsedSchema, modelTypes, modelFileContainer, isTopLevelType, ignoreXRefTypes):
    if parsedSchema.get('items', None) is not None:
        typeNameStr = typeName
        tmpProperty = Property()
        arrayType = ArrayType()
        arrayType.name = typeNameStr
        arrayType.description = parsedSchema.get('description', None)
        arrayType.itemsType = _extractArrayType(typeNameStr, tmpProperty, parsedSchema, modelTypes, modelFileContainer, ignoreXRefTypes)
        arrayType.source = modelFileContainer.fileName
        arrayType.domain = modelFileContainer.domain
        arrayType.arrayConstraints = tmpProperty.arrayConstraints
        arrayType.arrayDimensions = tmpProperty.arrayDimensions
        arrayType.topLevelType = isTopLevelType

        _appendToAlreadyLoadedTypes(arrayType, modelTypes)
        __initProcessing(arrayType, parsedSchema)
        __initTags(arrayType, parsedSchema)
        return True
    return False


def extractTypes(parsedSchema, modelFile, modelTypes, skipAdditionalSpecTypes=False, ignoreXRefTypes = False):
    """extract the types from the parsed schema


    Keyword arguments:
    parsedSchema -- dictionary with the loaded schema
    modelFile -- file name and path to the model to load
    skipAdditionalSpecTypes -- if true, then openApi paths and asyncApi types are not extracted for the model
    """

    modelFileContainer = ModelFileContainer(modelFile, parsedSchema)
    handled = __extractTopLevelObjectType(parsedSchema, modelTypes, modelFileContainer, ignoreXRefTypes)
    if not handled:
        handled = __extractTopLevelEnumType(parsedSchema, modelTypes, modelFileContainer)
    if not handled:
        titleStr = parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr) if titleStr is not None else None
        handled = __extractPureArrayType(typeNameStr, parsedSchema, modelTypes, modelFileContainer, False, ignoreXRefTypes)

    schemaDefinitions = parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        _extractDefinitionsTypes(schemaDefinitions, modelTypes, modelFileContainer, None, ignoreXRefTypes)
    else:
        componentsDict = parsedSchema.get('components', None)
        if componentsDict is not None:
            schemas = componentsDict.get('schemas', None)
            if schemas is not None:
                # extract types from extra components section (OpenApi v3)
                _extractDefinitionsTypes(schemas, modelTypes, modelFileContainer, None, ignoreXRefTypes)
            if not skipAdditionalSpecTypes:
                _parseAsyncApiChannelParameters(modelTypes, componentsDict, None, modelFileContainer, 'componentsSection')
                _extractAsyncApiAmqpChannelBindings(componentsDict, modelTypes, modelFileContainer)
                _extractAsyncApiAmqpMessageBindings(componentsDict, modelTypes, modelFileContainer)
                _extractAsyncApiAmqpOperationBindings(componentsDict, modelTypes, modelFileContainer)

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
            _getTypeFromParsedSchema(modelFileContainer, type.name, modelTypes, ignoreXRefTypes)

    # fix missing foreign key property references
    for type in modelTypes:
        if (hasattr(type, 'properties')):
            for property in type.properties:
                if (property.foreignKey) and (property.foreignKey.propertyName) and (not property.foreignKey.property):
                    property.foreignKey.property = __getPropertyByName(property.foreignKey.type, property.foreignKey.propertyName)

    # load additional types, e.g. openapi.PathType
    if not skipAdditionalSpecTypes:
        if (parsedSchema.get('openapi', None) is not None) or (parsedSchema.get('swagger', None) is not None):
            modelFileContainer = ModelFileContainer(modelFile, parsedSchema)
            extractOpenApiInfo(modelTypes, modelFileContainer)
            extractOpenApiServer(modelTypes, modelFileContainer)
            extractOpenApiPathTypes(modelTypes, modelFileContainer)
        if parsedSchema.get('asyncapi', None):
            modelFileContainer = ModelFileContainer(modelFile, parsedSchema)
            extractAsyncApiTypes(modelTypes, modelFileContainer)
    return modelTypes


def extractOpenApiInfo(modelTypes, modelFileContainer):
    infoDict = modelFileContainer.parsedSchema.get('info', None)
    if infoDict is None:
        return
    infoObj = openapi.OpenApiInfo()
    __initInfoObj(infoObj, infoDict)
    modelTypes.append(infoObj)


def __initInfoObj(infoObj, infoDict):
    infoObj.description = infoDict.get("description", None)
    infoObj.license = infoDict.get("license", None)
    infoObj.title = infoDict.get("title", None)
    infoObj.version = infoDict.get("version", None)


def extractOpenApiServer(modelTypes, modelFileContainer):
    serverList = modelFileContainer.parsedSchema.get('servers', None)
    if serverList is None:
        return
    for serverDict in serverList:
        serverObj = openapi.OpenApiServer()
        serverObj.url = serverDict.get("url", "UNKNOWN_URL")
        serverObj.description = serverDict.get("description", None)
        modelTypes.append(serverObj)


def __getPropertyByName(type, propertyName):
    if hasattr(type, "properties"):
        for property in type.properties:
            if property.name == propertyName:
                return property
    return None


def _extractTypeAndRelatedTypes(modelFileContainer, desiredTypeName, modelTypes, ignoreXRefTypes):
    """extract the types from the parsed schema

    Keyword arguments:
    modelFileContainer -- file name and path to the model to load
    desiredTypeName -- name of the type that should be loaded
    """

    schemaProperties = modelFileContainer.parsedSchema.get('properties', None)
    allOfEntry = modelFileContainer.parsedSchema.get('allOf', None)
    refEntry = modelFileContainer.parsedSchema.get('$ref', None)
    additionalProperties = __getAdditionalPropertiesForDictionaryType(modelFileContainer.parsedSchema)
    if (schemaProperties is not None) or (allOfEntry is not None) or (additionalProperties is not None):
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
            type = _extractObjectType(
                typeNameStr, schemaProperties, additionalProperties,
                allOfEntry, refEntry, description, modelTypes, modelFileContainer, True, ignoreXRefTypes)
            type.topLevelType = True
            if len(type.tags) == 0:
                tags = modelFileContainer.parsedSchema.get('x-tags', None)
                if tags is not None:
                    type.tags = _extractTags(tags)
            _markRequiredAttributes(type, modelFileContainer.parsedSchema.get('required', []))

    enumEntry = modelFileContainer.parsedSchema.get('enum', None)
    if enumEntry is not None:
        titleStr = modelFileContainer.parsedSchema.get('title', None)
        typeNameStr = toUpperCamelCase(titleStr)
        typeStr = modelFileContainer.parsedSchema.get('type', None)
        formatStr = modelFileContainer.parsedSchema.get('format', None)
        mainType = _extractEnumType(typeNameStr, None, enumEntry, typeStr, formatStr, modelTypes, modelFileContainer)
        __initProcessing(mainType, modelFileContainer.parsedSchema)
        __initTags(mainType, modelFileContainer.parsedSchema)
        __initEnumValues(mainType, modelFileContainer.parsedSchema)

    schemaDefinitions = modelFileContainer.parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        _extractDefinitionsTypes(schemaDefinitions, modelTypes, modelFileContainer, desiredTypeName, ignoreXRefTypes)
    else:
        openApiComponents = modelFileContainer.parsedSchema.get('components', None)
        if openApiComponents is not None:
            schemas = openApiComponents.get('schemas', None)
            if schemas is not None:
                # extract types from extra components section (OpenApi v3)
                _extractDefinitionsTypes(openApiComponents, modelTypes, modelFileContainer, desiredTypeName, ignoreXRefTypes)
    return modelTypes


def _extractDefinitionsTypes(definitions, modelTypes, modelFileContainer, desiredTypeName, ignoreXRefTypes):
    """build types from definitions section

    Keyword arguments:
    definitions -- dict of a schema definitions-block
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load, instance of ModelFileContainer
    desiredTypeName -- type name to load
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    for key in definitions.keys():
        object = definitions[key]
        properties = object.get('properties', None)
        allOfEntry = object.get('allOf', None)
        additionalProperties = __getAdditionalPropertiesForDictionaryType(object)
        description = object.get('description', None)

        enumEntry = object.get('enum', None)
        if enumEntry is not None:
            typeStr = object.get('type', None)
            formatStr = object.get('format', None)
            mainType = _extractEnumType(key, None, enumEntry, typeStr, formatStr, modelTypes, modelFileContainer)
            __initProcessing(mainType, object)
            __initTags(mainType, object)
            __initEnumValues(mainType, object)
        else:
            itemsEntry = object.get('items', None)
            if itemsEntry is not None:
                __extractPureArrayType(key, object, modelTypes, modelFileContainer, True, ignoreXRefTypes)
            else:
                refEntry = object.get('$ref', None)
                type = _extractObjectType(
                    key, properties, additionalProperties, allOfEntry, refEntry,
                    description, modelTypes, modelFileContainer, True, ignoreXRefTypes)
                __initProcessing(type, object)
                if len(type.tags) == 0:
                    tags = object.get('x-tags', None)
                    if tags is not None:
                        type.tags = _extractTags(tags)
                _markRequiredAttributes(type, object.get('required', []))

    # search for additional top-level types, because some are not detected at first parse time
    for key in definitions.keys():
        t = _getAlreadyCreatedTypesWithThatName(key, modelTypes, modelFileContainer)
        if hasattr(t, "topLevelType"):
            t.topLevelType = True


def _extractObjectType(
        typeNameStr, properties, additionalProperties, allOfEntries, refEntry,
        description, modelTypes, modelFileContainer, isTopLevelType, ignoreXRefTypes):
    """build a type object

    Keyword arguments:
    typeNameStr -- Name of the new type
    properties -- dict of a schema properties-block
    additionalProperties -- dict of a schema additionalProperties-block
    allOfEntries -- dict of allOf block
    refEntryDict -- dict of '$ref' key
    description -- optional description of that type
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load, instance of ModelFileContainer
    isTopLevelType -- is no inner type
    ignoreXRefTypes -- if True x-ref entries will not followed
    """

    # check up that no dummy for this type is already created.
    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(typeNameStr, modelTypes, modelFileContainer)
    # This can be the case in situations where attributes refer to another complex type
    newType = None
    if alreadyCreatedType is None:
        newType = ComplexType() if additionalProperties is None else DictionaryType()
        newType.domain = modelFileContainer.domain
        newType.name = typeNameStr
        newType.version = modelFileContainer.version
    else:
        if (isinstance(alreadyCreatedType, DictionaryType) and alreadyCreatedType.valueType is not None) or (hasattr(alreadyCreatedType, "properties") and len(alreadyCreatedType.properties) > 0):
            return alreadyCreatedType
        else:
            newType = alreadyCreatedType
    newType.source = modelFileContainer.fileName
    if description is not None:
        newType.description = description

    if allOfEntries is not None:
        __handleAllOf(newType, allOfEntries, modelTypes, modelFileContainer, ignoreXRefTypes)
    else:
        if refEntry is not None:
            tmpType = _extractReferenceType(refEntry, modelTypes, modelFileContainer, ignoreXRefTypes)
            ret = None
            if isinstance(tmpType, EnumType):
                ret = EnumType(tmpType.__dict__)
            elif isinstance(tmpType, ArrayType):
                ret = ArrayType(tmpType.__dict__)
            elif isinstance(tmpType, DictionaryType):
                ret = DictionaryType(tmpType.__dict__)
            elif isinstance(tmpType, ComplexType):
                ret = ComplexType(vars(tmpType))
            if ret is not None:
                if isinstance(ret, ComplexType):
                    newType.extendsType = tmpType
                else:
                    ret.name = newType.name
                    _appendToAlreadyLoadedTypes(ret, modelTypes)
                    return ret

    _appendToAlreadyLoadedTypes(newType, modelTypes)
    if (hasattr(newType, 'properties')) and (len(newType.properties) == 0) and (hasattr(newType, 'extendsType')) and (newType.extendsType is None):
        _extractAttributes(newType, properties, modelTypes, modelFileContainer, ignoreXRefTypes)
    elif additionalProperties is not None:
        _extractDictionaryValueType(newType, additionalProperties, modelTypes, modelFileContainer, ignoreXRefTypes)
    newType.topLevelType = isTopLevelType
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


def _extractDictionaryValueType(type, additionalProperties, modelTypes, modelFileContainer, ignoreXRefTypes):
    """extract the attributes of a type from the parsed model file

    Keyword arguments:
    type -- type that contains the properties
    additionalProperties -- dict of a schema properties-block
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and stuff, instance of ModelFileContainer
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    if additionalProperties is None:
        return
    property = Property()
    property.name = ''
    type.valueType = _extractAttribType(type.name + "Value", property, additionalProperties, modelTypes, modelFileContainer, ignoreXRefTypes)
    if property.isArray:
        tmpArrayType = ArrayType()
        tmpArrayType.name = type.name + "InnerArray"
        tmpArrayType.description = additionalProperties.get('description', None)
        tmpArrayType.itemsType = type.valueType
        tmpArrayType.source = modelFileContainer.fileName
        tmpArrayType.domain = modelFileContainer.domain
        tmpArrayType.arrayConstraints = property.arrayConstraints
        tmpArrayType.arrayDimensions = property.arrayDimensions
        _appendToAlreadyLoadedTypes(tmpArrayType, modelTypes)
        __initTags(tmpArrayType, additionalProperties)
        type.valueType = tmpArrayType
    pass


def _extractAttributes(type, properties, modelTypes, modelFileContainer, ignoreXRefTypes):
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
        newProperty.type = _extractAttribType(type.name, newProperty, propDict, modelTypes, modelFileContainer, ignoreXRefTypes)
        if (newProperty.type is not None) and (not newProperty.isArray):
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
            if hasattr(newProperty.type, 'minLength'):
                newProperty.type.minLength = propDict.get('minLength', None)
            if hasattr(newProperty.type, 'maxLength'):
                newProperty.type.maxLength = propDict.get('maxLength', None)
            if hasattr(newProperty.type, 'pattern'):
                newProperty.type.pattern = propDict.get('pattern', None)

        newProperty.isKey = propDict.get('x-key', False)
        newProperty.isVisualKey = propDict.get('x-visualKey', False)
        implicitRefEntry = propDict.get('x-ref', None) if ignoreXRefTypes is False else None
        if implicitRefEntry is not None:
            # either {TYPE_NAME} or {TYPE_NAME}.{PROPERTY_NAME}
            propertyRefName = None
            lastDefSeparator = implicitRefEntry.find("#")
            if lastDefSeparator != -1:
                tmpStr = implicitRefEntry[lastDefSeparator + 1:]
                lastDot = tmpStr.find(".")
                if lastDot != -1:
                    implicitRefEntry = implicitRefEntry[0: lastDefSeparator + lastDot + 1]
                    propertyRefName = tmpStr[lastDot + 1:]
            newProperty.foreignKey = ForeignKey()
            newProperty.foreignKey.type = _extractReferenceType(implicitRefEntry, modelTypes, modelFileContainer, False)
            newProperty.foreignKey.propertyName = propertyRefName
        tags = propDict.get('x-tags', None)
        if tags is not None:
            newProperty.tags = _extractTags(tags)
        newProperty.ordinal = propDict.get('x-ordinal', None)
        newProperty.processing = propDict.get('x-processing', None)
        type.properties.append(newProperty)


def _extractAttribType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer, ignoreXRefTypes):
    """extract the type from the parsed model file and
    returns the type of the property.

    Keyword arguments:
    newTypeName -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and stuff, instance of ModelFileContainer
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    newProperty.format = propDict.get('format', None)
    type = propDict.get('type', None)
    if type == 'integer':
        ret = IntegerType()
        ret.format = IntegerTypeFormatEnum.valueForString(newProperty.format)
        return ret
    elif type == 'number':
        ret = NumberType()
        ret.format = NumberTypeFormatEnum.valueForString(newProperty.format)
        return ret
    elif type == 'boolean':
        return BooleanType()
    elif type == 'string':
        # DateType, TimeType, DateTimeType, StringType, EnumType, DurationType
        return _extractStringType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer)
    elif type == 'object':
        subProps = propDict.get('properties', None)
        subAllOf = propDict.get('allOf', None)
        subAdditionalProperties = __getAdditionalPropertiesForDictionaryType(propDict)
        if (subProps is None) and (subAllOf is None) and (subAdditionalProperties is None):
            return ObjectType()
        else:
            return _extractComplexType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer, ignoreXRefTypes)
    else:
        refEntry = propDict.get('$ref', None)
        enumEntry = propDict.get('enum', None)
        if enumEntry is not None:
            typeStr = propDict.get('type', None)
            formatStr = propDict.get('format', None)
            enumType = _extractEnumType(newTypeName, newProperty, enumEntry, typeStr, formatStr, modelTypes, modelFileContainer)
            __initProcessing(enumType, propDict)
            __initTags(enumType, propDict)
            __initEnumValues(enumType, propDict)
            return enumType
        elif refEntry is not None:
            tmp = _extractReferenceType(refEntry, modelTypes, modelFileContainer, ignoreXRefTypes)
            if isinstance(tmp, ArrayType):
                newProperty.isArray = True
                if hasattr(newProperty, 'arrayDimensions'):
                    newProperty.arrayDimensions = tmp.arrayDimensions
                if hasattr(newProperty, 'arrayConstraints'):
                    newProperty.arrayConstraints = tmp.arrayConstraints
                return tmp.itemsType
            else:
                return tmp
        elif type == 'array':
            arrayType = _extractArrayType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer, ignoreXRefTypes)
            itemsDict = propDict.get("items", None)
            if itemsDict is not None:
                if hasattr(arrayType, "default"):
                    arrayType.default = itemsDict.get('default', None)
                if hasattr(arrayType, "minimum"):
                    arrayType.minimum = itemsDict.get('minimum', None)
                if hasattr(arrayType, "maximum"):
                    arrayType.maximum = itemsDict.get('maximum', None)
                if hasattr(arrayType, "exclusiveMinimum"):
                    arrayType.exclusiveMinimum = itemsDict.get('exclusiveMinimum', None)
                if hasattr(arrayType, "exclusiveMaximum"):
                    arrayType.exclusiveMaximum = itemsDict.get('exclusiveMaximum', None)
                if hasattr(arrayType, "pattern"):
                    arrayType. pattern = itemsDict.get('pattern', None)

            # if hasattr(newProperty, 'arrayDimensions'):
            #     newProperty.arrayDimensions = len(newProperty.arrayConstraints)
            return arrayType
        else:
            logging.error(
                "modelFile: %s, type=%s, property=%s: unknown property type: %s" %
                (modelFileContainer.fileName, newTypeName, newProperty.name, type))
            return None


def _extractArrayType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer, ignoreXRefTypes):
    """build array type reference
    and return it

    Keyword arguments:
    newTypeName -- current type name
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    ignoreXRefTypes -- if True x-ref references are not followed
    """
    itemsDict = propDict.get('items', None)
    if itemsDict is not None:
        newProperty.isArray = True
        if hasattr(newProperty, "arrayConstraints"):
            arrayConstraints = ArrayConstraints()
            arrayConstraints.arrayMinItems = propDict.get('minItems', None)
            arrayConstraints.arrayMaxItems = propDict.get('maxItems', None)
            arrayConstraints.arrayUniqueItems = propDict.get('uniqueItems', False)
            newProperty.arrayConstraints.append(arrayConstraints)
            newProperty.arrayDimensions = len(newProperty.arrayConstraints)
        itemsType = itemsDict.get('type', None)
        itemsItemsDict = itemsDict.get('items', None)
        if (itemsType == "array") and (itemsItemsDict is not None):
            newProperty.arrayDimensions = len(newProperty.arrayConstraints)
            retType = _extractArrayType(newTypeName, newProperty, itemsDict, modelTypes, modelFileContainer, ignoreXRefTypes)
            return retType
        else:
            # there are situations where the attrib has a ref to an array type
            tmpProperty = Property()
            tmpProperty.name = newProperty.name
            retType = _extractAttribType(newTypeName, tmpProperty, itemsDict, modelTypes, modelFileContainer, ignoreXRefTypes)
            if tmpProperty.isArray:
                newProperty.arrayConstraints.extend(tmpProperty.arrayConstraints)
                newProperty.arrayDimensions = len(newProperty.arrayConstraints)
            return retType


def _extractReferenceType(refEntry, modelTypes, modelFileContainer, ignoreXRefTypes):
    """build or reload a type reference
    and return it

    Keyword arguments:
    refEntry -- $ref entry from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    localDefinitionsStr = '#/definitions/'
    openApiComponentsStr = '#/components/schemas/'
    if refEntry.startswith(localDefinitionsStr):
        # internal reference
        typeName = refEntry[len(localDefinitionsStr):]
        return _extractInternalReferenceType(typeName, modelTypes, modelFileContainer, ignoreXRefTypes)
    elif refEntry.startswith(openApiComponentsStr):
        # internal reference
        typeName = refEntry[len(openApiComponentsStr):]
        return _extractInternalReferenceType(typeName, modelTypes, modelFileContainer, ignoreXRefTypes)
    else:
        if refEntry.find('.json') != -1:
            # load a new model from a json file
            return _extractExternalReferenceTypeFromJson(refEntry, modelTypes, modelFileContainer, ignoreXRefTypes)
        elif (refEntry.find('.yaml') != -1) or (refEntry.find('.yml') != -1):
            # load new model from a yaml file
            return _extractExternalReferenceTypeFromYaml(refEntry, modelTypes, modelFileContainer, ignoreXRefTypes)
        else:
            logging.error(
                "external reference from unknown type: %s" %
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


def _extractExternalReferenceTypeFromJson(refEntry, modelTypes, originModelFileContainer, ignoreXRefTypes):
    """load a reference type from an external JSON file. Before loading
    it is checked up, that the type isn't already loaded.
    The new created or already loaded type is returned.

    Keyword arguments:
    refEntry -- content of the $ref entry in the schema
    modelTypes -- list of already loaded models
    originModelFileContainer -- file name and path to the model to load
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    refEntryFileName = _extractFileNameFromRefEntry(refEntry, '.json')
    fileName = refEntryFileName
    if (not __isHttpLoadableModel(fileName)) and (not os.path.isfile(fileName)):
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
    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    parsedSchema = getParsedSchemaFromJson(fileName)
    modelFileContainer = ModelFileContainer(fileName, parsedSchema)
    return _getTypeFromParsedSchema(modelFileContainer, desiredTypeName, modelTypes, ignoreXRefTypes)


def _extractExternalReferenceTypeFromYaml(refEntry, modelTypes, originModelFileContainer, ignoreXRefTypes):
    """load a reference type from an external YAML file. Before loading
    it is checked up, that the type isn't already loaded.
    The new created or already loaded type is returned.

    Keyword arguments:
    refEntry -- content of the $ref entry in the schema
    modelTypes -- list of already loaded models
    originModelFileContainer -- file name and path to the model to load
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    fileExt = '.yaml' if refEntry.find('.yaml') != -1 else '.yml'
    refEntryFileName = _extractFileNameFromRefEntry(refEntry, fileExt)
    fileName = refEntryFileName
    if (not __isHttpLoadableModel(fileName)) and (not os.path.isfile(fileName)):
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

    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    # to handle circular dependencies
    alreadyLoadedType = _getAlreadyLoadedType(desiredTypeName, fileName, modelTypes)
    if alreadyLoadedType is not None:
        return alreadyLoadedType
    parsedSchema = getParsedSchemaFromYaml(fileName)
    modelFileContainer = ModelFileContainer(fileName, parsedSchema)
    return _getTypeFromParsedSchema(modelFileContainer, desiredTypeName, modelTypes, ignoreXRefTypes)


def _getTypeFromParsedSchema(modelFileContainer, desiredTypeName, modelTypes, ignoreXRefTypes):
    """loads a desired type from a parsed schema
    and return it.
    The desired type and all over attributes related will be added to the
    list of the current loaded types.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    modelFileContainer -- instance of ModelFileContainer to pass some data through the functions
    desiredTypeName -- name of the type to look for
    modelTypes -- list of already loaded models
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    newModelTypes = _extractTypeAndRelatedTypes(modelFileContainer, desiredTypeName, modelTypes, ignoreXRefTypes)
    desiredType = None
    for type in newModelTypes:
        if not hasattr(type, "name"):
            continue
        if (type.name == desiredTypeName) and (type.source == modelFileContainer.fileName):
            desiredType = type
            break
    if desiredType is None:
        logging.error(
            "can't find external type: desiredTypeName=%s, file=%s" %
            (desiredTypeName, modelFileContainer.fileName))
        return None
    _putAllNewRelatedTypesToAlreadyLoadedTypes(desiredType, modelTypes)
    return desiredType


def _putAllNewRelatedTypesToAlreadyLoadedTypes(desiredType, alreadyLoadedModelTypes):
    """Search in new model types for all related types to the desired type and
    put them the already loaded model types.

    Keyword arguments:
    desiredType -- desired type
    alreadyLoadedModelTypes -- list with already loaded types
    """

    if not _appendToAlreadyLoadedTypes(desiredType, alreadyLoadedModelTypes):
        # type already exists
        return
    if not hasattr(desiredType, 'properties'):
        return
    for property in desiredType.properties:
        if not isBaseType(property.type):
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
        if not hasattr(type, "name"):
            continue
        if (typeName == type.name) and (typeSource == type.source):
            return type
    return None


def _appendToAlreadyLoadedTypes(newType, alreadyLoadedModelTypes):
    """Tests if the new type is already contained in the list of
    loaded types. If not then the new type is appended.
    Function returns True if the type was added and False
    in case that the type already exists.

    Keyword arguments:
    newType -- new type that should be added
    alreadyLoadedModelTypes -- list with already loaded types
    """

    if not hasattr(newType, "name"):
        alreadyLoadedModelTypes.append(newType)
        return True

    newTypeName = newType.name
    for type in alreadyLoadedModelTypes:
        if not hasattr(type, "name"):
            continue
        if (newTypeName == type.name):
            if hasattr(type, "source") and (newType.source != type.source):
                continue
            return False
    alreadyLoadedModelTypes.append(newType)
    return True


def _createDummyReference(definitions, refTypeName, parsedSchema, modelTypes, modelFileContainer, ignoreXRefTypes):
    if definitions is None:
        return ComplexType()
    for key in definitions.keys():
        if key != refTypeName:
            continue
        ret = None
        object = definitions[key]
        if object.get('properties', None) is not None:
            ret = ComplexType()
        if object.get('allOf', None) is not None:
            return ComplexType()
        if __getAdditionalPropertiesForDictionaryType(object) is not None:
            ret = DictionaryType()
        if object.get('enum', None) is not None:
            ret = EnumType()
        if ret is not None:
            #modelTypes.append(ret)
            return ret
        if object.get('items', None) is not None:
            tmpModelTypes = []
            if __extractPureArrayType(refTypeName, object, tmpModelTypes, modelFileContainer, False, ignoreXRefTypes):
                for t in tmpModelTypes:
                    if t.name == refTypeName:
                        #modelTypes.append(t)
                        return t
            return ArrayType()
    return ComplexType()


def _extractInternalReferenceType(refTypeName, modelTypes, modelFileContainer, ignoreXRefTypes):
    """builds or relaod a type reference in the current file
    and return it.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    newType -- current Type
    refTypeName -- name of the referenced type
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    ignoreXRefTypes -- if True x-ref references are not followed
    """

    alreadyCreatedType = _getAlreadyCreatedTypesWithThatName(refTypeName, modelTypes, modelFileContainer)
    if alreadyCreatedType is not None:
        return alreadyCreatedType

    schemaDefinitions = modelFileContainer.parsedSchema.get('definitions', None)
    if schemaDefinitions is not None:
        # extract types from extra definitions section
        dummyReference = _createDummyReference(schemaDefinitions, refTypeName, modelFileContainer.parsedSchema, modelTypes, modelFileContainer, ignoreXRefTypes)
    else:
        componentsDict = modelFileContainer.parsedSchema.get('components', None)
        if componentsDict is not None:
            schemas = componentsDict.get('schemas', None)
            if schemas is not None:
                # extract types from extra components section (OpenApi v3)
                dummyReference = _createDummyReference(schemaDefinitions, refTypeName, modelFileContainer.parsedSchema, modelTypes, modelFileContainer, ignoreXRefTypes)

    ## THIS doesn't work for ArrayTypes :-/
    # dummyReference = ComplexType()
    dummyReference.domain = modelFileContainer.domain
    dummyReference.name = refTypeName
    dummyReference.source = modelFileContainer.fileName
    dummyReference.version = modelFileContainer.version
    modelTypes.append(dummyReference)
    return dummyReference


def _extractComplexType(newTypeName, newProperty, propDict, modelTypes, modelFileContainer, ignoreXRefTypes):
    """builds a new inner complex type for that property
    and return it

    Keyword arguments:
    newTypeName -- current type name
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFileContainer -- file name and path to the model to load
    ignoreXRefTypes -- if True x-ref entries are not followed
    """

    propName = newProperty.name if newProperty.name is not None else "Inner"
    innerTypeName = toUpperCamelCase(newTypeName + ' ' + propName)

    properties = propDict.get('properties', None)
    additionalProperties = __getAdditionalPropertiesForDictionaryType(propDict)
    newInnerType = ComplexType() if additionalProperties is None else DictionaryType()
    newInnerType.domain = modelFileContainer.domain

    newInnerType.name = innerTypeName
    newInnerType.source = modelFileContainer.fileName
    newInnerType.version = modelFileContainer.version
    _appendToAlreadyLoadedTypes(newInnerType, modelTypes)
    description = propDict.get('description', None)
    if description is not None:
        newInnerType.description = description
    tags = propDict.get('x-tags', None)
    if tags is not None:
        newInnerType.tags = _extractTags(tags)
    if properties is not None:
        _extractAttributes(newInnerType, properties, modelTypes, modelFileContainer, ignoreXRefTypes)
        _markRequiredAttributes(newInnerType, propDict.get('required', []))
    else:
        if additionalProperties is not None:
            _extractDictionaryValueType(newInnerType, additionalProperties, modelTypes, modelFileContainer, ignoreXRefTypes)
        else:
            allOfEntries = propDict.get("allOf", None)
            if allOfEntries is not None:
                __handleAllOf(newInnerType, allOfEntries, modelTypes, modelFileContainer, ignoreXRefTypes)
            else:
                logging.error(
                    "modelFile: %s, type=%s, property=%s: inner complex type without properties"
                    % (modelFileContainer.fileName, newTypeName, newProperty.name))
    return newInnerType


def __handleAllOf(newType, allOfEntries, modelTypes, modelFileContainer, ignoreXRefTypes):
    for allOfEntry in allOfEntries:
        tmpRefEntry = allOfEntry.get('$ref', None)
        propertiesEntry = allOfEntry.get('properties', None)
        if (propertiesEntry is not None):
            _extractAttributes(newType, propertiesEntry, modelTypes, modelFileContainer, ignoreXRefTypes)
            _markRequiredAttributes(type, allOfEntry.get('required', []))
        elif tmpRefEntry is not None:
            newType.extendsType = _extractReferenceType(tmpRefEntry, modelTypes, modelFileContainer, ignoreXRefTypes)


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
        typeStr = propDict.get('type', None)
        formatStr = propDict.get('format', None)
        enumType = _extractEnumType(newTypeName, newProperty, enumValue, typeStr, formatStr, modelTypes, modelFileContainer)
        __initProcessing(enumType, propDict)
        __initTags(enumType, propDict)
        __initEnumValues(enumType, propDict)
        return enumType
    elif formatValue == 'date':
        return DateType()
    elif formatValue == 'time':
        return TimeType()
    elif formatValue == 'date-time':
        return DateTimeType()
    elif formatValue == 'duration':
        return DurationType()
    elif formatValue == 'uuid':
        return UuidType()
    elif formatValue == 'byte':
        return BytesType()
    else:
        s = StringType()
        s.format = formatValue
        return s


def __initEnumValuesFromContent(enumType, enumValuesArray):
    if len(enumValuesArray) > 0:
        if isinstance(enumValuesArray[0], str):
            enumType.values = enumValuesArray
        elif isinstance(enumValuesArray[0], int):
            enumType.numValues = enumValuesArray
            enumType.type = IntegerType()
        elif isinstance(enumValuesArray[0], float):
            enumType.numValues = enumValuesArray
            enumType.type = NumberType()
        else:
            enumType.values = enumValuesArray


def _extractEnumType(newTypeName, newProperty, enumValue, typeStr, formatStr, modelTypes, modelFileContainer):
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
            if (len(alreadyCreatedType.values) != 0) or (len(alreadyCreatedType.values) != 0):
                return alreadyCreatedType
            else:
                enumType = alreadyCreatedType
        else:
            # a dummy type was pre-created. now it has been filled with the real values
            enumType = EnumType()
            enumType.domain = modelFileContainer.domain
            enumType.name = enumTypeName
    else:
        enumType = EnumType()
        enumType.domain = modelFileContainer.domain
        enumType.name = enumTypeName

    if typeStr == 'integer':
        enumType.type = IntegerType()
        enumType.type.format = IntegerTypeFormatEnum.valueForString(formatStr)
        enumType.numValues = enumValue
    elif typeStr == 'number':
        enumType.type = NumberType()
        enumType.type.format = NumberTypeFormatEnum.valueForString(formatStr)
        enumType.numValues = enumValue
    elif typeStr == 'string':
        # DateType, TimeType, DateTimeType, StringType, EnumType, DurationType
        if formatStr == 'date':
            enumType.type = DateType()
        elif formatStr == 'time':
            enumType.type = TimeType()
        elif formatStr == 'date-time':
            enumType.type = DateTimeType()
        elif formatStr == 'duration':
            enumType.type = DurationType()
        elif formatStr == 'uuid':
            enumType.type = UuidType()
        elif formatStr == 'byte':
            enumType.type = BytesType()
        else:
            enumType.type = StringType()
        enumType.values = enumValue
    else:
        enumType.type = StringType()
        __initEnumValuesFromContent(enumType, enumValue)

    enumType.source = modelFileContainer.fileName
    enumType.version = modelFileContainer.version
    if alreadyCreatedType is not None:
        _replaceAllCurrentAppearencesOfAlreadyCreatedType(alreadyCreatedType, enumType, modelTypes)
    else:
        _appendToAlreadyLoadedTypes(enumType, modelTypes)
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
            for key, value in tag.items():
                tagObj = Tag()
                tagObj.name = key
                tagObj.value = value
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
        if command.operationId is None:
            opId = toName(pathType.pathPattern)
            command.operationId = toLowerCamelCase(commandKey + " " + opId)
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
    __extractOpenApiContentSectionAndAppend(contentDict, requestBody, modelTypes, modelFileContainer, command.operationId)


def __extractOpenApiContentSectionAndAppend(contentDict, contentHost, modelTypes, modelFileContainer, innerTypeName):
    if contentDict is None:
        return
    for contentDictKey in contentDict.keys():
        content = contentDict[contentDictKey]
        contentEntry = openapi.ContentEntry()
        contentEntry.mimeType = contentDictKey
        schema = content.get('schema', None)
        __getTypeFromSchemaDictAndAsignId(schema, contentEntry, modelTypes, modelFileContainer, innerTypeName)
        contentHost.content.append(contentEntry)


def __getTypeFromSchemaDictAndAsignId(schema, typeHost, modelTypes, modelFileContainer, innerTypeName):
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
        typeHost.type = _extractReferenceType(refEntry, modelTypes, modelFileContainer, False)
    else:
        dictToUse = itemsEntry if typeHost.isArray is True else schema
        propertiesDict = dictToUse.get('properties', None)
        if propertiesDict is not None:
            newInnerTypeName = innerTypeName
            typeHost.type = _extractObjectType(newInnerTypeName, propertiesDict, None, None, None, None, modelTypes, modelFileContainer, False, False)
        else:
            errorMsg = 'Attention, inner type declarations are currently not implemented for some additional model scenarios.'
            logging.error(errorMsg)


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
                __getTypeFromSchemaDictAndAsignId(schema, contentEntry, modelTypes, modelFileContainer, command.operationId)
        else:
            parameter = openapi.Parameter()
            command.parameters.append(parameter)
            parameter.inType = openapi.ParameterInTypeEnum.valueForString(originalInType)
            parameter.name = param.get('name', None)
            parameter.description = param.get('description', None)
            parameter.required = param.get('required', False)
            __extractParameterType(param, modelTypes, modelFileContainer, parameter, command.operationId)


def __extractParameterType(paramDict, modelTypes, modelFileContainer, parameterObj, paramName):
    paramSchema = paramDict.get('schema', None)
    paramType = paramDict.get('type', None)
    if (paramSchema is None) and (paramType is None):
        logging.error(
            "modelFile: %s, name=%s: missing schema or type entry" %
            (modelFileContainer.fileName, paramName))
    if paramSchema is not None:
        parameterObj.type = _extractAttribType(
            paramName.capitalize(),
            parameterObj,
            paramSchema,
            modelTypes,
            modelFileContainer, True)
    elif paramType is not None:
        parameterObj.type = _extractAttribType(
            paramName.capitalize(),
            parameterObj,
            paramDict,
            modelTypes,
            modelFileContainer, True)


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
            __extractOpenApiContentSectionAndAppend(contentDict, response, modelTypes, modelFileContainer, command.operationId)
        else:
            # swagger v2
            schema = responseDict.get('schema', None)
            if schema is not None:
                contentEntry = openapi.ContentEntry()
                response.content.append(contentEntry)
                __getTypeFromSchemaDictAndAsignId(schema, contentEntry, modelTypes, modelFileContainer, command.operationId)


def __getAdditionalPropertiesForDictionaryType(dictionary):
    additionalProperties = dictionary.get('additionalProperties', None)
    if (additionalProperties is not None) and (type(additionalProperties) == bool):
        # additionalProperties are only handled as objects here
        return None
    return additionalProperties


def _parseAsyncApiInfo(modelTypes, parsedSchema):
    infoDict = parsedSchema.get('info', None)
    if infoDict is None:
        return
    infoObj = asyncapi.AsyncApiInfo()
    __initInfoObj(infoObj, infoDict)
    modelTypes.append(infoObj)


def _parseAsyncApiServers(modelTypes, parsedSchema):
    serversDict = parsedSchema.get('servers', None)
    if serversDict is None:
        return
    for key in serversDict.keys():
        serverDict = serversDict.get(key, None)
        if serverDict is None:
            continue
        serverType = asyncapi.AsyncApiServer()
        serverType.name = key
        serverType.url = serverDict.get('url', None)
        serverType.description = serverDict.get('description', None)
        serverType.protocol = serverDict.get('protocol', None)
        serverType.protocolVersion = serverDict.get('protocolVersion', None)
        modelTypes.append(serverType)


def _parseAsyncApiChannelParameters(modelTypes, channelDict, channelType, modelFileContainer, channelKey):
    parametersDict = channelDict.get('parameters', None)
    if parametersDict is None:
        return
    for key in parametersDict.keys():
        paramDict = parametersDict.get(key, None)
        if paramDict is None:
            continue
        # could be a reference to the components section
        refValue = paramDict.get("$ref", None)
        if refValue is None:
            paramType = __createNewChannelParam(modelTypes, key, paramDict, modelFileContainer)
            modelTypes.append(paramType)
        else:
            paramType = __getAlreadyLoadedChannelParam(modelTypes, refValue)
            if paramType is None:
                logging.error("Parameter reference not found: channel: {}, parameter: {}".format(channelKey, key))
        if (channelType is not None) and (paramType is not None):
            channelType.parameters.append(paramType)


def getDesiredNameFromRefValue(refValue):
    lastSlash = refValue.rfind('/')
    lastSlash = lastSlash + 1
    return refValue[lastSlash:]


def __getAlreadyLoadedChannelBinding(modelTypes, refValue):
    desiredName = getDesiredNameFromRefValue(refValue)
    for type in modelTypes:
        if isinstance(type, asyncapi.ChannelBindingsAmqp):
            if type.name == desiredName:
                return type
    return None


def __getAlreadyLoadedChannelParam(modelTypes, refValue):
    desiredName = getDesiredNameFromRefValue(refValue)
    for type in modelTypes:
        if isinstance(type, asyncapi.Parameter):
            if type.name == desiredName:
                return type
    return None


def __createNewChannelParam(modelTypes, key, paramDict, modelFileContainer):
    paramType = asyncapi.Parameter()
    paramType.name = key
    paramType.description = paramDict.get('description', None)
    __extractParameterType(paramDict, modelTypes, modelFileContainer, paramType, key)
    return paramType


def _initAsyncApiMessagePayload(messageDict, modelTypes, modelFileContainer, name):
    payloadDict = messageDict.get('payload', None)
    if payloadDict is None:
        return None
    payload = asyncapi.Payload()
    __getTypeFromSchemaDictAndAsignId(payloadDict, payload, modelTypes, modelFileContainer, name)
    return payload


def _initAsyncApiMessageHeaders(messageDict, modelTypes, modelFileContainer, innerTypeName):
    headersDict = messageDict.get('headers', None)
    if headersDict is None:
        return None

    refEntry = headersDict.get("$ref", None)
    if refEntry is not None:
        # load reference type
        return _extractReferenceType(refEntry, modelTypes, modelFileContainer, False)

    typeEntry = headersDict.get("type", None)
    if typeEntry is None:
        logging.error("unknown headers type")
        return None
    if typeEntry != "object":
        logging.error("headers type isn't object: {}".format(typeEntry))
        return None

    propertiesDict = headersDict.get('properties', None)
    if propertiesDict is not None:
        return _extractObjectType(innerTypeName, propertiesDict, None, None, None, None, modelTypes, modelFileContainer, False, False)
    else:
        errorMsg = 'Wrong message headers inner type'
        logging.error(errorMsg)


def _parseAsyncApiChannels(modelTypes, parsedSchema, modelFileContainer):
    channelsDict = parsedSchema.get('channels', None)
    if channelsDict is None:
        return
    for key in channelsDict.keys():
        channelDict = channelsDict.get(key, None)
        if channelDict is None:
            continue
        channelType = asyncapi.Channel()
        channelType.key = key
        channelType.description = channelDict.get('description', None)
        _parseAsyncApiChannelParameters(modelTypes, channelDict, channelType, modelFileContainer, key)
        _parseAsyncApiChannelPublish(modelTypes, channelDict, channelType, modelFileContainer)
        _parseAsyncApiChannelSubscribe(modelTypes, channelDict, channelType, modelFileContainer)
        _parseAsyncApiChannelBindings(modelTypes, channelDict, channelType)
        modelTypes.append(channelType)


def _parseAsyncApiOperationBinding(operationDict, modelTypes, channelType):
    bindingsDict = operationDict.get("bindings", None)
    bindingsObj = None
    if bindingsDict is not None:
        refValue = bindingsDict.get("$ref", None)
        if refValue is None:
            bindingsObj = __initOperationBindingsAmqpObj(None, bindingsDict.get("amqp", None), modelTypes)
        else:
            bindingsObj = __getAlreadyLoadedOperationBinding(modelTypes, refValue)
            if bindingsObj is None:
                logging.error("Operation binding reference not found: channel: {}, parameter: {}".format(channelType.key, refValue))  # noqa: E501
    return bindingsObj


def _parseAsyncApiOperationMessageBinding(messageDict, modelTypes):
    amqpBindingsObj = None
    bindingsDict = messageDict.get("bindings", None)
    if bindingsDict is not None:
        refValue = bindingsDict.get("$ref", None)
        if refValue is not None:
            # binding is already loaded
            amqpBindingsObj = __getAlreadyLoadedMessageBinding(modelTypes, refValue)
        else:
            amqpBindingsDict = bindingsDict.get("amqp", None)
            if amqpBindingsDict is not None:
                amqpBindingsObj = __initMessageBindingsAmqpObj(None, amqpBindingsDict, modelTypes)
    return amqpBindingsObj


def _parseAsyncApiOperationMessage(operationDict, modelTypes, operationType, modelFileContainer, messageKey):
    messageDict = operationDict.get(messageKey, None)
    messageObj = None
    typePrefix = ""
    if messageKey == "x-responseMessage":
        typePrefix = "XResponse"
    if messageDict is not None:
        messageObj = asyncapi.Message()
        messageObj.amqpBindings = _parseAsyncApiOperationMessageBinding(messageDict, modelTypes)
        messageObj.payload = _initAsyncApiMessagePayload(messageDict, modelTypes, modelFileContainer, "{}Payload_{}".format(typePrefix, operationType.operationId))  # noqa: E501
        messageObj.headers = _initAsyncApiMessageHeaders(messageDict, modelTypes, modelFileContainer, "{}Headers_{}".format(typePrefix, operationType.operationId))  # noqa: E501
    return messageObj


def _parseAsyncApiChannelSubscribe(modelTypes, channelDict, channelType, modelFileContainer):
    subscribeDict = channelDict.get("subscribe", None)
    if subscribeDict is None:
        return
    subscribeObj = asyncapi.OperationBase()
    channelType.subscribe = subscribeObj
    __parseAsyncApiOperationBase(modelTypes, subscribeObj, subscribeDict, channelType, modelFileContainer)
    channelType.subscribe.xResponseMessage = _parseAsyncApiOperationMessage(subscribeDict, modelTypes, subscribeObj, modelFileContainer, "x-responseMessage")  # noqa: E501


def _parseAsyncApiChannelPublish(modelTypes, channelDict, channelType, modelFileContainer):
    publishDict = channelDict.get("publish", None)
    if publishDict is None:
        return
    publishObj = asyncapi.OperationBase()
    channelType.publish = publishObj
    __parseAsyncApiOperationBase(modelTypes, publishObj, publishDict, channelType, modelFileContainer)
    channelType.publish.xResponseMessage = _parseAsyncApiOperationMessage(publishDict, modelTypes, publishObj, modelFileContainer, "x-responseMessage")  # noqa: E501


def __parseAsyncApiOperationBase(modelTypes, operationObj, operationDict, channelType, modelFileContainer):
    modelTypes.append(operationObj)
    operationObj.description = operationDict.get("description", None)
    operationObj.summary = operationDict.get("summary", None)
    operationObj.operationId = operationDict.get("operationId", None)
    if operationObj.operationId is None:
        opId = toName(channelType.key)
        opId = toUpperCamelCase(opId, '_')
        operationObj.operationId = opId

    operationObj.amqpBindings = _parseAsyncApiOperationBinding(operationDict, modelTypes, channelType)
    operationObj.message = _parseAsyncApiOperationMessage(operationDict, modelTypes, operationObj, modelFileContainer, "message")


def __getAlreadyLoadedMessageBinding(modelTypes, refValue):
    desiredName = getDesiredNameFromRefValue(refValue)
    for type in modelTypes:
        if isinstance(type, asyncapi.MessageBindingsAmqp):
            if type.name == desiredName:
                return type
    return None


def __getAlreadyLoadedOperationBinding(modelTypes, refValue):
    desiredName = getDesiredNameFromRefValue(refValue)
    for type in modelTypes:
        if isinstance(type, asyncapi.OperationBindingsAmqp):
            if type.name == desiredName:
                return type
    return None


def _parseAsyncApiChannelBindings(modelTypes, channelDict, channelType):
    bindingsDict = channelDict.get("bindings", None)
    if bindingsDict is None:
        return
    refValue = bindingsDict.get("$ref", None)
    bindingsObj = None
    if refValue is None:
        amqpBindingsDict = bindingsDict.get("amqp", None)
        if amqpBindingsDict is not None:
            bindingsObj = __initChannelBindingsAmqpObj(None, amqpBindingsDict, modelTypes)
    else:
        bindingsObj = __getAlreadyLoadedChannelBinding(modelTypes, refValue)
        if bindingsObj is None:
            logging.error("Channel binding reference not found: channel: {}, binding: {}".format(channelType.name, refValue))
    channelType.amqpBindings = bindingsObj


def extractAsyncApiTypes(modelTypes, modelFileContainer):
    """extract the asyncapi specific types from the parsed schema


    Keyword arguments:
    modelTypes -- dictionary with the loaded schema
    modelFileContainer -- container that bundles data around the file to parse
    """

    parsedSchema = modelFileContainer.parsedSchema
    _parseAsyncApiInfo(modelTypes, parsedSchema)
    _parseAsyncApiServers(modelTypes, parsedSchema)
    _parseAsyncApiChannels(modelTypes, parsedSchema, modelFileContainer)


def _extractAsyncApiAmqpChannelBindings(componentsDict, modelTypes, modelFileContainer):
    bindingsDict = componentsDict.get("channelBindings", {})
    for key in bindingsDict.keys():
        dict = bindingsDict.get(key, {})
        amqpBindingsDict = dict.get("amqp", None)
        if amqpBindingsDict is None:
            continue
        __initChannelBindingsAmqpObj(key, amqpBindingsDict, modelTypes)


def __initChannelBindingsAmqpObj(name, amqpBindingsDict, modelTypes):
    bindingsObj = asyncapi.ChannelBindingsAmqp()
    bindingsObj.name = name
    bindingsObj.isType = asyncapi.ChannelBindingsAmqpIsTypeEnum.valueForString(amqpBindingsDict.get("is", "routingKey"))
    bindingsObj.exchange = __initChannelBindingsExchange(amqpBindingsDict.get("exchange", None))
    bindingsObj.queue = __initChannelBindingsQueue(amqpBindingsDict.get("queue", None))
    modelTypes.append(bindingsObj)
    return bindingsObj


def __initChannelBindingsExchange(exchangeDict):
    if exchangeDict is None:
        return None
    exchangeObj = asyncapi.ChannelBindingsAmqpExchange()
    exchangeObj.name = exchangeDict.get("name", None)
    exchangeObj.type = asyncapi.ChannelBindingsAmqpExchangeTypeEnum.valueForString(exchangeDict.get("type", None))
    exchangeObj.durable = exchangeDict.get("durable", False)
    exchangeObj.autoDelete = exchangeDict.get("autoDelete", False)
    return exchangeObj


def __initChannelBindingsQueue(queueDict):
    if queueDict is None:
        return None
    queueObj = asyncapi.ChannelBindingsAmqpQueue()
    queueObj.name = queueDict.get("name", None)
    queueObj.durable = queueDict.get("durable", False)
    queueObj.exclusive = queueDict.get("exclusive", False)
    queueObj.autoDelete = queueDict.get("autoDelete", False)
    return queueObj


def _extractAsyncApiAmqpMessageBindings(componentsDict, modelTypes, modelFileContainer):
    bindingsDict = componentsDict.get("messageBindings", {})
    for key in bindingsDict.keys():
        dict = bindingsDict.get(key, {})
        amqpBindingsDict = dict.get("amqp", None)
        if amqpBindingsDict is None:
            continue
        __initMessageBindingsAmqpObj(key, amqpBindingsDict, modelTypes)


def __initMessageBindingsAmqpObj(name, amqpBindingsDict, modelTypes):
    bindingsObj = asyncapi.MessageBindingsAmqp()
    bindingsObj.name = name
    bindingsObj.contentEncoding = amqpBindingsDict.get("contentEncoding", None)
    bindingsObj.messageType = amqpBindingsDict.get("messageType", None)
    modelTypes.append(bindingsObj)
    return bindingsObj


def _extractAsyncApiAmqpOperationBindings(componentsDict, modelTypes, modelFileContainer):
    bindingsDict = componentsDict.get("operationBindings", {})
    for key in bindingsDict.keys():
        dict = bindingsDict.get(key, {})
        amqpBindingsDict = dict.get("amqp", None)
        if amqpBindingsDict is None:
            continue
        __initOperationBindingsAmqpObj(key, amqpBindingsDict, modelTypes)


def __initOperationBindingsAmqpObj(name, amqpBindingsDict, modelTypes):
    if amqpBindingsDict is None:
        return None
    bindingsObj = asyncapi.OperationBindingsAmqp()
    bindingsObj.name = name
    bindingsObj.expiration = amqpBindingsDict.get("expiration", None)
    bindingsObj.replyTo = amqpBindingsDict.get("replyTo", "amq.rabbitmq.reply-to")
    bindingsObj.mandatory = amqpBindingsDict.get("mandatory", False)
    modelTypes.append(bindingsObj)
    return bindingsObj
