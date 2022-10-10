# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Type:
    """Dummy base class to implement strong typed references
    """

    def __init__(self, dictObj=None):
        pass

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return


class ObjectType (Type):
    """Straight out of hell - a undefined object type
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()
        pass

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return


class IntegerType (Type):
    """integer values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.format = None

        self.default = None

        self.minimum = None

        self.exclusiveMinimum = None

        self.maximum = None

        self.exclusiveMaximum = None

        if dictObj is not None:
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
    """floating point values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.format = None

        self.default = None

        self.minimum = None

        self.exclusiveMinimum = None

        self.maximum = None

        self.exclusiveMaximum = None

        if dictObj is not None:
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
    """boolean values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class StringType (Type):
    """integer values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        self.minLength = None

        self.maxLength = None

        self.pattern = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)

        self.minLength = dictObj.get('minLength', None)

        self.maxLength = dictObj.get('maxLength', None)

        self.pattern = dictObj.get('pattern', None)


class UuidType (Type):
    """UUID values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class EnumType (Type):
    """type for enum values - fixed value types
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        #: is taken from the version entry of the file, optional
        self.version = None

        self.name = None

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None

        self.description = None

        self.values = []

        #: additional enum values
        self.valuesMap = None

        self.default = None

        self.topLevelType = False

        #: additional flags to mark a type
        self.tags = []

        if dictObj is not None:
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

        self.valuesMap = dictObj.get('valuesMap', None)

        self.default = dictObj.get('default', None)

        self.topLevelType = dictObj.get('topLevelType', False)

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))


class Tag:
    """a tag type
    """

    def __init__(self, dictObj=None):

        self.name = None

        self.value = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.value = dictObj.get('value', None)


class DateType (Type):
    """type for date values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        self.minimum = None

        self.exclusiveMinimum = None

        self.maximum = None

        self.exclusiveMaximum = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


class TimeType (Type):
    """type for time values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        self.minimum = None

        self.exclusiveMinimum = None

        self.maximum = None

        self.exclusiveMaximum = None

        if dictObj is not None:
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
    """type for timestamp values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        self.minimum = None

        self.exclusiveMinimum = None

        self.maximum = None

        self.exclusiveMaximum = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


class DurationType (Type):
    """type for date values
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class BytesType (Type):
    """type for byte values, it will usually be rendered to a byte array
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        self.default = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class ComplexType (Type):
    """complex type description
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        #: is taken from the version entry of the file, optional
        self.version = None

        self.name = None

        self.description = None

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None

        #: in case of inheritance points this attrib to the base type
        self.extendsType = None

        #: list of types that extend this type
        self.extendedBy = []

        #: types that hold attribute references to that type
        self.referencedBy = []

        #: properties of that type
        self.properties = []

        self.topLevelType = False

        #: additional flags to mark a type
        self.tags = []

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.version = dictObj.get('version', None)

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        self.domain = dictObj.get('domain', None)

        self.source = dictObj.get('source', None)

        subDictObj = dictObj.get('extendsType', None)
        if subDictObj is not None:
            self.extendsType = ComplexType(subDictObj)

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

        self.topLevelType = dictObj.get('topLevelType', False)

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))


class Property:
    """a property of a type
    """

    def __init__(self, dictObj=None):

        #: type unique identifier
        self.name = None

        #: true - if the property is an array
        self.isArray = False

        #: if isArray true you can specify here the number of the array dimensions
        self.arrayDimensions = None

        self.arrayConstraints = []

        #: either a basic or a complex type
        self.type = None

        #: additional flags to mark a property
        self.tags = []

        #: optional description from the model file
        self.description = None

        #: is set to true if the attribute is marked as required in the model
        self.required = False

        #: ordinal number/position of that attribute. Used in protobuf e.g.
        self.ordinal = None

        #: is set to true if the attribute is the key of the type
        self.isKey = False

        #: is set to true if the attribute is some kind of a name, caption, label or anther kind of visual key
        self.isVisualKey = False

        #: content of the 'x-ref' entry of a property, points to an implicit referenced type, e.g. for IDs
        self.foreignKey = None

        #: holds the original 'format' value from the schema
        self.format = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.isArray = dictObj.get('isArray', False)

        self.arrayDimensions = dictObj.get('arrayDimensions', None)

        arrayArrayConstraints = dictObj.get('arrayConstraints', [])
        for elemArrayConstraints in arrayArrayConstraints:
            self.arrayConstraints.append(
                ArrayConstraints(elemArrayConstraints))

        subDictObj = dictObj.get('type', None)
        if subDictObj is not None:
            self.type = Type(subDictObj)

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))

        self.description = dictObj.get('description', None)

        self.required = dictObj.get('required', False)

        self.ordinal = dictObj.get('ordinal', None)

        self.isKey = dictObj.get('isKey', False)

        self.isVisualKey = dictObj.get('isVisualKey', False)

        subDictObj = dictObj.get('foreignKey', None)
        if subDictObj is not None:
            self.foreignKey = Type(subDictObj)

        self.format = dictObj.get('format', None)


class DictionaryType (Type):
    """key/value dictionary type. Keys are always strings, the value type can be
    specified
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        #: is taken from the version entry of the file, optional
        self.version = None

        self.name = None

        self.description = None

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None

        #: types that hold attribute references to that type
        self.referencedBy = []

        #: either a basic or a complex type
        self.valueType = None

        self.topLevelType = False

        #: additional flags to mark a type
        self.tags = []

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.version = dictObj.get('version', None)

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        self.domain = dictObj.get('domain', None)

        self.source = dictObj.get('source', None)

        arrayReferencedBy = dictObj.get('referencedBy', [])
        for elemReferencedBy in arrayReferencedBy:
            self.referencedBy.append(
                ComplexType(elemReferencedBy))

        subDictObj = dictObj.get('valueType', None)
        if subDictObj is not None:
            self.valueType = Type(subDictObj)

        self.topLevelType = dictObj.get('topLevelType', False)

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))


class ArrayType (Type):
    """Array type
    """

    def __init__(self, dictObj=None):
        super(Type, self).__init__()

        #: is taken from the version entry of the file, optional
        self.version = None

        self.name = None

        self.description = None

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None

        #: types that hold attribute references to that type
        self.referencedBy = []

        #: either a basic or a complex type
        self.itemsType = None

        self.topLevelType = False

        #: additional flags to mark a type
        self.tags = []

        self.arrayConstraints = []

        #: if isArray true you can specify here the number of the array dimensions
        self.arrayDimensions = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.version = dictObj.get('version', None)

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        self.domain = dictObj.get('domain', None)

        self.source = dictObj.get('source', None)

        arrayReferencedBy = dictObj.get('referencedBy', [])
        for elemReferencedBy in arrayReferencedBy:
            self.referencedBy.append(
                ComplexType(elemReferencedBy))

        subDictObj = dictObj.get('itemsType', None)
        if subDictObj is not None:
            self.itemsType = Type(subDictObj)

        self.topLevelType = dictObj.get('topLevelType', False)

        arrayTags = dictObj.get('tags', [])
        for elemTags in arrayTags:
            self.tags.append(
                Tag(elemTags))

        arrayArrayConstraints = dictObj.get('arrayConstraints', [])
        for elemArrayConstraints in arrayArrayConstraints:
            self.arrayConstraints.append(
                ArrayConstraints(elemArrayConstraints))

        self.arrayDimensions = dictObj.get('arrayDimensions', None)


class ArrayConstraints:
    def __init__(self, dictObj=None):

        #: defined minimum of elements in the array/list
        self.arrayMinItems = None

        #: defined maximum of elements in the array/list
        self.arrayMaxItems = None

        #: the elements in the array/list have to be unique
        self.arrayUniqueItems = False

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.arrayMinItems = dictObj.get('arrayMinItems', None)

        self.arrayMaxItems = dictObj.get('arrayMaxItems', None)

        self.arrayUniqueItems = dictObj.get('arrayUniqueItems', False)


class ForeignKey:
    """Type describes the reference of a property to another field in the model
    """

    def __init__(self, dictObj=None):

        self.type = None

        self.propertyName = None

        self.property = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        subDictObj = dictObj.get('type', None)
        if subDictObj is not None:
            self.type = Type(subDictObj)

        self.propertyName = dictObj.get('propertyName', None)

        subDictObj = dictObj.get('property', None)
        if subDictObj is not None:
            self.property = Property(subDictObj)


