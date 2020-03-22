"""Reads JSON schemas in yaml format and build the model types from it"""

import yaml

def getModelFromYaml(modelFile):
    """reads a JSON schema file in yaml format and build a model from it"""

    parsedSchema = getParsedSchema(modelFile)
    # TODO

def getParsedSchema(modelFile):
    """reads a JSON schema file in yaml format
    and returns the parsed dictionary from it"""

    with open(modelFile) as json_schema:
        return yaml.load(json_schema, Loader=yaml.FullLoader)
