"""This file bundles the functions use to extract the path information
from parsed openApi or swagger files
"""

import yacg.model.openapi as openapi


def extractOpenApiPathTypes(modelTypes, parsedSchema):
    pathDict = parsedSchema.get('path', None)
    if pathDict is None:
        return
    for pathKey in pathDict:
        pathType = openapi.PathType()
        pathType.pathPattern = pathKey
        commandDict = pathDict[pathKey]
        _extractCommandsForPath(pathType, commandDict)
        modelTypes.append(pathType)


def _extractCommandsForPath(pathType, commandDict):
    pass
