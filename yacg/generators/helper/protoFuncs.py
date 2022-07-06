"""Set of functions to smooth model handling for templates that create
Protocol Buffers (protobuf) related code
"""

import yacg.model.model as model


def getType(property):
    """This method returns the name of the .protoType representing the model type
    defined in the provided property.

    Keyword arguments:
    property -- the property providing the type definition
    """
    type = property.type
    if type is None:
        return '???'
    elif isinstance(type, model.IntegerType):
        if type.format is None:
            return 'int32'
        elif type.format is model.IntegerTypeFormatEnum.INT32:
            return 'int32'
        elif type.format is model.IntegerTypeFormatEnum.INT64:
            return 'int64'
        else:
            return 'int32'
    elif isinstance(type, model.NumberType):
        if type.format is None:
            return 'double'
        elif type.format is model.NumberTypeFormatEnum.DOUBLE:
            return 'double'
        elif type.format is model.NumberTypeFormatEnum.FLOAT:
            return 'float'
        else:
            return 'double'
    elif isinstance(type, model.BooleanType):
        return 'bool'
    elif isinstance(type, model.StringType):
        return 'string'
    elif isinstance(type, model.UuidType):
        return 'string'
    elif isinstance(type, model.EnumType):
        return type.name
    elif isinstance(type, model.DateType):
        return 'google.protobuf.Date'
    elif isinstance(type, model.TimeType):
        return 'google.protobuf.TimeOfDay'
    elif isinstance(type, model.DateTimeType):
        return 'google.protobuf.Timestamp'
    elif isinstance(type, model.ComplexType):
        return type.name
    else:
        return '???'
