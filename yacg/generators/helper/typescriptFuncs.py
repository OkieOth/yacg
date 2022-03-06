"""Set of functions to smooth model handling for templates that create
Typescript code
"""

import yacg.model.model as model


def printTypescriptType(type, isArray):
    if type is None:
        return 'unknown' if not isArray else 'unknown[]'
    elif isinstance(type, model.IntegerType):
        return 'number' if not isArray else 'number[]'
    elif isinstance(type, model.ObjectType):
        return 'Object' if not isArray else 'Object[]'
    elif isinstance(type, model.NumberType):
        return 'number' if not isArray else 'number[]'
    elif isinstance(type, model.BooleanType):
        return 'boolean' if not isArray else 'boolean[]'
    elif isinstance(type, model.StringType):
        return 'string' if not isArray else 'string[]'
    elif isinstance(type, model.UuidType):
        # instead of the original type definition, here is only string used
        return 'string | any' if not isArray else 'string[] | any[]'
    elif isinstance(type, model.EnumType):
        return "{type}".format(type=type.name) if not isArray else "{type}[]".format(type=type.name)
    elif isinstance(type, model.DateTimeType):
        return 'Date' if not isArray else 'Date[]'
    elif isinstance(type, model.DateType):
        return 'Date' if not isArray else 'Date[]'
    elif isinstance(type, model.BytesType):
            return 'number[]' if not isArray else 'number[][]'
    elif isinstance(type, model.DictionaryType):
        return "Map<String, {}>".format(printTypescriptType(type.valueType)) if not isArray else "Map<String, {}>[]".format(printTypescriptType(type.valueType))
    elif isinstance(type, model.ComplexType):
        return "{type}".format(type=type.name) if not isArray else "{type}[]".format(type=type.name)
    else:
        return type
