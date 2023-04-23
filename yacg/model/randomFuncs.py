'''Functions needed by the createRandomData script'''
import random
import uuid
import datetime
import faker
import string

import yacg.model.random_config as randomConfig
import yacg.model.model as model


fakerInst = faker.Faker()


def extendMetaModelWithRandomConfigTypes(loadedTypes):
    '''travers a list of loaded types and replaces all 'processing' attributes
    with types from the random config model
    '''
    for t in loadedTypes:
        if t.processing is not None:
            randomTypeConf = randomConfig.RandomDataTypeConf()
            randomTypeConf.initFromDict(t.processing)
            t.processing = randomTypeConf
        if not hasattr(t, "properties"):
            continue
        for p in t.properties:
            if p.processing is not None:
                randomPropConf = randomConfig.RandomDataPropertyConf()
                randomPropConf.initFromDict(p.processing)
                p.processing = randomPropConf
    pass


def generateRandomData(type, defaultConfig, defaultElemCount=0):
    '''Generates random objects for that specific type in respect of the included
    'processing' attribute content and the passed 'defaultConfig'.

    Returns an array of JSON dictionaries that represents the random content.

    Keyword arguments:
    type -- type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    '''
    ret = []
    elemCount = defaultElemCount
    if elemCount == 0:
        if isinstance(type, list):
            pass
        if (defaultConfig is not None) and (defaultConfig.defaultElemCount is not None):
            elemCount = defaultConfig.defaultElemCount
        if type.processing is not None:
            if type.processing.randElemCount is not None:
                elemCount = type.processing.randElemCount
            else:
                min = 1
                max = 10
                if type.processing.randMaxElemCount is not None:
                    max = type.processing.randMaxElemCount
                if type.processing.randMinElemCount is not None:
                    min = type.processing.randMinElemCount
                elemCount = random.randint(min, max)
    for i in range(elemCount):
        r = None
        if isinstance(type, model.ComplexType):
            r = _generateRandomComplexType(type, defaultConfig, 0, None)
        elif isinstance(type, model.ArrayType):
            r = _generateRandomArrayType(type, defaultConfig)
        elif isinstance(type, model.DictionaryType):
            r = _generateRandomDictionaryType(type, defaultConfig, None)
        elif isinstance(type, model.IntegerType):
            r = __getRandomIntValue(None)
        elif isinstance(type, model.NumberType):
            r = __getRandomNumberValue(None)
        elif isinstance(type, model.BooleanType):
            r = __getRandomBooleanValue()
        elif isinstance(type, model.StringType):
            r = __getRandomStringValue(None)
        elif isinstance(type, model.UuidType):
            r = str(uuid.uuid4())
        elif isinstance(type, model.EnumType):
            r = __getRandomEnumValue(type, None)
        elif isinstance(type, model.DateType):
            r = __getRandomDateValue(defaultConfig, None)
        elif isinstance(type, model.TimeType):
            r = __getRandomTimeValue(None)
        elif isinstance(type, model.DateTimeType):
            r = __getRandomDateTimeValue(defaultConfig, None)
        if r is not None:
            ret.append(r)
    if len(ret) == 1:
        return ret[0]
    else:
        return ret


def _randIngnore(property, defaultConfig):
    '''Process the configuration how likely a value should be generated
    Returns False when a value for the property should be created
    '''
    if property.required:
        return False
    probabilityToBeEmpty = defaultConfig.defaultProbabilityToBeEmpty
    if (property.processing is not None) and (property.processing.randProbabilityToBeEmpty is not None):
        probabilityToBeEmpty = property.processing.randProbabilityToBeEmpty
    if probabilityToBeEmpty == 0:
        return False
    while probabilityToBeEmpty > 0:
        if bool(random.getrandbits(1)):
            return False
        probabilityToBeEmpty = probabilityToBeEmpty - 1
    return True


def __getMaxDepth(type, defaultConfig, randComplexTypeConf):
    maxDepth = 1
    if defaultConfig.defaultTypeDepth is not None:
        maxDepth = defaultConfig.defaultTypeDepth
    if (randComplexTypeConf is not None) and (randComplexTypeConf.defaultTypeDepth is not None):
        maxDepth = defaultConfig.defaultTypeDepth
    if (type.processing is not None) and (type.processing.randComplexTypeConf is not None) and (type.processing.randComplexTypeConf.defaultTypeDepth is not None):
        maxDepth = type.processing.randComplexTypeConf.defaultTypeDepth
    return maxDepth


def _generateRandomComplexType(type, defaultConfig, currentDepth, randComplexTypeConf):
    '''Generates random object for given complex type.

    Returns a JSON dictionary that represents the random object.

    Keyword arguments:
    type -- complex type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    currentDepth -- current depth for cascaded complex types
    randComplexTypeConf -- object of type RandomComplexTypeConf
    '''

    typeDict = {}
    if currentDepth > __getMaxDepth(type, defaultConfig, randComplexTypeConf):
        return None
    for property in type.properties:
        if (property.processing is not None) and (property.processing.randIgnore):
            continue
        if _randIngnore(property, defaultConfig):
            continue
        if (property.processing is not None) and (len(property.processing.randValuePool) > 0):
            randomValue = random.choice(property.type.values)
        elif property.isArray:
            dummyArray = model.ArrayType()
            dummyArray.itemsType = property.type
            dummyArray.arrayDimensions = property.arrayDimensions
            dummyArray.arrayConstraints = property.arrayConstraints
            dummyArray.processing = property.processing
            randomValue = _generateRandomArrayType(dummyArray, defaultConfig)
        else:
            randomValue = _getRandomValueForProperty(property, defaultConfig, currentDepth + 1)
        if randomValue is None:
            continue
        typeDict[property.name] = randomValue
    return typeDict


def _generateRandomArrayType(type, defaultConfig):
    '''Generates random object for given array type.

    Returns a JSON Array that represents the random object.

    Keyword arguments:
    type -- array type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    arrayConstraints -- constraints related to the type or the property
    '''

    arrayDimensions = type.arrayDimensions if type.arrayDimensions is not None else 1
    minElems = 1
    maxElems = 10
    if (defaultConfig is not None) and (defaultConfig.defaultMinArrayElemCount is not None):
        minElems = defaultConfig.defaultMinArrayElemCount
    if (defaultConfig is not None) and (defaultConfig.defaultMaxArrayElemCount is not None):
        maxElems = defaultConfig.defaultMaxArrayElemCount
    if (type.processing is not None) and (type.processing.randArrayConf is not None):
        if type.processing.randArrayConf.randMinElemCount is not None:
            minElems = type.processing.randArrayConf.randMinElemCount
        if type.processing.randArrayConf.randMaxElemCount is not None:
            maxElems = type.processing.randArrayConf.randMaxElemCount

    ret = []
    uniqueValues = False
    array = []
    for i in range(arrayDimensions):
        uValues = uniqueValues
        minE = minElems
        maxE = maxElems
        if (type.arrayConstraints is not None) and (len(type.arrayConstraints) > i) and (type.arrayConstraints[i] is not None):
            if type.arrayConstraints[i].arrayUniqueItems is not None:
                uValues = type.arrayConstraints[i].arrayUniqueItems
            if type.arrayConstraints[i].arrayMinItems is not None:
                minE = type.arrayConstraints[i].arrayMinItems
            if type.arrayConstraints[i].arrayMaxItems is not None:
                maxE = type.arrayConstraints[i].arrayMaxItems
        if (i + 1) < arrayDimensions:
            __fillRandomChildArrays(minE, maxE, array)
            if len(ret) == 0:
                ret = array
        else:
            if (type.arrayConstraints is not None) and (len(type.arrayConstraints) > 0):
                l = len(type.arrayConstraints) - 1
                if type.arrayConstraints[l].arrayMinItems is not None:
                    minElems = type.arrayConstraints[l].arrayMinItems
                if type.arrayConstraints[l].arrayMaxItems is not None:
                    maxElems = type.arrayConstraints[l].arrayMaxItems
            __fillRandomChildArraysWithValues(type.itemsType, defaultConfig, minE, maxE, uValues, array)
    if len(ret) == 0:
        return array
    else:
        return ret


def __fillRandomChildArraysWithValues(itemsType, defaultConfig, minE, maxE, uValues, array):
    if len(array) == 0:
        __generateRandomArrayTypeImpl(itemsType, defaultConfig, minE, maxE, uValues, array)
    else:
        for a in array:
            if len(a) == 0:
                __generateRandomArrayTypeImpl(itemsType, defaultConfig, minE, maxE, uValues, a)
            else:
                __fillRandomChildArraysWithValues(itemsType, defaultConfig, minE, maxE, uValues, a)


def __fillRandomChildArrays(minE, maxE, array):
    if len(array) == 0:
        __generateRandomArrayOfArrays(minE, maxE, array)
        return
    for a in array:
        if len(a) == 0:
            __generateRandomArrayOfArrays(minE, maxE, a)
        else:
            __fillRandomChildArrays(minE, maxE, a)


def __generateRandomArrayOfArrays(minE, maxE, array):
    numberOfElements = random.randint(minE, maxE)
    for i in range(numberOfElements):
        array.append([])


def __generateRandomArrayTypeImpl(itemsType, defaultConfig, minElems, maxElems, uniqueValues, array):
    '''Generates random object for given array type.

    Keyword arguments:
    itemsType -- type used for the random generation
    defaultConfig -- default configuration for this random task
    minElems -- minimal number of elements
    maxElems -- maximum number of elements
    uniqueValues -- bool if the content of the array should be uniqe
    array -- array to fill with random values
    '''

    numberOfElements = random.randint(minElems, maxElems)
    for i in range(numberOfElements):
        v = generateRandomData(itemsType, defaultConfig, 1)
        if uniqueValues:
            found = False
            for e in array:
                if e == v:
                    found = True
                    break
            if found:
                continue
        array.append(v)


def __getRandomKeyName(keyPool, minLen, maxLen):
    if (keyPool is not None) and (len(keyPool) > 0):
        return keyPool[random.randint(0, len(keyPool) - 1)]
    strLen = random.randint(minLen, maxLen)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(strLen))


def _generateRandomDictionaryType(type, defaultConfig, randDictTypeConf):
    '''Generates random object for given dictionary type.

    Returns a JSON dictionary that represents the random object.

    Keyword arguments:
    type -- array type that describes the data to generate, can also contain RandomDictConf
    randDictTypeConf -- object of yacg.model.random_config.RamdonDictConf, maybe from a property for inner types
    '''

    randMinKeyCount = 2
    randMaxKeyCount = 20
    randKeyCount = None
    randKeyMinLen = 4
    randKeyMaxLen = 15
    keyPool = None

    if (hasattr(type, "processing")) and (type.processing is not None) and (type.processing.randDictTypeConf is not None):
        if type.processing.randDictTypeConf.randMinKeyCount is not None:
            randMinKeyCount = type.processing.randDictTypeConf.randMinKeyCount
        if type.processing.randDictTypeConf.randMaxKeyCount is not None:
            randMaxKeyCount = type.processing.randDictTypeConf.randMaxKeyCount
        if type.processing.randDictTypeConf.randKeyCount is not None:
            randKeyCount = type.processing.randDictTypeConf.randKeyCount
        if type.processing.randDictTypeConf.randKeyMinLen is not None:
            randKeyMinLen = type.processing.randDictTypeConf.randKeyMinLen
        if type.processing.randDictTypeConf.randKeyMaxLen is not None:
            randKeyMaxLen = type.processing.randDictTypeConf.randKeyMaxLen
        if type.processing.randDictTypeConf.keyPool is not None:
            keyPool = type.processing.randDictTypeConf.keyPool
    if (randDictTypeConf is not None):
        if randDictTypeConf.randMinKeyCount is not None:
            randMinKeyCount = randDictTypeConf.randMinKeyCount
        if randDictTypeConf.randMaxKeyCount is not None:
            randMaxKeyCount = randDictTypeConf.randMaxKeyCount
        if randDictTypeConf.randKeyCount is not None:
            randKeyCount = randDictTypeConf.randKeyCount
        if randDictTypeConf.randKeyMinLen is not None:
            randKeyMinLen = randDictTypeConf.randKeyMinLen
        if randDictTypeConf.randKeyMaxLen is not None:
            randKeyMaxLen = randDictTypeConf.randKeyMaxLen
        if randDictTypeConf.keyPool is not None:
            keyPool = randDictTypeConf.keyPool

    typeDict = {}
    if randKeyCount is None:
        randKeyCount = random.randint(randMinKeyCount, randMaxKeyCount)
    for i in range(randKeyCount):
        key = __getRandomKeyName(keyPool, randKeyMinLen, randKeyMaxLen)
        value = generateRandomData(type.valueType, defaultConfig, 1)
        typeDict[key] = value
    return typeDict


def _getRandomValueForProperty(property, defaultConfig, currentDepth):
    '''Generates random data for a given property description.

    Returns a JSON object that represents the random object. The
    type of the object depends on the property type

    Keyword arguments:
    property -- yacg property object
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    currentDepth -- current depth of cascaded complex types
    '''

    if property.type is None:
        return None
    elif isinstance(property.type, model.IntegerType):
        return __getRandomIntValue(property.processing)
    elif isinstance(property.type, model.NumberType):
        return __getRandomNumberValue(property.processing)
    elif isinstance(property.type, model.BooleanType):
        return __getRandomBooleanValue()
    elif isinstance(property.type, model.StringType):
        return __getRandomStringValue(property.processing)
    elif isinstance(property.type, model.UuidType):
        return str(uuid.uuid4())
    elif isinstance(property.type, model.EnumType):
        return __getRandomEnumValue(property.type, property.processing)
    elif isinstance(property.type, model.DateType):
        return __getRandomDateValue(defaultConfig, property.processing)
    elif isinstance(property.type, model.TimeType):
        return __getRandomTimeValue(property.processing)
    elif isinstance(property.type, model.DateTimeType):
        return __getRandomDateTimeValue(defaultConfig, property.processing)
    elif isinstance(property.type, model.DictionaryType):
        randDictTypeConf = property.processing.randValueConf if property.processing is not None else None
        return _generateRandomDictionaryType(property.type, defaultConfig, randDictTypeConf)
    elif isinstance(property.type, model.ComplexType):
        randComplexTypeConf = property.processing.randValueConf if property.processing is not None else None
        return _generateRandomComplexType(property.type, defaultConfig, currentDepth + 1, randComplexTypeConf)
    else:
        return None


def getValueFromPoolIfConfigured(processing):
    if (processing is not None):
        poolLength = len(processing.randValuePool)
        if poolLength == 0:
            return False, None
        index = random.randint(0, len(poolLength) - 1)
        return True, processing.randValuePool[index]
    return False, None


def __getRandomIntValue(processing):
    handled, value = getValueFromPoolIfConfigured(processing)
    if handled:
        return value
    minValue = -10000
    maxValue = 10000
    if (processing is not None) and (processing.randValueConf is not None):
        if processing.randValueConf.numTypeConf is not None:
            if processing.randValueConf.numTypeConf.minValue is not None:
                minValue = processing.randValueConf.numTypeConf.minValue
            if processing.randValueConf.numTypeConf.maxValue is not None:
                maxValue = processing.randValueConf.numTypeConf.maxValue
    return random.randint(minValue, maxValue)


def __getRandomNumberValue(processing):
    handled, value = getValueFromPoolIfConfigured(processing)
    if handled:
        return value
    minValue = -10000
    maxValue = 10000
    if (processing is not None) and (processing.randValueConf is not None):
        if processing.randValueConf.numTypeConf is not None:
            if processing.randValueConf.numTypeConf.minValue is not None:
                minValue = processing.randValueConf.numTypeConf.minValue
            if processing.randValueConf.numTypeConf.maxValue is not None:
                maxValue = processing.randValueConf.numTypeConf.maxValue
    newInt = random.randint(minValue, maxValue)
    return random.random() + newInt


def __getRandomBooleanValue():
    return bool(random.getrandbits(1))


def __getRandomStringValue(processing):
    handled, value = getValueFromPoolIfConfigured(processing)
    if handled:
        return value
    # property.processing.randValueConf.stringTypeConf.strType
    # ... 'NAME', 'ADDRESS', 'EMAIL', 'URL', 'PHONE', 'COUNTRY', 'TEXT', 'SENTENCE'

    strType = randomConfig.RandomStringTypeConfStrTypeEnum.SENTENCE
    maxLen = 512  # TODO make configurable
    if (processing is not None) and (processing.randValueConf is not None):
        if processing.randValueConf.stringTypeConf is not None:
            if processing.randValueConf.stringTypeConf.strType is not None:
                strType = processing.randValueConf.stringTypeConf.strType
            if processing.randValueConf.stringTypeConf.maxLength is not None:
                maxLen = processing.randValueConf.stringTypeConf.maxLength
    if strType == randomConfig.RandomStringTypeConfStrTypeEnum.TEXT:
        ret = fakerInst.text()
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.NAME:
        ret = fakerInst.text()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.ADDRESS:
        ret = fakerInst.address()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.EMAIL:
        ret = fakerInst.email()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.URL:
        ret = fakerInst.url()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.PHONE:
        ret = fakerInst.phone()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.COUNTRY:
        ret = fakerInst.country()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.NAME:
        ret = fakerInst.name()
    else:
        ret = fakerInst.sentence()
    if len(ret) > maxLen:
        return ret[:maxLen]
    else:
        return ret


def __getRandomEnumValue(type, processing):
    handled, value = getValueFromPoolIfConfigured(processing)
    if handled:
        return value
    return random.choice(type.values)


def __getRandomDateValueImpl(processing, defaultConfig, formatStr):
    handled, value = getValueFromPoolIfConfigured(processing)
    if handled:
        return value
    # seems to be a better approach:
    # https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    minDateStr = defaultConfig.defaultMinDate if defaultConfig.defaultMinDate is not None else "2020-01-01"
    maxDateStr = defaultConfig.defaultMaxDate if defaultConfig.defaultMaxDate is not None else "2025-01-01"
    if (processing is not None) and (processing.randValueConf is not None):
        if processing.randValueConf.dateTypeConf is not None:
            if processing.randValueConf.dateTypeConf.minValue is not None:
                minDateStr = processing.randValueConf.dateTypeConf.minValue
            if processing.randValueConf.dateTypeConf.maxValue is not None:
                maxDateStr = processing.randValueConf.dateTypeConf.maxValue

    fstr = "%Y-%m-%d"
    startDate = datetime.datetime.strptime(minDateStr, fstr)
    endDate = datetime.datetime.strptime(maxDateStr, fstr)
    delta = endDate - startDate
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    randomDate = startDate + datetime.timedelta(seconds=random_second)
    return randomDate.strftime(formatStr)


def __getRandomDateValue(defaultConfig, processing):
    formatStr = "%Y-%m-%d"
    return __getRandomDateValueImpl(processing, defaultConfig, formatStr)


def __getRandomTimeValue(processing):
    handled, value = getValueFromPoolIfConfigured(processing)
    if handled:
        return value
    minTime = "00:00:00"
    maxTime = "23:59:00"
    if (processing is not None) and (processing.randValueConf is not None):
        if processing.randValueConf.dateTypeConf is not None:
            if processing.randValueConf.timeTypeConf.minValue is not None:
                minTime = processing.randValueConf.timeTypeConf.minValue
            if processing.randValueConf.timeTypeConf.maxValue is not None:
                maxTime = processing.randValueConf.timeTypeConf.maxValue

    minParts = minTime.split(":")
    minHour = int(minParts[0])
    minMin = int(minParts[1])
    minSec = int(minParts[2]) if len(minParts) > 2 else None
    maxParts = maxTime.split(":")
    maxHour = int(maxParts[0])
    maxMin = int(maxParts[1])
    maxSec = int(maxParts[2]) if len(maxParts) > 2 else None
    hour = random.randint(minHour, maxHour)
    min = random.randint(minMin, maxMin)
    sec = random.randint(minSec, maxSec) if (minSec is not None) and (maxSec is not None) else None
    retHour = str(hour)
    if len(retHour) == 1:
        retHour = "0" + retHour
    retMin = str(min)
    if len(retMin) == 1:
        retMin = "0" + retMin
    if sec is not None:
        retSec = str(sec)
        if len(retSec) == 1:
            retSec = "0" + retSec
        return "{}:{}:{}".format(retHour, retMin, retSec)
    else:
        return "{}:{}".format(retHour, retMin)


def __getRandomDateTimeValue(defaultConfig, processing):
    formatStr = "%Y-%m-%dT%H:%M:%S"
    return __getRandomDateValueImpl(processing, defaultConfig, formatStr)
