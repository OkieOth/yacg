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


def _extractCommandsForPath(pathType, commandsDict):
    for commandKey in commandsDict:
        commandDict = commandsDict[commandKey]
        command = openapi.Command()
        command.command = openapi.CommandCommandEnum.valueForString(commandKey)
        command.description = commandDict.get('description', None)
        command.summary = commandDict.get('summary', None)
        command.operationId = commandDict.get('operationId', None)
        command.tags = commandDict.get('tags', [])

        pathType.commands.append(command)
