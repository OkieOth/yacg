"""Reads JSON schemas in yaml format and build the model types from it"""

import yaml

from yacg.builder.impl.dictionaryBuilder import extractTypes

def getModelFromYaml(modelFile):
    """reads a JSON schema file and build a model from it, 
    returns a list of yacg.model.model.Type objects
    
    
    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    parsedSchema = getParsedSchema(modelFile)
    return extractTypes (parsedSchema,modelFile)

def getParsedSchema(modelFile):
    """reads a JSON schema file in yaml format
    and returns the parsed dictionary from it
    
    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    with open(modelFile) as json_schema:
        return yaml.load(json_schema, Loader=yaml.FullLoader)
