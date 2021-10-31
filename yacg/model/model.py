# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Type:
    """ Dummy base class to implement strong typed references
    """

    def __init__(self, dictObj = None):
        if dictObj is None:
            pass
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return


class IntegerType (Type):
    """ integer values
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.format = IntegerTypeFormatEnum.valueForString(dictObj.get('format', None))

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


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

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.format = NumberTypeFormatEnum.valueForString(dictObj.get('format', None))

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


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

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

            #: boolean values
            self.default = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class StringType (Type):
    """ integer values
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

            #: integer values
            self.default = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class UuidType (Type):
    """ UUID values
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

            #: UUID values
            self.default = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class EnumType (Type):
    """ type for enum values - fixed value types
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.version = dictObj.get('version', None)

        self.name = dictObj.get('name', None)

        self.domain = dictObj.get('domain', None)

        self.source = dictObj.get('source', None)

        self.description = dictObj.get('description', None)

        arrayValues = dictObj.get('values', [])
        for elemValues in arrayValues:
            self.values.append(elemValues)

        self.default = dictObj.get('default', None)

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))


class Tag:
    """ a tag type
    """

    def __init__(self, dictObj = None):
        if dictObj is None:

            #: a tag type
            self.name = None

            #: a tag type
            self.value = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.value = dictObj.get('value', None)


class DateType (Type):
    """ type for date values
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


class DateTimeType (Type):
    """ type for timestamp values
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


class BytesType (Type):
    """ type for byte values, it will usually be rendered to a byte array
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

            #: type for byte values, it will usually be rendered to a byte array
            self.default = None
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class ComplexType (Type):
    """ complex type description
    """

    def __init__(self, dictObj = None):
        super(Type, self).__init__()
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.version = dictObj.get('version', None)

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        self.domain = dictObj.get('domain', None)

        self.source = dictObj.get('source', None)

        self.extendsType = ComplexType(dict.get('extendsType', None))

        arrayExtendedBy = dictObj.get('extendedBy', [])
        for elemExtendedBy in arrayExtendedBy:
            self.extendedBy.append(
                ComplexType(elemExtendedBy))

        arrayReferencedBy = dictObj.get('referencedBy', [])
        for elemReferencedBy in arrayReferencedBy:
            self.referencedBy.append(
                ComplexType(elemReferencedBy))

        arrayProperties = dictObj.get('properties', [])
        for elemProperties in arrayProperties:
            self.properties.append(
                Property(elemProperties))

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))


class Property:
    """ a property of a type
    """

    def __init__(self, dictObj = None):
        if dictObj is None:

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
        else:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.isArray = dictObj.get('isArray', False)

        self.arrayMinItems = dictObj.get('arrayMinItems', None)

        self.arrayMaxItems = dictObj.get('arrayMaxItems', None)

        self.arrayUniqueItems = dictObj.get('arrayUniqueItems', None)

        self.type = Type(dict.get('type', None))

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))

        self.description = dictObj.get('description', None)

        self.required = dictObj.get('required', False)

        self.ordinal = dictObj.get('ordinal', None)

        self.isKey = dictObj.get('isKey', False)

        self.isVisualKey = dictObj.get('isVisualKey', False)

        self.foreignKey = Type(dict.get('foreignKey', None))

        self.format = dictObj.get('format', None)


