# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

from enum import Enum


class Type:
    """Dummy base class to implement strong typed references
    """

    def __init__(self, dictObj=None):

        #: anchor to store codegen runtime data, for instance for the random data creation
        self.processing = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.processing is not None:
            ret["processing"] = self.processing
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.processing = dictObj.get('processing', None)


class ObjectType (Type):
    """Straight out of hell - a undefined object type
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        pass

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return


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



class IntegerType (Type):
    """integer values
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.format = None
        self.default = None
        self.minimum = None
        self.exclusiveMinimum = None
        self.maximum = None
        self.exclusiveMaximum = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.format is not None:
            ret["format"] = IntegerTypeFormatEnum.valueAsString(self.format)
        if self.default is not None:
            ret["default"] = self.default
        if self.minimum is not None:
            ret["minimum"] = self.minimum
        if self.exclusiveMinimum is not None:
            ret["exclusiveMinimum"] = self.exclusiveMinimum
        if self.maximum is not None:
            ret["maximum"] = self.maximum
        if self.exclusiveMaximum is not None:
            ret["exclusiveMaximum"] = self.exclusiveMaximum
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.format = IntegerTypeFormatEnum.valueForString(dictObj.get('format', None))

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



class NumberType (Type):
    """floating point values
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.format = None
        self.default = None
        self.minimum = None
        self.exclusiveMinimum = None
        self.maximum = None
        self.exclusiveMaximum = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.format is not None:
            ret["format"] = NumberTypeFormatEnum.valueAsString(self.format)
        if self.default is not None:
            ret["default"] = self.default
        if self.minimum is not None:
            ret["minimum"] = self.minimum
        if self.exclusiveMinimum is not None:
            ret["exclusiveMinimum"] = self.exclusiveMinimum
        if self.maximum is not None:
            ret["maximum"] = self.maximum
        if self.exclusiveMaximum is not None:
            ret["exclusiveMaximum"] = self.exclusiveMaximum
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.format = NumberTypeFormatEnum.valueForString(dictObj.get('format', None))

        self.default = dictObj.get('default', None)

        self.minimum = dictObj.get('minimum', None)

        self.exclusiveMinimum = dictObj.get('exclusiveMinimum', None)

        self.maximum = dictObj.get('maximum', None)

        self.exclusiveMaximum = dictObj.get('exclusiveMaximum', None)


class BooleanType (Type):
    """boolean values
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.default = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class StringType (Type):
    """integer values
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.default = None
        self.minLength = None
        self.maxLength = None
        self.pattern = None
        self.format = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        if self.minLength is not None:
            ret["minLength"] = self.minLength
        if self.maxLength is not None:
            ret["maxLength"] = self.maxLength
        if self.pattern is not None:
            ret["pattern"] = self.pattern
        if self.format is not None:
            ret["format"] = self.format
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)

        self.minLength = dictObj.get('minLength', None)

        self.maxLength = dictObj.get('maxLength', None)

        self.pattern = dictObj.get('pattern', None)

        self.format = dictObj.get('format', None)


class UuidType (Type):
    """UUID values
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.default = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class EnumTypeValuesMap:
    """additional enum values
    """

    def __init__(self, dictObj=None):
        pass

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return


class Tag:
    """a tag type
    """

    def __init__(self, dictObj=None):
        self.name = None
        self.value = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.value is not None:
            ret["value"] = self.value
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.value = dictObj.get('value', None)


class EnumType (Type):
    """type for enum values - fixed value types
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)

        #: is taken from the version entry of the file, optional
        self.version = None
        self.name = None

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None
        self.description = None

        #: only a string or numeric type make sense
        self.type = None
        self.numValues = []
        self.values = []

        #: additional enum values
        self.valuesMap = None
        self.default = None
        self.topLevelType = False

        #: additional flags to mark a type
        self.tags = []

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.version is not None:
            ret["version"] = self.version
        if self.name is not None:
            ret["name"] = self.name
        if self.domain is not None:
            ret["domain"] = self.domain
        if self.source is not None:
            ret["source"] = self.source
        if self.description is not None:
            ret["description"] = self.description
        if self.type is not None:
            ret["type"] = self.type.toDict()
        if (self.numValues is not None) and (len(self.numValues) > 0):
            ret["numValues"] = self.numValues
        if (self.values is not None) and (len(self.values) > 0):
            ret["values"] = self.values
        if (self.valuesMap is not None) and (len(self.valuesMap) > 0):
            ret["valuesMap"] = self.valuesMap
        if self.default is not None:
            ret["default"] = self.default
        if self.topLevelType is not None:
            ret["topLevelType"] = self.topLevelType
        if (self.tags is not None) and (len(self.tags) > 0):
            ret["tags"] = self.tags.toDict()
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.version = dictObj.get('version', None)

        self.name = dictObj.get('name', None)

        self.domain = dictObj.get('domain', None)

        self.source = dictObj.get('source', None)

        self.description = dictObj.get('description', None)

        subDictObj = dictObj.get('type', None)
        if subDictObj is not None:
            self.type = Type(subDictObj)

        arrayNumValues = dictObj.get('numValues', [])
        for elemNumValues in arrayNumValues:
            self.numValues.append(elemNumValues)

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


class DateType (Type):
    """type for date values
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.default = None
        self.minimum = None
        self.exclusiveMinimum = None
        self.maximum = None
        self.exclusiveMaximum = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        if self.minimum is not None:
            ret["minimum"] = self.minimum
        if self.exclusiveMinimum is not None:
            ret["exclusiveMinimum"] = self.exclusiveMinimum
        if self.maximum is not None:
            ret["maximum"] = self.maximum
        if self.exclusiveMaximum is not None:
            ret["exclusiveMaximum"] = self.exclusiveMaximum
        return ret


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
        Type.__init__(self)
        self.default = None
        self.minimum = None
        self.exclusiveMinimum = None
        self.maximum = None
        self.exclusiveMaximum = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        if self.minimum is not None:
            ret["minimum"] = self.minimum
        if self.exclusiveMinimum is not None:
            ret["exclusiveMinimum"] = self.exclusiveMinimum
        if self.maximum is not None:
            ret["maximum"] = self.maximum
        if self.exclusiveMaximum is not None:
            ret["exclusiveMaximum"] = self.exclusiveMaximum
        return ret


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
        Type.__init__(self)
        self.default = None
        self.minimum = None
        self.exclusiveMinimum = None
        self.maximum = None
        self.exclusiveMaximum = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        if self.minimum is not None:
            ret["minimum"] = self.minimum
        if self.exclusiveMinimum is not None:
            ret["exclusiveMinimum"] = self.exclusiveMinimum
        if self.maximum is not None:
            ret["maximum"] = self.maximum
        if self.exclusiveMaximum is not None:
            ret["exclusiveMaximum"] = self.exclusiveMaximum
        return ret


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
        Type.__init__(self)
        self.default = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class BytesType (Type):
    """type for byte values, it will usually be rendered to a byte array
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)
        self.default = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.default is not None:
            ret["default"] = self.default
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.default = dictObj.get('default', None)


class ComplexType (Type):
    """complex type description
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.version is not None:
            ret["version"] = self.version
        if self.name is not None:
            ret["name"] = self.name
        if self.description is not None:
            ret["description"] = self.description
        if self.domain is not None:
            ret["domain"] = self.domain
        if self.source is not None:
            ret["source"] = self.source
        if self.extendsType is not None:
            ret["extendsType"] = self.extendsType.toDict()
        if (self.extendedBy is not None) and (len(self.extendedBy) > 0):
            ret["extendedBy"] = self.extendedBy.toDict()
        if (self.referencedBy is not None) and (len(self.referencedBy) > 0):
            ret["referencedBy"] = self.referencedBy.toDict()
        if (self.properties is not None) and (len(self.properties) > 0):
            ret["properties"] = self.properties.toDict()
        if self.topLevelType is not None:
            ret["topLevelType"] = self.topLevelType
        if (self.tags is not None) and (len(self.tags) > 0):
            ret["tags"] = self.tags.toDict()
        return ret


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

        #: anchor to store codegen runtime data, for instance for the random data creation
        self.processing = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.isArray is not None:
            ret["isArray"] = self.isArray
        if self.arrayDimensions is not None:
            ret["arrayDimensions"] = self.arrayDimensions
        if (self.arrayConstraints is not None) and (len(self.arrayConstraints) > 0):
            ret["arrayConstraints"] = self.arrayConstraints.toDict()
        if self.type is not None:
            ret["type"] = self.type.toDict()
        if (self.tags is not None) and (len(self.tags) > 0):
            ret["tags"] = self.tags.toDict()
        if self.description is not None:
            ret["description"] = self.description
        if self.required is not None:
            ret["required"] = self.required
        if self.ordinal is not None:
            ret["ordinal"] = self.ordinal
        if self.isKey is not None:
            ret["isKey"] = self.isKey
        if self.isVisualKey is not None:
            ret["isVisualKey"] = self.isVisualKey
        if self.foreignKey is not None:
            ret["foreignKey"] = self.foreignKey.toDict()
        if self.format is not None:
            ret["format"] = self.format
        if self.processing is not None:
            ret["processing"] = self.processing
        return ret


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

        self.processing = dictObj.get('processing', None)


class DictionaryType (Type):
    """key/value dictionary type. Keys are always strings, the value type can be
    specified
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.version is not None:
            ret["version"] = self.version
        if self.name is not None:
            ret["name"] = self.name
        if self.description is not None:
            ret["description"] = self.description
        if self.domain is not None:
            ret["domain"] = self.domain
        if self.source is not None:
            ret["source"] = self.source
        if (self.referencedBy is not None) and (len(self.referencedBy) > 0):
            ret["referencedBy"] = self.referencedBy.toDict()
        if self.valueType is not None:
            ret["valueType"] = self.valueType.toDict()
        if self.topLevelType is not None:
            ret["topLevelType"] = self.topLevelType
        if (self.tags is not None) and (len(self.tags) > 0):
            ret["tags"] = self.tags.toDict()
        return ret


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


class ArrayConstraints:
    def __init__(self, dictObj=None):

        #: defined minimum of elements in the array/list
        self.arrayMinItems = None

        #: defined maximum of elements in the array/list
        self.arrayMaxItems = None

        #: the elements in the array/list have to be unique
        self.arrayUniqueItems = False

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.arrayMinItems is not None:
            ret["arrayMinItems"] = self.arrayMinItems
        if self.arrayMaxItems is not None:
            ret["arrayMaxItems"] = self.arrayMaxItems
        if self.arrayUniqueItems is not None:
            ret["arrayUniqueItems"] = self.arrayUniqueItems
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.arrayMinItems = dictObj.get('arrayMinItems', None)

        self.arrayMaxItems = dictObj.get('arrayMaxItems', None)

        self.arrayUniqueItems = dictObj.get('arrayUniqueItems', False)


class ArrayType (Type):
    """Array type
    """

    def __init__(self, dictObj=None):
        Type.__init__(self)

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.version is not None:
            ret["version"] = self.version
        if self.name is not None:
            ret["name"] = self.name
        if self.description is not None:
            ret["description"] = self.description
        if self.domain is not None:
            ret["domain"] = self.domain
        if self.source is not None:
            ret["source"] = self.source
        if (self.referencedBy is not None) and (len(self.referencedBy) > 0):
            ret["referencedBy"] = self.referencedBy.toDict()
        if self.itemsType is not None:
            ret["itemsType"] = self.itemsType.toDict()
        if self.topLevelType is not None:
            ret["topLevelType"] = self.topLevelType
        if (self.tags is not None) and (len(self.tags) > 0):
            ret["tags"] = self.tags.toDict()
        if (self.arrayConstraints is not None) and (len(self.arrayConstraints) > 0):
            ret["arrayConstraints"] = self.arrayConstraints.toDict()
        if self.arrayDimensions is not None:
            ret["arrayDimensions"] = self.arrayDimensions
        return ret


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


class ForeignKey:
    """Type describes the reference of a property to another field in the model
    """

    def __init__(self, dictObj=None):
        self.type = None
        self.propertyName = None
        self.property = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.type is not None:
            ret["type"] = self.type.toDict()
        if self.propertyName is not None:
            ret["propertyName"] = self.propertyName
        if self.property is not None:
            ret["property"] = self.property.toDict()
        return ret


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


