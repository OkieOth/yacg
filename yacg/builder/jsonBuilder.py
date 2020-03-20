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
    if (parsedSchema['type']=='object') and (parsedSchema['properties']!=None):
        # extract top level type
        titleStr = parsedSchema['title']
        typeNameStr = toUpperCamelCase(titleStr)
        properties = parsedSchema['properties']
        extractObjectType(typeNameStr,properties,modelTypes,modelFile)
    if parsedSchema['definitions'] != None:
        # extract types from extra definitions section
        definitions = parsedSchema['definitions']
        extractDefinitionsTypes(definitions,modelTypes,modelFile)
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
        properties = object['properties']
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
        prop = properties[key]
        propName = key
        extractAndSetAttribType(prop,modelTypes,modelFile)
        newProperty =  Property(propName,propType)
        #TODO
        type.properties.append(newProperty)

def extractAndSetAttribType(prop,modelTypes,modelFile):
    """extract the type from the parsed model file

    Keyword arguments:
    prop -- dict of the property
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """

    type = prop['type']
    if type == 'int':
        prop.type = IntegerType()
        pass
    elif type =='number':
        prop.type = NumberType()
        pass
    elif type =='string':
        # DateType, DateTimeType, StringType, EnumType
        pass
    elif type =='object':
        # TODO ComplexType
        pass
    else:
        pass

def extractAndSetStringType(prop,modelTypes,modelFile):
    """extract the type from the parsed model file

    Keyword arguments:
    prop -- dict of the property
    modelTypes -- list of already loaded models
    modelFile -- file name and path to the model to load        
    """
    pass #TODO