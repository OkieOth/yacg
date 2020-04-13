# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Type:
    """ Dummy base class to implement strong typed references
    """

    def __init__(self):
        pass


class IntegerType (Type):
    """ integer values
    """

    def __init__(self):

        #: integer values
        self.format = None

        #: integer values
        self.default = None


class IntegerTypeFormatEnum(Enum):
    INT32 = 'int32'
    INT64 = 'int64'


class NumberType (Type):
    """ floating point values
    """

    def __init__(self):

        #: floating point values
        self.format = None

        #: floating point values
        self.default = None


class NumberTypeFormatEnum(Enum):
    FLOAT = 'float'
    DOUBLE = 'double'


class BooleanType (Type):
    """ boolean values
    """

    def __init__(self):

        #: boolean values
        self.default = None


class StringType (Type):
    """ integer values
    """

    def __init__(self):

        #: integer values
        self.default = None


class UuidType (Type):
    """ UUID values
    """

    def __init__(self):

        #: UUID values
        self.default = None


class EnumType (Type):
    """ type for enum values - fixed value types
    """

    def __init__(self):

        #: type for enum values - fixed value types
        self.name = None

        #: type for enum values - fixed value types
        self.domain = None

        #: type for enum values - fixed value types
        self.values = []

        #: type for enum values - fixed value types
        self.default = None


class DateType (Type):
    """ type for date values
    """

    def __init__(self):

        #: type for date values
        self.default = None


class DateTimeType (Type):
    """ type for timestamp values
    """

    def __init__(self):

        #: type for timestamp values
        self.default = None


class ComplexType (Type):
    """ complex type description
    """

    def __init__(self):

        #: complex type description
        self.name = None

        #: complex type description
        self.description = None

        #: complex type description
        self.domain = None

        #: complex type description
        self.source = None

        #: complex type description
        self.extendsType = None

        #: complex type description
        self.extendedBy = []

        #: complex type description
        self.referencedBy = []

        #: complex type description
        self.properties = []

        #: complex type description
        self.tags = []


class Property:
    """ a property of a type
    """

    def __init__(self):

        #: a property of a type
        self.name = None

        #: a property of a type
        self.isArray = None

        #: a property of a type
        self.type = None

        #: a property of a type
        self.tags = []

        #: a property of a type
        self.description = None


class Tag:
    """ a tag type
    """

    def __init__(self):

        #: a tag type
        self.name = None

        #: a tag type
        self.value = None


