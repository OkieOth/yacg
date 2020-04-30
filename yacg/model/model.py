# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Type:
    """ Dummy base class to implement strong typed references
    """

    def __init__(self):
        pass

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Type()
        return obj


class IntegerType (Type):
    """ integer values
    """

    def __init__(self):

        #: integer values
        self.format = None

        #: integer values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = IntegerType()

        obj.format = IntegerTypeFormatEnum.valueForString(dict.get('format', None))

        obj.default = dict.get('default', None)
        return obj


class IntegerTypeFormatEnum(Enum):
    INT32 = 'int32'
    INT64 = 'int64'

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        elif stringValue == 'int32':
            return IntegerTypeFormatEnum.INT32
        elif stringValue == 'int64':
            return IntegerTypeFormatEnum.INT64
        else:
            return None


class NumberType (Type):
    """ floating point values
    """

    def __init__(self):

        #: floating point values
        self.format = None

        #: floating point values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = NumberType()

        obj.format = NumberTypeFormatEnum.valueForString(dict.get('format', None))

        obj.default = dict.get('default', None)
        return obj


class NumberTypeFormatEnum(Enum):
    FLOAT = 'float'
    DOUBLE = 'double'

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        elif stringValue == 'float':
            return NumberTypeFormatEnum.FLOAT
        elif stringValue == 'double':
            return NumberTypeFormatEnum.DOUBLE
        else:
            return None


class BooleanType (Type):
    """ boolean values
    """

    def __init__(self):

        #: boolean values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = BooleanType()

        obj.default = dict.get('default', None)
        return obj


class StringType (Type):
    """ integer values
    """

    def __init__(self):

        #: integer values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = StringType()

        obj.default = dict.get('default', None)
        return obj


class UuidType (Type):
    """ UUID values
    """

    def __init__(self):

        #: UUID values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = UuidType()

        obj.default = dict.get('default', None)
        return obj


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

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = EnumType()

        obj.name = dict.get('name', None)

        obj.domain = dict.get('domain', None)

        arrayValues = dict.get('values', [])
        for elemValues in arrayValues:
            obj.values.append(elemValues)

        obj.default = dict.get('default', None)
        return obj


class DateType (Type):
    """ type for date values
    """

    def __init__(self):

        #: type for date values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = DateType()

        obj.default = dict.get('default', None)
        return obj


class DateTimeType (Type):
    """ type for timestamp values
    """

    def __init__(self):

        #: type for timestamp values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = DateTimeType()

        obj.default = dict.get('default', None)
        return obj


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

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = ComplexType()

        obj.name = dict.get('name', None)

        obj.description = dict.get('description', None)

        obj.domain = dict.get('domain', None)

        obj.source = dict.get('source', None)

        obj.extendsType = ComplexType.dictToObject(dict.get('extendsType', None))

        arrayExtendedBy = dict.get('extendedBy', [])
        for elemExtendedBy in arrayExtendedBy:
            obj.extendedBy.append(
                ComplexType.dictToObject(elemExtendedBy))

        arrayReferencedBy = dict.get('referencedBy', [])
        for elemReferencedBy in arrayReferencedBy:
            obj.referencedBy.append(
                ComplexType.dictToObject(elemReferencedBy))

        arrayProperties = dict.get('properties', [])
        for elemProperties in arrayProperties:
            obj.properties.append(
                Property.dictToObject(elemProperties))

        arrayTags = dict.get('tags', [])
        for elemTags in arrayTags:
            obj.tags.append(
                Tag.dictToObject(elemTags))
        return obj


class Property:
    """ a property of a type
    """

    def __init__(self):

        #: a property of a type
        self.name = None

        #: a property of a type
        self.isArray = False

        #: a property of a type
        self.type = None

        #: a property of a type
        self.tags = []

        #: a property of a type
        self.description = None

        #: a property of a type
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Property()

        obj.name = dict.get('name', None)

        obj.isArray = dict.get('isArray', None)

        obj.type = Type.dictToObject(dict.get('type', None))

        arrayTags = dict.get('tags', [])
        for elemTags in arrayTags:
            obj.tags.append(
                Tag.dictToObject(elemTags))

        obj.description = dict.get('description', None)

        obj.default = dict.get('default', None)
        return obj


class Tag:
    """ a tag type
    """

    def __init__(self):

        #: a tag type
        self.name = None

        #: a tag type
        self.value = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Tag()

        obj.name = dict.get('name', None)

        obj.value = dict.get('value', None)
        return obj


