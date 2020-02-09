"""Reads JSON schema files and build the model types from it"""

import json

def getModelFromJson(modelFile):
    with open(modelFile) as json_schema:
        parsedSchema = json.load(json_schema)
        print (parsedSchema)