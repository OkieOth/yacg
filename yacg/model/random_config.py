# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class RandomDataTypeConf:
    """can put on schema types to include them in the random data generation
    """

    def __init__(self, dictObj=None):

        #: how many elements of that type should be at minimum generated
        self.randMinElemCount = None

        #: how many elements of that type should be at maximum generated
        self.randMaxElemCount = None

        #: number of elements of that type should be at minimum generated
        self.randElemCount = None

        self.typeDepth = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randMinElemCount = dictObj.get('randMinElemCount', None)

        self.randMaxElemCount = dictObj.get('randMaxElemCount', None)

        self.randElemCount = dictObj.get('randElemCount', None)

        self.typeDepth = dictObj.get('typeDepth', None)


class RandomDataPropertyConf:
    """can put on schema properties to taylormade the random data generation
    """

    def __init__(self, dictObj=None):

        #: set this on a property to 'true' and no random data are generated for it
        self.ingnore = None

        #: in case the property contains an array, this specifies the random data handling of the array
        self.arrayConf = None

        #: values used to put randomly on the attrib, type is not close checked
        self.valuePool = None

        #: taylormade configuration for the property type
        self.typeConf = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.ingnore = dictObj.get('ingnore', None)

        subDictObj = dictObj.get('arrayConf', None)
        if subDictObj is not None:
            self.arrayConf = RandomArrayConf(subDictObj)

        self.valuePool = dictObj.get('valuePool', None)

        subDictObj = dictObj.get('typeConf', None)
        if subDictObj is not None:
            self.typeConf = RandomPropertyTypeConf(subDictObj)


class RandomArrayConf:
    """Processing information to create random arrays
    """

    def __init__(self, dictObj=None):

        #: how many elements of that type should be at minimum generated
        self.randMinElemCount = None

        #: how many elements of that type should be at maximum generated
        self.randMaxElemCount = None

        #: number of elements of that type should be at minimum generated
        self.randElemCount = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randMinElemCount = dictObj.get('randMinElemCount', None)

        self.randMaxElemCount = dictObj.get('randMaxElemCount', None)

        self.randElemCount = dictObj.get('randElemCount', None)


class RandomPropertyTypeConf:
    def __init__(self, dictObj=None):

        self.complexTypeConf = None

        self.stringTypeConf = None

        self.numTypeConf = None

        self.dateTypeConf = None

        self.timeTypeConf = None

        self.durationTypeConf = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        subDictObj = dictObj.get('complexTypeConf', None)
        if subDictObj is not None:
            self.complexTypeConf = RandomComplexTypeConf(subDictObj)

        subDictObj = dictObj.get('stringTypeConf', None)
        if subDictObj is not None:
            self.stringTypeConf = RandomStringTypeConf(subDictObj)

        subDictObj = dictObj.get('numTypeConf', None)
        if subDictObj is not None:
            self.numTypeConf = RandomNumTypeConf(subDictObj)

        subDictObj = dictObj.get('dateTypeConf', None)
        if subDictObj is not None:
            self.dateTypeConf = RandomDateTypeConf(subDictObj)

        subDictObj = dictObj.get('timeTypeConf', None)
        if subDictObj is not None:
            self.timeTypeConf = RandomTimeTypeConf(subDictObj)

        subDictObj = dictObj.get('durationTypeConf', None)
        if subDictObj is not None:
            self.durationTypeConf = RandomDurationTypeConf(subDictObj)


class RandomComplexTypeConf:
    """Constraints to generate random values of a complex type
    """

    def __init__(self, dictObj=None):

        #: defines for complex types how many levels of childs should be followed
        self.typeDepth = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.typeDepth = dictObj.get('typeDepth', None)


class RandomStringTypeConf:
    """Constraints to generate random string values
    """

    def __init__(self, dictObj=None):

        self.strType = None

        self.maxLength = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.strType = RandomStringTypeConfStrTypeEnum.valueForString(dictObj.get('strType', None))

        self.maxLength = dictObj.get('maxLength', None)


class RandomNumTypeConf:
    """Constraints to generate random numeric values
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


class RandomDateTypeConf:
    """Constraints to generate random date values, used for dates and date-times
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


class RandomTimeTypeConf:
    """Constraints to generate random time values
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


class RandomDurationTypeConf:
    """Constraints to generate random duration values
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


class RandomStringTypeConfStrTypeEnum(Enum):
    NAME = 'NAME'
    ADDRESS = 'ADDRESS'
    EMAIL = 'EMAIL'
    URL = 'URL'
    PHONE = 'PHONE'
    COUNTRY = 'COUNTRY'
    TEXT = 'TEXT'
    SENTENCE = 'SENTENCE'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'name':
            return RandomStringTypeConfStrTypeEnum.NAME
        elif lowerStringValue == 'address':
            return RandomStringTypeConfStrTypeEnum.ADDRESS
        elif lowerStringValue == 'email':
            return RandomStringTypeConfStrTypeEnum.EMAIL
        elif lowerStringValue == 'url':
            return RandomStringTypeConfStrTypeEnum.URL
        elif lowerStringValue == 'phone':
            return RandomStringTypeConfStrTypeEnum.PHONE
        elif lowerStringValue == 'country':
            return RandomStringTypeConfStrTypeEnum.COUNTRY
        elif lowerStringValue == 'text':
            return RandomStringTypeConfStrTypeEnum.TEXT
        elif lowerStringValue == 'sentence':
            return RandomStringTypeConfStrTypeEnum.SENTENCE
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == RandomStringTypeConfStrTypeEnum.NAME:
            return 'NAME'
        elif enumValue == RandomStringTypeConfStrTypeEnum.ADDRESS:
            return 'ADDRESS'
        elif enumValue == RandomStringTypeConfStrTypeEnum.EMAIL:
            return 'EMAIL'
        elif enumValue == RandomStringTypeConfStrTypeEnum.URL:
            return 'URL'
        elif enumValue == RandomStringTypeConfStrTypeEnum.PHONE:
            return 'PHONE'
        elif enumValue == RandomStringTypeConfStrTypeEnum.COUNTRY:
            return 'COUNTRY'
        elif enumValue == RandomStringTypeConfStrTypeEnum.TEXT:
            return 'TEXT'
        elif enumValue == RandomStringTypeConfStrTypeEnum.SENTENCE:
            return 'SENTENCE'
        else:
            return ''



