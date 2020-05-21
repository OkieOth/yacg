"""Reads JSON schemas in yaml format and build the model types from it"""

import os.path

from .impl.dictionaryBuilder import extractTypes, getParsedSchemaFromYaml


def getModelFromYaml(model, typeList, skipOpenApi=False):
    """reads a JSON schema file and build a model from it,
    returns a list of yacg.model.model.Type objects


    Keyword arguments:
    model -- config.Model instance
    typeList -- list of already loaded types
    """

    modelFile = model.schema
    parsedSchema = getParsedSchemaFromYaml(modelFile)
    modelFile = os.path.abspath(modelFile)
    return extractTypes(parsedSchema, modelFile, typeList, skipOpenApi)
