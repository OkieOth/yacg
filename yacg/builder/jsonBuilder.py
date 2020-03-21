"""Reads JSON schema files and build the model types from it"""

import json
import logging

from yacg.model.model import ComplexType 
from yacg.model.model import Property 
from yacg.util.stringUtils import toUpperCamelCase
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType

def getModelFromJson(modelFile):
    """reads a JSON schema file and build a model from it, 
    returns a list of yacg.model.model.Type objects
    
    
    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    with open(modelFile) as json_schema:
        parsedSchema = json.load(json_schema)
        return extractTypes (parsedSchema,modelFile)

def extractTypes(parsedSchema,modelFile):
    """extract the types from the parsed schema


    Keyword arguments:
    parsedSchema -- dictionary with the loaded schema
    modelFile -- file name and path to the model to load
    """
    
    modelTypes = []
    schemaType = parsedSchema.get('type',None)
    schemaProperties = parsedSchema.get('properties',None)
    if (schemaType=='object') and (schemaProperties!=None):
        # extract top level type
        titleStr = parsedSchema.get('title',None)
        typeNameStr = toUpperCamelCase(titleStr)
        extractObjectType(typeNameStr,schemaProperties,modelTypes,modelFile)
    schemaDefinitions = parsedSchema.get('definitions',None)
    if schemaDefinitions != None:
        # extract types from extra definitions section
        extractDefinitionsTypes(schemaDefinitions,modelTypes,modelFile)
    return modelTypes

def extractDefinitionsTypes(definitions,modelTypes,modelFile):    
    """build types from definitions section
    
    Keyword arguments:
    definitions -- dict of a schema definitions-block
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load    
    """

    for key in definitions.keys():
        object = definitions[key]
        properties = object.get('properties',None)
        extractObjectType(key,properties,modelTypes,modelFile)    


def extractObjectType(typeNameStr,properties,modelTypes,modelFile):
    """build a type object

    Keyword arguments:
    typeNameStr -- Name of the new type
    properties -- dict of a schema properties-block
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """
    
    # check up that no dummy for this type is already created.
    alreadyCreatedType = getAlreadyCreatedTypesWithThatName(typeNameStr,modelTypes,modelFile)
    # This can be the case in situations where attributes refer to another complex type
    newType = ComplexType(typeNameStr) if alreadyCreatedType == None else alreadyCreatedType 
    newType.source = modelFile
    if alreadyCreatedType == None:            
        modelTypes.append(newType)
    if len(newType.properties)==0: 
        extractAttributes(newType,properties,modelTypes,modelFile)

def getAlreadyCreatedTypesWithThatName(typeNameStr,modelTypes,modelFile):
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

def extractAttributes(type, properties, modelTypes,modelFile):
    """extract the attributes of a type from the parsed model file

    Keyword arguments:
    type -- type that contains the properties
    properties -- dict of a schema properties-block
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    for key in properties.keys():
        propDict = properties[key]
        propName = key
        newProperty =  Property(propName,None)
        newProperty.type = extractAttribType(type,newProperty,propDict,modelTypes,modelFile)
        #TODO
        type.properties.append(newProperty)

def extractAttribType(newType,newProperty,propDict,modelTypes,modelFile):
    """extract the type from the parsed model file and
    returns the type of the property.

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    type = propDict.get('type',None)
    refEntry = propDict.get('$ref',None)
    if type == 'integer':
        return IntegerType()
    elif type =='number':
        return NumberType()
    elif type =='string':
        # DateType, DateTimeType, StringType, EnumType
        return extractStringType(newType,newProperty,propDict,modelTypes,modelFile)
    elif type =='object':
        return extractComplexType(newType,newProperty,propDict,modelTypes,modelFile)
    else:
        if refEntry != None:
            # TODO extract reference type
            return extractReferenceType(newType,newProperty,refEntry,modelTypes,modelFile)
        else:
            logging.error("modelFile: %s, type=%s, property=%s: unknown property type: %s" 
                % (modelFile,newType.name,newProperty.name,type))
            return None


def extractReferenceType(newType,newProperty,refEntry,modelTypes,modelFile):
    """build or reload a type reference 
    and return it

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    refEntry -- $ref entry from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    # TODO .. #/definitions/
    localDefinitionsStr = '#/definitions/'
    if refEntry.startswith(localDefinitionsStr):
        # internal reference
        typeName = refEntry[len(localDefinitionsStr):]
        return extractInternalReferenceType(newType,newProperty,typeName,modelTypes,modelFile)
    else:
        # external reference
        pass
    pass

def extractInternalReferenceType(newType,newProperty,refTypeName,modelTypes,modelFile):
    """builds or relaod a type reference in the current file
    and return it.

    If the type isn't loaded an empty dummy is created.

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    refTypeName -- name of the referenced type
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    alreadyCreatedType = getAlreadyCreatedTypesWithThatName(refTypeName,modelTypes,modelFile)
    if alreadyCreatedType != None:
        return alreadyCreatedType 
    dummyReference = ComplexType(refTypeName)
    dummyReference.source = modelFile
    modelTypes.append(dummyReference)
    return dummyReference

def extractComplexType(newType,newProperty,propDict,modelTypes,modelFile):
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
    newInnerType = ComplexType(innerTypeName)
    newInnerType.source = modelFile
    modelTypes.append(newInnerType)
    properties = propDict.get('properties',None)
    if properties != None:
        extractAttributes(newInnerType, properties, modelTypes,modelFile)
    else:
        logging.error("modelFile: %s, type=%s, property=%s: inner complex type without properties" 
                % (modelFile, newType.name,newProperty.name))
    return newInnerType


def extractStringType(newType,newProperty,propDict,modelTypes,modelFile):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    propDict -- dict of the property from the model file
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    formatValue = propDict.get('format',None)
    enumValue = propDict.get('enum',None)
    if (formatValue == None) and (enumValue == None):
        return StringType()
    elif enumValue != None:
        return extractEnumType(newType,newProperty,enumValue,modelTypes,modelFile)
    elif formatValue == 'date':
        return DateType()
    elif formatValue == 'date-time':
        return DateTimeType()
    elif formatValue == 'uuid':
        return UuidType()
    else:
        # TODO logging
        logging.error("modelFile: %s, type=%s, property=%s: unknown string type format: %s" 
            % (modelFile,newType.name,newProperty.name,formatValue))
        return StringType()

def extractEnumType(newType,newProperty,enumValue,modelTypes,modelFile):
    """extract the specific string type depending on the given format
    and return the specific type

    Keyword arguments:
    newType -- current Type
    newProperty -- current property
    enumValues -- list with allowed values
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    enumTypeName = toUpperCamelCase(newType.name + ' ' + newProperty.name + 'Enum');    
    enumType = EnumType(enumTypeName)
    enumType.values = enumValue
    enumType.source = modelFile
    return enumType