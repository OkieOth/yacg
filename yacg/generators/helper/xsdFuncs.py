"""Set of functions to smooth model handling for templates that create
XML Schema (XSD)
"""

import yacg.model.model as model


def printXsdType(prop):
    """This method returns the name of the XML type representing the model type
    defined in the provided property.

    Keyword arguments:
    property -- the property providing the type definition
    """
    type = prop.type
    if type is None:
        return '???'
    elif isinstance(type, model.IntegerType):
        if type.format is model.IntegerTypeFormatEnum.INT32:
            return 'xsd:int'
        elif type.format is model.IntegerTypeFormatEnum.INT64:
            return 'xsd:long'
        else:
            return 'xsd:integer'
    elif isinstance(type, model.NumberType):
        if type.format is model.NumberTypeFormatEnum.DOUBLE:
            return 'xsd:double'
        elif type.format is model.NumberTypeFormatEnum.FLOAT:
            return 'xsd:float'
        else:
            return 'xsd:decimal'
    elif isinstance(type, model.BooleanType):
        return 'xsd:boolean'
    elif isinstance(type, model.StringType):
        return 'xsd:string'
    elif isinstance(type, model.UuidType):
        return 'tns:Guid'
    elif isinstance(type, model.EnumType):
        return "tns:{}".format(type.name)
    elif isinstance(type, model.DateType):
        return 'xsd:date'
    elif isinstance(type, model.TimeType):
        return 'xsd:time'
    elif isinstance(type, model.DateTimeType):
        return 'xsd:dateTime'
    elif isinstance(type, model.ObjectType):
        return 'xsd:any'
    elif isinstance(type, model.BytesType):
        return 'xsd:base64Binary'
    elif isinstance(type, model.ComplexType):
        return "tns:{}".format(type.name)
    else:
        return '???'
