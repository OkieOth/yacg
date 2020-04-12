# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Type:
    """ base type for all type
    """

    def __init__(self):
        self.name = None


class IntegerType (Type):
    """ integer values
    """

    def __init__(self):
        self.format = None


class IntegerTypeFormatEnum(Enum):
    INT32 = 'int32'
    INT64 = 'int64'


class NumberType (Type):
    """ floating point values
    """

    def __init__(self):
        self.format = None


class NumberTypeFormatEnum(Enum):
    FLOAT = 'float'
    DOUBLE = 'double'


class StringType (Type):
    """ integer values
    """

    def __init__(self):
        pass


class EnumType (Type):
    """ type for enum values - fixed value types
    """

    def __init__(self):
        self.values = []


class DateType (Type):
    """ type for date values
    """

    def __init__(self):
        pass


class DateTimeType (Type):
    """ type for timestamp values
    """

    def __init__(self):
        pass


class ComplexType (Type):
    """ complex type description
    """

    def __init__(self):
        self.domain = None
        self.source = None
        self.extendsType = None
        self.extendedBy = None
        self.referencedBy = None
        self.properties = None
        self.tags = []


class Property:
    """ a property of a type
    """

    def __init__(self):
        self.name = None
        self.isArray = None
        self.type = None
        self.tags = []


class Tag:
    """ a tag type
    """

    def __init__(self):
        self.name = None
        self.value = None


