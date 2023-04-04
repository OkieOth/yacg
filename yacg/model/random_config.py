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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "defaultElemCount":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultElemCount = value
        if attribName == "defaultTypeDepth":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultTypeDepth = value
        if attribName == "defaultMinArrayElemCount":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultMinArrayElemCount = value
        if attribName == "defaultMaxArrayElemCount":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultMaxArrayElemCount = value
        if attribName == "defaultMinDate":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultMinDate = value
        if attribName == "defaultMaxDate":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultMaxDate = value
        if attribName == "defaultProbabilityToBeEmpty":
            if ret is None:
                ret = RamdonDefaultConfig()
            ret.defaultProbabilityToBeEmpty = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "defaultElemCount":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultElemCount = value
            if key == "defaultTypeDepth":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultTypeDepth = value
            if key == "defaultMinArrayElemCount":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultMinArrayElemCount = value
            if key == "defaultMaxArrayElemCount":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultMaxArrayElemCount = value
            if key == "defaultMinDate":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultMinDate = value
            if key == "defaultMaxDate":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultMaxDate = value
            if key == "defaultProbabilityToBeEmpty":
                if ret is None:
                    ret = RamdonDefaultConfig()
                ret.defaultProbabilityToBeEmpty = value
        return ret

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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "randMinElemCount":
            if ret is None:
                ret = RandomDataTypeConf()
            ret.randMinElemCount = value
        if attribName == "randMaxElemCount":
            if ret is None:
                ret = RandomDataTypeConf()
            ret.randMaxElemCount = value
        if attribName == "randElemCount":
            if ret is None:
                ret = RandomDataTypeConf()
            ret.randElemCount = value
        initObj = ret.randComplexTypeConf if ret is not None else None
        randComplexTypeConfTmp = RandomComplexTypeConf.initWithFlatValue(attribName, value, initObj)
        if randComplexTypeConfTmp is not None:
            if ret is None:
                ret = RandomDataTypeConf()
            ret.randComplexTypeConf = randComplexTypeConfTmp
        initObj = ret.randArrayConf if ret is not None else None
        randArrayConfTmp = RandomArrayConf.initWithFlatValue(attribName, value, initObj)
        if randArrayConfTmp is not None:
            if ret is None:
                ret = RandomDataTypeConf()
            ret.randArrayConf = randArrayConfTmp
        initObj = ret.randDictTypeConf if ret is not None else None
        randDictTypeConfTmp = RandomDictConf.initWithFlatValue(attribName, value, initObj)
        if randDictTypeConfTmp is not None:
            if ret is None:
                ret = RandomDataTypeConf()
            ret.randDictTypeConf = randDictTypeConfTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "randMinElemCount":
                if ret is None:
                    ret = RandomDataTypeConf()
                ret.randMinElemCount = value
            if key == "randMaxElemCount":
                if ret is None:
                    ret = RandomDataTypeConf()
                ret.randMaxElemCount = value
            if key == "randElemCount":
                if ret is None:
                    ret = RandomDataTypeConf()
                ret.randElemCount = value
            initObj = ret.randComplexTypeConf if ret is not None else None
            randComplexTypeConfTmp = RandomComplexTypeConf.initWithFlatValue(attribName, value, initObj)
            if randComplexTypeConfTmp is not None:
                if ret is None:
                    ret = RandomDataTypeConf()
                ret.randComplexTypeConf = randComplexTypeConfTmp
            initObj = ret.randArrayConf if ret is not None else None
            randArrayConfTmp = RandomArrayConf.initWithFlatValue(attribName, value, initObj)
            if randArrayConfTmp is not None:
                if ret is None:
                    ret = RandomDataTypeConf()
                ret.randArrayConf = randArrayConfTmp
            initObj = ret.randDictTypeConf if ret is not None else None
            randDictTypeConfTmp = RandomDictConf.initWithFlatValue(attribName, value, initObj)
            if randDictTypeConfTmp is not None:
                if ret is None:
                    ret = RandomDataTypeConf()
                ret.randDictTypeConf = randDictTypeConfTmp
        return ret

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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "typeDepth":
            if ret is None:
                ret = RandomComplexTypeConf()
            ret.typeDepth = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "typeDepth":
                if ret is None:
                    ret = RandomComplexTypeConf()
                ret.typeDepth = value
        return ret

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.typeDepth = dictObj.get('typeDepth', None)


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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "randMinElemCount":
            if ret is None:
                ret = RandomArrayConf()
            ret.randMinElemCount = value
        if attribName == "randMaxElemCount":
            if ret is None:
                ret = RandomArrayConf()
            ret.randMaxElemCount = value
        if attribName == "randElemCount":
            if ret is None:
                ret = RandomArrayConf()
            ret.randElemCount = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "randMinElemCount":
                if ret is None:
                    ret = RandomArrayConf()
                ret.randMinElemCount = value
            if key == "randMaxElemCount":
                if ret is None:
                    ret = RandomArrayConf()
                ret.randMaxElemCount = value
            if key == "randElemCount":
                if ret is None:
                    ret = RandomArrayConf()
                ret.randElemCount = value
        return ret

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.randMinElemCount = dictObj.get('randMinElemCount', None)

        self.randMaxElemCount = dictObj.get('randMaxElemCount', None)

        self.randElemCount = dictObj.get('randElemCount', None)


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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "randMinKeyCount":
            if ret is None:
                ret = RandomDictConf()
            ret.randMinKeyCount = value
        if attribName == "randMaxKeyCount":
            if ret is None:
                ret = RandomDictConf()
            ret.randMaxKeyCount = value
        if attribName == "randKeyCount":
            if ret is None:
                ret = RandomDictConf()
            ret.randKeyCount = value
        if attribName == "randKeyMinLen":
            if ret is None:
                ret = RandomDictConf()
            ret.randKeyMinLen = value
        if attribName == "randKeyMaxLen":
            if ret is None:
                ret = RandomDictConf()
            ret.randKeyMaxLen = value
        if attribName == "keyPool":
            if ret is None:
                ret = RandomDictConf()
            ret.keyPool = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "randMinKeyCount":
                if ret is None:
                    ret = RandomDictConf()
                ret.randMinKeyCount = value
            if key == "randMaxKeyCount":
                if ret is None:
                    ret = RandomDictConf()
                ret.randMaxKeyCount = value
            if key == "randKeyCount":
                if ret is None:
                    ret = RandomDictConf()
                ret.randKeyCount = value
            if key == "randKeyMinLen":
                if ret is None:
                    ret = RandomDictConf()
                ret.randKeyMinLen = value
            if key == "randKeyMaxLen":
                if ret is None:
                    ret = RandomDictConf()
                ret.randKeyMaxLen = value
            if key == "keyPool":
                if ret is None:
                    ret = RandomDictConf()
                ret.keyPool = value
        return ret

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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "randIgnore":
            if ret is None:
                ret = RandomDataPropertyConf()
            ret.randIgnore = value
        initObj = ret.randArrayConf if ret is not None else None
        randArrayConfTmp = RandomArrayConf.initWithFlatValue(attribName, value, initObj)
        if randArrayConfTmp is not None:
            if ret is None:
                ret = RandomDataPropertyConf()
            ret.randArrayConf = randArrayConfTmp
        if attribName == "randValuePool":
            if ret is None:
                ret = RandomDataPropertyConf()
            ret.randValuePool = value
        if attribName == "randProbabilityToBeEmpty":
            if ret is None:
                ret = RandomDataPropertyConf()
            ret.randProbabilityToBeEmpty = value
        initObj = ret.randValueConf if ret is not None else None
        randValueConfTmp = RandomPropertyTypeConf.initWithFlatValue(attribName, value, initObj)
        if randValueConfTmp is not None:
            if ret is None:
                ret = RandomDataPropertyConf()
            ret.randValueConf = randValueConfTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "randIgnore":
                if ret is None:
                    ret = RandomDataPropertyConf()
                ret.randIgnore = value
            initObj = ret.randArrayConf if ret is not None else None
            randArrayConfTmp = RandomArrayConf.initWithFlatValue(attribName, value, initObj)
            if randArrayConfTmp is not None:
                if ret is None:
                    ret = RandomDataPropertyConf()
                ret.randArrayConf = randArrayConfTmp
            if key == "randValuePool":
                if ret is None:
                    ret = RandomDataPropertyConf()
                ret.randValuePool = value
            if key == "randProbabilityToBeEmpty":
                if ret is None:
                    ret = RandomDataPropertyConf()
                ret.randProbabilityToBeEmpty = value
            initObj = ret.randValueConf if ret is not None else None
            randValueConfTmp = RandomPropertyTypeConf.initWithFlatValue(attribName, value, initObj)
            if randValueConfTmp is not None:
                if ret is None:
                    ret = RandomDataPropertyConf()
                ret.randValueConf = randValueConfTmp
        return ret

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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        initObj = ret.complexTypeConf if ret is not None else None
        complexTypeConfTmp = RandomComplexTypeConf.initWithFlatValue(attribName, value, initObj)
        if complexTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.complexTypeConf = complexTypeConfTmp
        initObj = ret.dictTypeConf if ret is not None else None
        dictTypeConfTmp = RandomDictConf.initWithFlatValue(attribName, value, initObj)
        if dictTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.dictTypeConf = dictTypeConfTmp
        initObj = ret.stringTypeConf if ret is not None else None
        stringTypeConfTmp = RandomStringTypeConf.initWithFlatValue(attribName, value, initObj)
        if stringTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.stringTypeConf = stringTypeConfTmp
        initObj = ret.numTypeConf if ret is not None else None
        numTypeConfTmp = RandomNumTypeConf.initWithFlatValue(attribName, value, initObj)
        if numTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.numTypeConf = numTypeConfTmp
        initObj = ret.dateTypeConf if ret is not None else None
        dateTypeConfTmp = RandomDateTypeConf.initWithFlatValue(attribName, value, initObj)
        if dateTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.dateTypeConf = dateTypeConfTmp
        initObj = ret.timeTypeConf if ret is not None else None
        timeTypeConfTmp = RandomTimeTypeConf.initWithFlatValue(attribName, value, initObj)
        if timeTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.timeTypeConf = timeTypeConfTmp
        initObj = ret.durationTypeConf if ret is not None else None
        durationTypeConfTmp = RandomDurationTypeConf.initWithFlatValue(attribName, value, initObj)
        if durationTypeConfTmp is not None:
            if ret is None:
                ret = RandomPropertyTypeConf()
            ret.durationTypeConf = durationTypeConfTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            initObj = ret.complexTypeConf if ret is not None else None
            complexTypeConfTmp = RandomComplexTypeConf.initWithFlatValue(attribName, value, initObj)
            if complexTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.complexTypeConf = complexTypeConfTmp
            initObj = ret.dictTypeConf if ret is not None else None
            dictTypeConfTmp = RandomDictConf.initWithFlatValue(attribName, value, initObj)
            if dictTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.dictTypeConf = dictTypeConfTmp
            initObj = ret.stringTypeConf if ret is not None else None
            stringTypeConfTmp = RandomStringTypeConf.initWithFlatValue(attribName, value, initObj)
            if stringTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.stringTypeConf = stringTypeConfTmp
            initObj = ret.numTypeConf if ret is not None else None
            numTypeConfTmp = RandomNumTypeConf.initWithFlatValue(attribName, value, initObj)
            if numTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.numTypeConf = numTypeConfTmp
            initObj = ret.dateTypeConf if ret is not None else None
            dateTypeConfTmp = RandomDateTypeConf.initWithFlatValue(attribName, value, initObj)
            if dateTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.dateTypeConf = dateTypeConfTmp
            initObj = ret.timeTypeConf if ret is not None else None
            timeTypeConfTmp = RandomTimeTypeConf.initWithFlatValue(attribName, value, initObj)
            if timeTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.timeTypeConf = timeTypeConfTmp
            initObj = ret.durationTypeConf if ret is not None else None
            durationTypeConfTmp = RandomDurationTypeConf.initWithFlatValue(attribName, value, initObj)
            if durationTypeConfTmp is not None:
                if ret is None:
                    ret = RandomPropertyTypeConf()
                ret.durationTypeConf = durationTypeConfTmp
        return ret

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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "strType":
            if ret is None:
                ret = RandomStringTypeConf()
            ret.strType = RandomStringTypeConfStrTypeEnum.valueForString(value)
        if attribName == "maxLength":
            if ret is None:
                ret = RandomStringTypeConf()
            ret.maxLength = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "strType":
                if ret is None:
                    ret = RandomStringTypeConf()
                ret.strType = RandomStringTypeConfStrTypeEnum.valueForString(value)
            if key == "maxLength":
                if ret is None:
                    ret = RandomStringTypeConf()
                ret.maxLength = value
        return ret

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

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "minValue":
            if ret is None:
                ret = RandomNumTypeConf()
            ret.minValue = value
        if attribName == "maxValue":
            if ret is None:
                ret = RandomNumTypeConf()
            ret.maxValue = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "minValue":
                if ret is None:
                    ret = RandomNumTypeConf()
                ret.minValue = value
            if key == "maxValue":
                if ret is None:
                    ret = RandomNumTypeConf()
                ret.maxValue = value
        return ret

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

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "minValue":
            if ret is None:
                ret = RandomDateTypeConf()
            ret.minValue = value
        if attribName == "maxValue":
            if ret is None:
                ret = RandomDateTypeConf()
            ret.maxValue = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "minValue":
                if ret is None:
                    ret = RandomDateTypeConf()
                ret.minValue = value
            if key == "maxValue":
                if ret is None:
                    ret = RandomDateTypeConf()
                ret.maxValue = value
        return ret

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

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "minValue":
            if ret is None:
                ret = RandomTimeTypeConf()
            ret.minValue = value
        if attribName == "maxValue":
            if ret is None:
                ret = RandomTimeTypeConf()
            ret.maxValue = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "minValue":
                if ret is None:
                    ret = RandomTimeTypeConf()
                ret.minValue = value
            if key == "maxValue":
                if ret is None:
                    ret = RandomTimeTypeConf()
                ret.maxValue = value
        return ret

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

    def toDict(self):
        ret = {}
        if self.minValue is not None:
            ret["minValue"] = self.minValue
        if self.maxValue is not None:
            ret["maxValue"] = self.maxValue
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "minValue":
            if ret is None:
                ret = RandomDurationTypeConf()
            ret.minValue = value
        if attribName == "maxValue":
            if ret is None:
                ret = RandomDurationTypeConf()
            ret.maxValue = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "minValue":
                if ret is None:
                    ret = RandomDurationTypeConf()
                ret.minValue = value
            if key == "maxValue":
                if ret is None:
                    ret = RandomDurationTypeConf()
                ret.maxValue = value
        return ret

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



