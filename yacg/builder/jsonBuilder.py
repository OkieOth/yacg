"""Reads JSON schema files and build the model types from it"""

import json

from yacg.model.model import ComplexType 
from yacg.model.model import Property 
from yacg.util.stringUtils import toUpperCamelCase
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType
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
    
    newType = ComplexType(typeNameStr)
    newType.source = modelFile    
    modelTypes.append(newType)
    extractAttributes(newType,properties,modelTypes,modelFile)


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
    if type == 'int':
        return IntegerType()
    elif type =='number':
        return NumberType()
    elif type =='string':
        # DateType, DateTimeType, StringType, EnumType
        return extractStringType(newType,newProperty,propDict,modelTypes,modelFile)
    elif type =='object':
        # TODO ComplexType
        return None
    else:
        # TODO logging
        # return None
        pass

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
    pass #TODO

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