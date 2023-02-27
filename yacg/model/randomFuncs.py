'''Functions needed by the createRandomData script'''
import random
import uuid
import datetime

import yacg.model.random_config as randomConfig
import yacg.model.model as model


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
            r = _generateRandomComplexType(type, defaultConfig)
        elif isinstance(type, model.ArrayType):
            r = _generateRandomArrayType(type, defaultConfig)
        elif isinstance(type, model.DictionaryType):
            r = _generateRandomDictionaryType(type, defaultConfig)
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


def _generateRandomComplexType(type, defaultConfig):
    '''Generates random object for given complex type.

    Returns a JSON dictionary that represents the random object.

    Keyword arguments:
    type -- complex type that describes the data to generate
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
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
            dummyArray.processing = property.procession
            randomValue = _generateRandomArrayType(dummyArray, defaultConfig)
        else:
            randomValue = _getRandomValueForProperty(property, defaultConfig)
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

    typeArray = []
    # TODO
    return typeArray


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


def _getRandomValueForProperty(property, defaultConfig):
    '''Generates random data for a given property description.

    Returns a JSON object that represents the random object. The
    type of the object depends on the property type

    Keyword arguments:
    property -- yacg property object
    defaultConfig -- object of yacg.model.random_config.RamdonDefaultConfig
    '''

    if property.type is None:
        return None
    elif isinstance(property.type, model.IntegerType):
        return __getRandomIntValue(property, defaultConfig)
    elif isinstance(property.type, model.NumberType):
        return __getRandomNumberValue(property, defaultConfig)
    elif isinstance(property.type, model.BooleanType):
        return __getRandomBooleanValue(property, defaultConfig)
    elif isinstance(property.type, model.StringType):
        return __getRandomStringValue(property, defaultConfig)
    elif isinstance(property.type, model.UuidType):
        return uuid.uuid4()
    elif isinstance(property.type, model.EnumType):
        return __getRandomEnumValue(property, defaultConfig)
    elif isinstance(property.type, model.DateType):
        return __getRandomDateValue(property, defaultConfig)
    elif isinstance(property.type, model.TimeType):
        return __getRandomTimeValue(property, defaultConfig)
    elif isinstance(property.type, model.DateTimeType):
        return __getRandomDateTimeValue(property, defaultConfig)
    elif isinstance(property.type, model.ComplexType):
        return _generateRandomComplexType(property.type, defaultConfig)
    else:
        return None


def getValueFromPoolIfConfigured(property):
    if (property.processing is not None):
        poolLength = len(property.processing.randValuePool)
        if poolLength == 0:
            return False, None
        index = random.randint(0, len(poolLength) - 1)
        return True, property.processing.randValuePool[index]
    return False, None


def __getRandomIntValue(property, defaultConfig):
    handled, value = getValueFromPoolIfConfigured(property)
    if handled:
        return value
    minValue = -10000
    maxValue = 10000
    if property.processing.randValueConf is not None:
        if property.processing.randValueConf.numTypeConf is not None:
            if property.processing.randValueConf.numTypeConf.minValue is not None:
                minValue = property.processing.randValueConf.numTypeConf.minValue
            if property.processing.randValueConf.numTypeConf.maxValue is not None:
                maxValue = property.processing.randValueConf.numTypeConf.maxValue
    return random.randint(minValue, maxValue)


def __getRandomNumberValue(property, defaultConfig):
    handled, value = getValueFromPoolIfConfigured(property)
    if handled:
        return value
    minValue = -10000
    maxValue = 10000
    if property.processing.randValueConf is not None:
        if property.processing.randValueConf.numTypeConf is not None:
            if property.processing.randValueConf.numTypeConf.minValue is not None:
                minValue = property.processing.randValueConf.numTypeConf.minValue
            if property.processing.randValueConf.numTypeConf.maxValue is not None:
                maxValue = property.processing.randValueConf.numTypeConf.maxValue
    newInt = random.randint(minValue, maxValue)
    return random.random() + newInt


def __getRandomBooleanValue(property, defaultConfig):
    return bool(random.getrandbits(1))


def __getRandomStringValue(property, defaultConfig):
    handled, value = getValueFromPoolIfConfigured(property)
    if handled:
        return value
    # property.processing.randValueConf = None
    # property.processing.randValueConf.complexTypeConf = None
    # property.processing.randValueConf.stringTypeConf = None
    # property.processing.randValueConf.numTypeConf = None
    # property.processing.randValueConf.dateTypeConf = None
    # property.processing.randValueConf.timeTypeConf = None
    # property.processing.randValueConf.durationTypeConf = None
    pass # TODO


def __getRandomEnumValue(property, defaultConfig):
    handled, value = getValueFromPoolIfConfigured(property)
    if handled:
        return value
    return random.choice(property.type.values)


def __getRandomDateValueImpl(property, defaultConfig, formatStr):
    handled, value = getValueFromPoolIfConfigured(property)
    if handled:
        return value
    # seems to be a better approach:
    # https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    minDateStr = defaultConfig.defaultMinDate if defaultConfig.defaultMinDate is not None else "2020-01-01"
    maxDateStr = defaultConfig.defaultMaxDate if defaultConfig.defaultMaxDate is not None else "2025-01-01"
    if property.processing.randValueConf is not None:
        if property.processing.randValueConf.dateTypeConf is not None:
            if property.processing.randValueConf.dateTypeConf.minValue is not None:
                minDateStr = property.processing.randValueConf.dateTypeConf.minValue
            if property.processing.randValueConf.dateTypeConf.maxValue is not None:
                maxDateStr = property.processing.randValueConf.dateTypeConf.maxValue

    formatStr = "%d-%m-%Y"
    startDate = datetime.strptime(minDateStr, formatStr)
    endDate = datetime.strptime(maxDateStr, formatStr)
    delta = endDate - startDate
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    randomDate = startDate + datetime.timedelta(seconds=random_second)
    return randomDate.strftime(formatStr)


def __getRandomDateValue(property, defaultConfig):
    formatStr = "%d-%m-%Y"
    __getRandomDateValueImpl(property, defaultConfig, formatStr)


def __getRandomTimeValue(property, defaultConfig):
    handled, value = getValueFromPoolIfConfigured(property)
    if handled:
        return value
    # property.processing.randValueConf = None
    # property.processing.randValueConf.complexTypeConf = None
    # property.processing.randValueConf.stringTypeConf = None
    # property.processing.randValueConf.numTypeConf = None
    # property.processing.randValueConf.dateTypeConf = None
    # property.processing.randValueConf.timeTypeConf = None
    # property.processing.randValueConf.durationTypeConf = None
    pass # TODO


def __getRandomDateTimeValue(property, defaultConfig):
    formatStr = "%d-%m-%YT%H:%M:%S"
    __getRandomDateValueImpl(property, defaultConfig, formatStr)
