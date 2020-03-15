"""Reads JSON schema files and build the model types from it"""

import json

def getModelFromJson(modelFile):
    """reads a JSON schema file and build a model from it"""

    with open(modelFile) as json_schema:
        parsedSchema = json.load(json_schema)
        #print (parsedSchema)
        return [] #TODO
