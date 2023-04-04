# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

from enum import Enum


class RamdonDefaultConfig:
    def __init__(self, dictObj=None):

        self.defaultElemCount = None

        self.defaultTypeDepth = 10

        self.defaultMinArrayElemCount = None

        self.defaultMaxArrayElemCount = None

        self.defaultMinDate = None

        self.defaultMaxDate = None

        #: 0 - always a value, 1 - 50 % empty, 2 - 75 % empty, 3 - 88% empty
        self.defaultProbabilityToBeEmpty = 1

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.defaultElemCount is not None:
            ret["defaultElemCount"] = self.defaultElemCount
        if self.defaultTypeDepth is not None:
            ret["defaultTypeDepth"] = self.defaultTypeDepth
        if self.defaultMinArrayElemCount is not None:
            ret["defaultMinArrayElemCount"] = self.defaultMinArrayElemCount
        if self.defaultMaxArrayElemCount is not None:
            ret["defaultMaxArrayElemCount"] = self.defaultMaxArrayElemCount
        if self.defaultMinDate is not None:
            ret["defaultMinDate"] = self.defaultMinDate
        if self.defaultMaxDate is not None:
            ret["defaultMaxDate"] = self.defaultMaxDate
        if self.defaultProbabilityToBeEmpty is not None:
            ret["defaultProbabilityToBeEmpty"] = self.defaultProbabilityToBeEmpty
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "defaultElemCount":
            self.defaultElemCount = value
        if attribName == "defaultTypeDepth":
            self.defaultTypeDepth = value
        if attribName == "defaultMinArrayElemCount":
            self.defaultMinArrayElemCount = value
        if attribName == "defaultMaxArrayElemCount":
            self.defaultMaxArrayElemCount = value
        if attribName == "defaultMinDate":
            self.defaultMinDate = value
        if attribName == "defaultMaxDate":
            self.defaultMaxDate = value
        if attribName == "defaultProbabilityToBeEmpty":
            self.defaultProbabilityToBeEmpty = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.defaultElemCount = dictObj.get('defaultElemCount', None)

        self.defaultTypeDepth = dictObj.get('defaultTypeDepth', 10)

        self.defaultMinArrayElemCount = dictObj.get('defaultMinArrayElemCount', None)

        self.defaultMaxArrayElemCount = dictObj.get('defaultMaxArrayElemCount', None)

        self.defaultMinDate = dictObj.get('defaultMinDate', None)

        self.defaultMaxDate = dictObj.get('defaultMaxDate', None)

        self.defaultProbabilityToBeEmpty = dictObj.get('defaultProbabilityToBeEmpty', 1)


def createRamdonDefaultConfigFromFlatDict(flatDict={}):
    ret = RamdonDefaultConfig()
    for key, value in flatDict.items():
        if key == "defaultElemCount":
            ret.defaultElemCount = value
        if key == "defaultTypeDepth":
            ret.defaultTypeDepth = value
        if key == "defaultMinArrayElemCount":
            ret.defaultMinArrayElemCount = value
        if key == "defaultMaxArrayElemCount":
            ret.defaultMaxArrayElemCount = value
        if key == "defaultMinDate":
            ret.defaultMinDate = value
        if key == "defaultMaxDate":
            ret.defaultMaxDate = value
        if key == "defaultProbabilityToBeEmpty":
            ret.defaultProbabilityToBeEmpty = value
    return ret

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

        self.randComplexTypeConf = None

        #: in case the type is an array, this specifies the random data handling of the array
        self.randArrayConf = None

        #: in case the is an dictionary, this specifies the random data handling of the dictionary
        self.randDictTypeConf = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.randMinElemCount is not None:
            ret["randMinElemCount"] = self.randMinElemCount
        if self.randMaxElemCount is not None:
            ret["randMaxElemCount"] = self.randMaxElemCount
        if self.randElemCount is not None:
            ret["randElemCount"] = self.randElemCount
        if self.randComplexTypeConf is not None:
            ret["randComplexTypeConf"] = self.randComplexTypeConf.toDict()
        if self.randArrayConf is not None:
            ret["randArrayConf"] = self.randArrayConf.toDict()
        if self.randDictTypeConf is not None:
            ret["randDictTypeConf"] = self.randDictTypeConf.toDict()
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "randMinElemCount":
            self.randMinElemCount = value
        if attribName == "randMaxElemCount":
            self.randMaxElemCount = value
        if attribName == "randElemCount":
            self.randElemCount = value
        self.randComplexTypeConf.initFlatValue(attribName, value)
        self.randArrayConf.initFlatValue(attribName, value)
        self.randDictTypeConf.initFlatValue(attribName, value)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randMinElemCount = dictObj.get('randMinElemCount', None)

        self.randMaxElemCount = dictObj.get('randMaxElemCount', None)

        self.randElemCount = dictObj.get('randElemCount', None)

        subDictObj = dictObj.get('randComplexTypeConf', None)
        if subDictObj is not None:
            self.randComplexTypeConf = RandomComplexTypeConf(subDictObj)

        subDictObj = dictObj.get('randArrayConf', None)
        if subDictObj is not None:
            self.randArrayConf = RandomArrayConf(subDictObj)

        subDictObj = dictObj.get('randDictTypeConf', None)
        if subDictObj is not None:
            self.randDictTypeConf = RandomDictConf(subDictObj)


def createRandomDataTypeConfFromFlatDict(flatDict={}):
    ret = RandomDataTypeConf()
    for key, value in flatDict.items():
        if key == "randMinElemCount":
            ret.randMinElemCount = value
        if key == "randMaxElemCount":
            ret.randMaxElemCount = value
        if key == "randElemCount":
            ret.randElemCount = value
        ret.randComplexTypeConf.initFlatValue(key, value)
        ret.randArrayConf.initFlatValue(key, value)
        ret.randDictTypeConf.initFlatValue(key, value)
    return ret

class RandomComplexTypeConf:
    """Constraints to generate random values of a complex type
    """

    def __init__(self, dictObj=None):

        #: defines for complex types how many levels of childs should be followed
        self.typeDepth = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.typeDepth is not None:
            ret["typeDepth"] = self.typeDepth
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "typeDepth":
            self.typeDepth = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.typeDepth = dictObj.get('typeDepth', None)


def createRandomComplexTypeConfFromFlatDict(flatDict={}):
    ret = RandomComplexTypeConf()
    for key, value in flatDict.items():
        if key == "typeDepth":
            ret.typeDepth = value
    return ret

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

    def toDict(self):
        ret = {}
        if self.randMinElemCount is not None:
            ret["randMinElemCount"] = self.randMinElemCount
        if self.randMaxElemCount is not None:
            ret["randMaxElemCount"] = self.randMaxElemCount
        if self.randElemCount is not None:
            ret["randElemCount"] = self.randElemCount
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "randMinElemCount":
            self.randMinElemCount = value
        if attribName == "randMaxElemCount":
            self.randMaxElemCount = value
        if attribName == "randElemCount":
            self.randElemCount = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randMinElemCount = dictObj.get('randMinElemCount', None)

        self.randMaxElemCount = dictObj.get('randMaxElemCount', None)

        self.randElemCount = dictObj.get('randElemCount', None)


def createRandomArrayConfFromFlatDict(flatDict={}):
    ret = RandomArrayConf()
    for key, value in flatDict.items():
        if key == "randMinElemCount":
            ret.randMinElemCount = value
        if key == "randMaxElemCount":
            ret.randMaxElemCount = value
        if key == "randElemCount":
            ret.randElemCount = value
    return ret

class RandomDictConf:
    """Processing information to create random dictionaries
    """

    def __init__(self, dictObj=None):

        #: how many elements of that type should be at minimum generated
        self.randMinKeyCount = None

        #: how many elements of that type should be at maximum generated
        self.randMaxKeyCount = None

        #: number of elements of that type should be at minimum generated
        self.randKeyCount = None

        #: minimum length of dictionary key names
        self.randKeyMinLen = 4

        #: maximum length of dictionary key names
        self.randKeyMaxLen = 10

        self.keyPool = []

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.randMinKeyCount is not None:
            ret["randMinKeyCount"] = self.randMinKeyCount
        if self.randMaxKeyCount is not None:
            ret["randMaxKeyCount"] = self.randMaxKeyCount
        if self.randKeyCount is not None:
            ret["randKeyCount"] = self.randKeyCount
        if self.randKeyMinLen is not None:
            ret["randKeyMinLen"] = self.randKeyMinLen
        if self.randKeyMaxLen is not None:
            ret["randKeyMaxLen"] = self.randKeyMaxLen
        if (self.keyPool is not None) and (len(self.keyPool) > 0):
            ret["keyPool"] = self.keyPool
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "randMinKeyCount":
            self.randMinKeyCount = value
        if attribName == "randMaxKeyCount":
            self.randMaxKeyCount = value
        if attribName == "randKeyCount":
            self.randKeyCount = value
        if attribName == "randKeyMinLen":
            self.randKeyMinLen = value
        if attribName == "randKeyMaxLen":
            self.randKeyMaxLen = value
        if attribName == "keyPool":
            self.keyPool = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randMinKeyCount = dictObj.get('randMinKeyCount', None)

        self.randMaxKeyCount = dictObj.get('randMaxKeyCount', None)

        self.randKeyCount = dictObj.get('randKeyCount', None)

        self.randKeyMinLen = dictObj.get('randKeyMinLen', 4)

        self.randKeyMaxLen = dictObj.get('randKeyMaxLen', 10)

        arrayKeyPool = dictObj.get('keyPool', [])
        for elemKeyPool in arrayKeyPool:
            self.keyPool.append(elemKeyPool)


def createRandomDictConfFromFlatDict(flatDict={}):
    ret = RandomDictConf()
    for key, value in flatDict.items():
        if key == "randMinKeyCount":
            ret.randMinKeyCount = value
        if key == "randMaxKeyCount":
            ret.randMaxKeyCount = value
        if key == "randKeyCount":
            ret.randKeyCount = value
        if key == "randKeyMinLen":
            ret.randKeyMinLen = value
        if key == "randKeyMaxLen":
            ret.randKeyMaxLen = value
        if key == "keyPool":
            ret.keyPool = value
    return ret

class RandomDataPropertyConf:
    """can put on schema properties to taylormade the random data generation
    """

    def __init__(self, dictObj=None):

        #: set this on a property to 'true' and no random data are generated for it
        self.randIgnore = None

        #: in case the property contains an array, this specifies the random data handling of the array
        self.randArrayConf = None

        #: values used to put randomly on the attrib, type is not close checked
        self.randValuePool = []

        #: 0 - always a value, 1 - 50 % empty, 2 - 75 % empty, 3 - 88% empty
        self.randProbabilityToBeEmpty = None

        #: taylormade configuration for the property type
        self.randValueConf = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.randIgnore is not None:
            ret["randIgnore"] = self.randIgnore
        if self.randArrayConf is not None:
            ret["randArrayConf"] = self.randArrayConf.toDict()
        if (self.randValuePool is not None) and (len(self.randValuePool) > 0):
            ret["randValuePool"] = self.randValuePool
        if self.randProbabilityToBeEmpty is not None:
            ret["randProbabilityToBeEmpty"] = self.randProbabilityToBeEmpty
        if self.randValueConf is not None:
            ret["randValueConf"] = self.randValueConf.toDict()
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "randIgnore":
            self.randIgnore = value
        self.randArrayConf.initFlatValue(attribName, value)
        if attribName == "randValuePool":
            self.randValuePool = value
        if attribName == "randProbabilityToBeEmpty":
            self.randProbabilityToBeEmpty = value
        self.randValueConf.initFlatValue(attribName, value)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randIgnore = dictObj.get('randIgnore', None)

        subDictObj = dictObj.get('randArrayConf', None)
        if subDictObj is not None:
            self.randArrayConf = RandomArrayConf(subDictObj)

        arrayRandValuePool = dictObj.get('randValuePool', [])
        for elemRandValuePool in arrayRandValuePool:
            self.randValuePool.append(elemRandValuePool)

        self.randProbabilityToBeEmpty = dictObj.get('randProbabilityToBeEmpty', None)

        subDictObj = dictObj.get('randValueConf', None)
        if subDictObj is not None:
            self.randValueConf = RandomPropertyTypeConf(subDictObj)


def createRandomDataPropertyConfFromFlatDict(flatDict={}):
    ret = RandomDataPropertyConf()
    for key, value in flatDict.items():
        if key == "randIgnore":
            ret.randIgnore = value
        ret.randArrayConf.initFlatValue(key, value)
        if key == "randValuePool":
            ret.randValuePool = value
        if key == "randProbabilityToBeEmpty":
            ret.randProbabilityToBeEmpty = value
        ret.randValueConf.initFlatValue(key, value)
    return ret

class RandomPropertyTypeConf:
    def __init__(self, dictObj=None):

        self.complexTypeConf = None

        #: in case the property contains an dictionary, this specifies the random data handling of the dictionary
        self.dictTypeConf = None

        self.stringTypeConf = None

        self.numTypeConf = None

        self.dateTypeConf = None

        self.timeTypeConf = None

        self.durationTypeConf = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.complexTypeConf is not None:
            ret["complexTypeConf"] = self.complexTypeConf.toDict()
        if self.dictTypeConf is not None:
            ret["dictTypeConf"] = self.dictTypeConf.toDict()
        if self.stringTypeConf is not None:
            ret["stringTypeConf"] = self.stringTypeConf.toDict()
        if self.numTypeConf is not None:
            ret["numTypeConf"] = self.numTypeConf.toDict()
        if self.dateTypeConf is not None:
            ret["dateTypeConf"] = self.dateTypeConf.toDict()
        if self.timeTypeConf is not None:
            ret["timeTypeConf"] = self.timeTypeConf.toDict()
        if self.durationTypeConf is not None:
            ret["durationTypeConf"] = self.durationTypeConf.toDict()
        return ret

    def initFlatValue(self, attribName, value):
        self.complexTypeConf.initFlatValue(attribName, value)
        self.dictTypeConf.initFlatValue(attribName, value)
        self.stringTypeConf.initFlatValue(attribName, value)
        self.numTypeConf.initFlatValue(attribName, value)
        self.dateTypeConf.initFlatValue(attribName, value)
        self.timeTypeConf.initFlatValue(attribName, value)
        self.durationTypeConf.initFlatValue(attribName, value)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        subDictObj = dictObj.get('complexTypeConf', None)
        if subDictObj is not None:
            self.complexTypeConf = RandomComplexTypeConf(subDictObj)

        subDictObj = dictObj.get('dictTypeConf', None)
        if subDictObj is not None:
            self.dictTypeConf = RandomDictConf(subDictObj)

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


def createRandomPropertyTypeConfFromFlatDict(flatDict={}):
    ret = RandomPropertyTypeConf()
    for key, value in flatDict.items():
        ret.complexTypeConf.initFlatValue(key, value)
        ret.dictTypeConf.initFlatValue(key, value)
        ret.stringTypeConf.initFlatValue(key, value)
        ret.numTypeConf.initFlatValue(key, value)
        ret.dateTypeConf.initFlatValue(key, value)
        ret.timeTypeConf.initFlatValue(key, value)
        ret.durationTypeConf.initFlatValue(key, value)
    return ret

class RandomStringTypeConf:
    """Constraints to generate random string values
    """

    def __init__(self, dictObj=None):

        self.strType = None

        self.maxLength = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.strType is not None:
            ret["strType"] = RandomStringTypeConfStrTypeEnum.valueAsString(self.strType)
        if self.maxLength is not None:
            ret["maxLength"] = self.maxLength
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "strType":
            self.strType = RandomStringTypeConfStrTypeEnum.valueForString(value)
        if attribName == "maxLength":
            self.maxLength = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.strType = RandomStringTypeConfStrTypeEnum.valueForString(dictObj.get('strType', None))

        self.maxLength = dictObj.get('maxLength', None)


def createRandomStringTypeConfFromFlatDict(flatDict={}):
    ret = RandomStringTypeConf()
    for key, value in flatDict.items():
        if key == "strType":
            ret.strType = RandomStringTypeConfStrTypeEnum.valueForString(value)
        if key == "maxLength":
            ret.maxLength = value
    return ret

class RandomNumTypeConf:
    """Constraints to generate random numeric values
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "minValue":
            self.minValue = value
        if attribName == "maxValue":
            self.maxValue = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


def createRandomNumTypeConfFromFlatDict(flatDict={}):
    ret = RandomNumTypeConf()
    for key, value in flatDict.items():
        if key == "minValue":
            ret.minValue = value
        if key == "maxValue":
            ret.maxValue = value
    return ret

class RandomDateTypeConf:
    """Constraints to generate random date values, used for dates and date-times
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "minValue":
            self.minValue = value
        if attribName == "maxValue":
            self.maxValue = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


def createRandomDateTypeConfFromFlatDict(flatDict={}):
    ret = RandomDateTypeConf()
    for key, value in flatDict.items():
        if key == "minValue":
            ret.minValue = value
        if key == "maxValue":
            ret.maxValue = value
    return ret

class RandomTimeTypeConf:
    """Constraints to generate random time values
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "minValue":
            self.minValue = value
        if attribName == "maxValue":
            self.maxValue = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


def createRandomTimeTypeConfFromFlatDict(flatDict={}):
    ret = RandomTimeTypeConf()
    for key, value in flatDict.items():
        if key == "minValue":
            ret.minValue = value
        if key == "maxValue":
            ret.maxValue = value
    return ret

class RandomDurationTypeConf:
    """Constraints to generate random duration values
    """

    def __init__(self, dictObj=None):

        self.minValue = None

        self.maxValue = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    def initFlatValue(self, attribName, value):
        if attribName == "minValue":
            self.minValue = value
        if attribName == "maxValue":
            self.maxValue = value

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.minValue = dictObj.get('minValue', None)

        self.maxValue = dictObj.get('maxValue', None)


def createRandomDurationTypeConfFromFlatDict(flatDict={}):
    ret = RandomDurationTypeConf()
    for key, value in flatDict.items():
        if key == "minValue":
            ret.minValue = value
        if key == "maxValue":
            ret.maxValue = value
    return ret

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




