"""This is a custom filter that allows to create multifile output
based on swagger/openApi operationId
"""


def swaggerFilterByOperationId(pathTypes):
    """take pathTypes and return a dictionary with operationId as key
    and PathType object as value

    Keyword arguments:
    pathTypes -- list of types that build the model, list of yacg.model.openapi.PathType instances
    """

    ret = {}
    for pathType in pathTypes:
        for command in pathType.commands:
            ret[command.operationId] = pathTypes
    return ret
