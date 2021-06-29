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
        obj = cls()
        return obj


class IntegerType (Type):
    """ integer values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: integer values
        self.format = None

        #: integer values
        self.default = None

        #: integer values
        self.minimum = None

        #: integer values
        self.exclusiveMinimum = None

        #: integer values
        self.maximum = None

        #: integer values
        self.exclusiveMaximum = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.format = IntegerTypeFormatEnum.valueForString(dict.get('format', None))

        obj.default = dict.get('default', None)

        obj.minimum = dict.get('minimum', None)

        obj.exclusiveMinimum = dict.get('exclusiveMinimum', None)

        obj.maximum = dict.get('maximum', None)

        obj.exclusiveMaximum = dict.get('exclusiveMaximum', None)
        return obj


class IntegerTypeFormatEnum(Enum):
    INT32 = 'int32'
    INT64 = 'int64'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'int32':
            return IntegerTypeFormatEnum.INT32
        elif lowerStringValue == 'int64':
            return IntegerTypeFormatEnum.INT64
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == IntegerTypeFormatEnum.INT32:
            return 'int32'
        elif enumValue == IntegerTypeFormatEnum.INT64:
            return 'int64'
        else:
            return ''



class NumberType (Type):
    """ floating point values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: floating point values
        self.format = None

        #: floating point values
        self.default = None

        #: floating point values
        self.minimum = None

        #: floating point values
        self.exclusiveMinimum = None

        #: floating point values
        self.maximum = None

        #: floating point values
        self.exclusiveMaximum = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.format = NumberTypeFormatEnum.valueForString(dict.get('format', None))

        obj.default = dict.get('default', None)

        obj.minimum = dict.get('minimum', None)

        obj.exclusiveMinimum = dict.get('exclusiveMinimum', None)

        obj.maximum = dict.get('maximum', None)

        obj.exclusiveMaximum = dict.get('exclusiveMaximum', None)
        return obj


class NumberTypeFormatEnum(Enum):
    FLOAT = 'float'
    DOUBLE = 'double'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'float':
            return NumberTypeFormatEnum.FLOAT
        elif lowerStringValue == 'double':
            return NumberTypeFormatEnum.DOUBLE
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == NumberTypeFormatEnum.FLOAT:
            return 'float'
        elif enumValue == NumberTypeFormatEnum.DOUBLE:
            return 'double'
        else:
            return ''



class BooleanType (Type):
    """ boolean values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: boolean values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.default = dict.get('default', None)
        return obj


class StringType (Type):
    """ integer values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: integer values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.default = dict.get('default', None)
        return obj


class UuidType (Type):
    """ UUID values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: UUID values
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.default = dict.get('default', None)
        return obj


class EnumType (Type):
    """ type for enum values - fixed value types
    """

    def __init__(self):
        super(Type, self).__init__()

        #: type for enum values - fixed value types
        self.version = None

        #: type for enum values - fixed value types
        self.name = None

        #: type for enum values - fixed value types
        self.domain = None

        #: type for enum values - fixed value types
        self.source = None

        #: type for enum values - fixed value types
        self.description = None

        #: type for enum values - fixed value types
        self.values = []

        #: type for enum values - fixed value types
        self.default = None

        #: type for enum values - fixed value types
        self.tags = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.version = dict.get('version', None)

        obj.name = dict.get('name', None)

        obj.domain = dict.get('domain', None)

        obj.source = dict.get('source', None)

        obj.description = dict.get('description', None)

        arrayValues = dict.get('values', [])
        for elemValues in arrayValues:
            obj.values.append(elemValues)

        obj.default = dict.get('default', None)

        arrayTags = dict.get('tags', [])
        for elemTags in arrayTags:
            obj.tags.append(
                Tag.dictToObject(elemTags))
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
        obj = cls()

        obj.name = dict.get('name', None)

        obj.value = dict.get('value', None)
        return obj


class DateType (Type):
    """ type for date values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: type for date values
        self.default = None

        #: type for date values
        self.minimum = None

        #: type for date values
        self.exclusiveMinimum = None

        #: type for date values
        self.maximum = None

        #: type for date values
        self.exclusiveMaximum = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.default = dict.get('default', None)

        obj.minimum = dict.get('minimum', None)

        obj.exclusiveMinimum = dict.get('exclusiveMinimum', None)

        obj.maximum = dict.get('maximum', None)

        obj.exclusiveMaximum = dict.get('exclusiveMaximum', None)
        return obj


class DateTimeType (Type):
    """ type for timestamp values
    """

    def __init__(self):
        super(Type, self).__init__()

        #: type for timestamp values
        self.default = None

        #: type for timestamp values
        self.minimum = None

        #: type for timestamp values
        self.exclusiveMinimum = None

        #: type for timestamp values
        self.maximum = None

        #: type for timestamp values
        self.exclusiveMaximum = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.default = dict.get('default', None)

        obj.minimum = dict.get('minimum', None)

        obj.exclusiveMinimum = dict.get('exclusiveMinimum', None)

        obj.maximum = dict.get('maximum', None)

        obj.exclusiveMaximum = dict.get('exclusiveMaximum', None)
        return obj


class BytesType (Type):
    """ type for byte values, it will usually be rendered to a byte array
    """

    def __init__(self):
        super(Type, self).__init__()

        #: type for byte values, it will usually be rendered to a byte array
        self.default = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.default = dict.get('default', None)
        return obj


class ComplexType (Type):
    """ complex type description
    """

    def __init__(self):
        super(Type, self).__init__()

        #: complex type description
        self.version = None

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
        obj = cls()

        obj.version = dict.get('version', None)

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
        self.arrayMinItems = None

        #: a property of a type
        self.arrayMaxItems = None

        #: a property of a type
        self.arrayUniqueItems = None

        #: a property of a type
        self.type = None

        #: a property of a type
        self.tags = []

        #: a property of a type
        self.description = None

        #: a property of a type
        self.required = False

        #: a property of a type
        self.ordinal = None

        #: a property of a type
        self.isKey = False

        #: a property of a type
        self.isVisualKey = False

        #: a property of a type
        self.foreignKey = None

        #: a property of a type
        self.format = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.name = dict.get('name', None)

        obj.isArray = dict.get('isArray', False)

        obj.arrayMinItems = dict.get('arrayMinItems', None)

        obj.arrayMaxItems = dict.get('arrayMaxItems', None)

        obj.arrayUniqueItems = dict.get('arrayUniqueItems', None)

        obj.type = Type.dictToObject(dict.get('type', None))

        arrayTags = dict.get('tags', [])
        for elemTags in arrayTags:
            obj.tags.append(
                Tag.dictToObject(elemTags))

        obj.description = dict.get('description', None)

        obj.required = dict.get('required', False)

        obj.ordinal = dict.get('ordinal', None)

        obj.isKey = dict.get('isKey', False)

        obj.isVisualKey = dict.get('isVisualKey', False)

        obj.foreignKey = Type.dictToObject(dict.get('foreignKey', None))

        obj.format = dict.get('format', None)
        return obj


