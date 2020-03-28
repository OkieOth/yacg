"""Reads JSON schemas in yaml format and build the model types from it"""

import os.path

from yacg.builder.impl.dictionaryBuilder import extractTypes, getParsedSchemaFromYaml

def getModelFromYaml(modelFile):
    """reads a JSON schema file and build a model from it, 
    returns a list of yacg.model.model.Type objects
    
    
    Keyword arguments:
    modelFile -- file name and path to the model to load
    """

    parsedSchema = getParsedSchemaFromYaml(modelFile)
    modelFile = os.path.abspath(modelFile)
    return extractTypes (parsedSchema,modelFile,[])


