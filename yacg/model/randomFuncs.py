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


def generateRandomData(type, defaultConfig):
    '''Generates random objects for that specific type in respect of the included
    'processing' attribute content and the passed 'defaultConfig'.

    Returns an array of JSON dictionaries that represents the random content.

    Keyword arguments:
    type -- type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    '''
    ret = []
    for i in range(type.processing.randElemCount):
        r = None
        if isinstance(type, model.ComplexType):
            r = _generateRandomComplexType(type, defaultConfig, 0)
        elif isinstance(type, model.ArrayType):
            r = _generateRandomArrayType(type, defaultConfig)
        elif isinstance(type, model.DictionaryType):
            r = _generateRandomDictionaryType(type, defaultConfig)
        elif isinstance(type, model.IntegerType):
            r = __getRandomIntValue(None)
        elif isinstance(type, model.NumberType):
            r = __getRandomNumberValue(None)
        elif isinstance(type, model.BooleanType):
            r = __getRandomBooleanValue()
        elif isinstance(type, model.StringType):
            r = __getRandomStringValue(None)
        elif isinstance(type, model.UuidType):
            r = uuid.uuid4()
        elif isinstance(type, model.EnumType):
            r = __getRandomEnumValue(property.type, None)
        elif isinstance(type, model.DateType):
            r = __getRandomDateValue(defaultConfig, None)
        elif isinstance(type, model.TimeType):
            r = __getRandomTimeValue(None)
        elif isinstance(type, model.DateTimeType):
            r = __getRandomDateTimeValue(defaultConfig, None)
        if r is not None:
            ret.append(r)
    return ret


def _randIngnore(property, defaultConfig):
    '''Process the configuration how likely a value should be generated
    Returns True when a value for the property should be created
    '''
    if property.required:
        return False
    probabilityToBeEmpty = defaultConfig.defaultProbabilityToBeEmpty
    if (property.processing is not None) and (property.processing.randProbabilityToBeEmpty is not None):
        probabilityToBeEmpty = property.processing.randProbabilityToBeEmpty
    while probabilityToBeEmpty > 0:
        if bool(random.getrandbits(1)):
            return True
    return False


def _generateRandomComplexType(type, defaultConfig, currentDepth):
    '''Generates random object for given complex type.

    Returns a JSON dictionary that represents the random object.

    Keyword arguments:
    type -- complex type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    currentDepth -- current depth for cascaded complex types
    '''

    typeDict = {}
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
    '''

    arrayDimensions = type.arrayDimensions if type.arrayDimensions is not None else 1
    minElems = 0
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
            __fillRandomChildArraysWithValues(type.itemsType, defaultConfig, minE, maxE, uValues, array)
    if len(ret) == 0:
        return array
    else:
        return ret


def __fillRandomChildArraysWithValues(itemsType, defaultConfig, minE, maxE, uValues, array):
    for a in array:
        if len(a) == 0:
            __generateRandomArrayTypeImpl(type.itemsType, defaultConfig, minE, maxE, uValues, a)
        else:
            __fillRandomChildArraysWithValues(itemsType, defaultConfig, minE, maxE, uValues, a)


def __fillRandomChildArrays(minE, maxE, array):
    for a in array:
        if len(a) == 0:
            __generateRandomArrayOfArrays(minE, maxE, a)
        else:
            __fillRandomChildArrays(minE, maxE, a)


def __generateRandomArrayOfArrays(minE, maxE, array):
    numberOfElements = random.randint(minElems, maxElems)
    for i in range(numberOfElements):
        array.append([])

def __generateRandomArrayTypeImpl(itemsType, defaultConfig, minElems, maxElems, uniqueValues, array):
    '''Generates random object for given array type.

    Returns a JSON Array that represents the random object.

    Keyword arguments:
    itemsType -- type used for the random generation
    defaultConfig -- default configuration for this random task
    minElems -- minimal number of elements
    maxElems -- maximum number of elements
    uniqueValues -- bool if the content of the array should be uniqe
    '''

    numberOfElements = random.randint(minElems, maxElems)
    ret = []
    for i in range(numberOfElements):
        v = generateRandomData(itemsType, defaultConfig)
        if uniqueValues:
            found = False
            for e in ret:
                if e == v:
                    found = True
                    break
            if found:
                continue
        ret.append(generateRandomData(itemsType, defaultConfig))
    return ret


def __getRandomKeyName(minLen, maxLen):
    strLen = random.randint(minLen, maxLen)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(strLen))


def _generateRandomDictionaryType(type, defaultConfig):
    '''Generates random object for given dictionary type.

    Returns a JSON dictionary that represents the random object.

    Keyword arguments:
    type -- array type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    '''

    typeDict = {}
    # TODO
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
        return uuid.uuid4()
    elif isinstance(property.type, model.EnumType):
        return __getRandomEnumValue(property.type, property.processing)
    elif isinstance(property.type, model.DateType):
        return __getRandomDateValue(defaultConfig, property.processing)
    elif isinstance(property.type, model.TimeType):
        return __getRandomTimeValue(property.processing)
    elif isinstance(property.type, model.DateTimeType):
        return __getRandomDateTimeValue(defaultConfig, property.processing)
    elif isinstance(property.type, model.ComplexType):
        return _generateRandomComplexType(type, defaultConfig, currentDepth + 1)
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
        ret = faker.text()
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.NAME:
        ret = faker.text()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.ADDRESS:
        ret = faker.address()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.EMAIL:
        ret = faker.email()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.URL:
        ret = faker.url()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.PHONE:
        ret = faker.phone()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.COUNTRY:
        ret = faker.country()
        pass
    elif strType == randomConfig.RandomStringTypeConfStrTypeEnum.NAME:
        ret = faker.name()
    else:
        ret = faker.sentence()
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

    formatStr = "%d-%m-%Y"
    startDate = datetime.strptime(minDateStr, formatStr)
    endDate = datetime.strptime(maxDateStr, formatStr)
    delta = endDate - startDate
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    randomDate = startDate + datetime.timedelta(seconds=random_second)
    return randomDate.strftime(formatStr)


def __getRandomDateValue(defaultConfig, processing):
    formatStr = "%d-%m-%Y"
    __getRandomDateValueImpl(processing, defaultConfig, formatStr)


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
    formatStr = "%d-%m-%YT%H:%M:%S"
    __getRandomDateValueImpl(processing, defaultConfig, formatStr)
