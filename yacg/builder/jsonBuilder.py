"""Reads JSON schema files and build the model types from it"""

import json
from yacg.builder.impl.dictionaryBuilder import extractTypes


def getModelFromJson(modelFile):
    """reads a JSON schema file and build a model from it, 
    returns a list of yacg.model.model.Type objects
    
    
    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    parsedSchema = getParsedSchema(modelFile)
    return extractTypes (parsedSchema,modelFile)

def getParsedSchema(modelFile):
    """reads a JSON schema file in json format
    and returns the parsed dictionary from it
    
    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    with open(modelFile) as json_schema:
        return json.load(json_schema)
