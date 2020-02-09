"""Reads JSON schemas in yaml format and build the model types from it"""

import yaml

def getModelFromYaml():
    with open(modelFile) as json_schema:
        parsedSchema = yaml.load(json_schema, Loader=yaml.FullLoader)
        print (parsedSchema)
