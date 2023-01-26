'''Functions needed by the createRandomData script'''
import random

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
        return __getRandomIntValue(property, randomDataTask)
    elif isinstance(property.type, model.NumberType):
        return __getRandomNumberValue(property, randomDataTask)
    elif isinstance(property.type, model.BooleanType):
        return __getRandomBooleanValue(property, randomDataTask)
    elif isinstance(property.type, model.StringType):
        return __getRandomStringValue(property, randomDataTask)
    elif isinstance(property.type, model.UuidType):
        return uuid.uuid4()
    elif isinstance(property.type, model.EnumType):
        return __getRandomEnumValue(property, randomDataTask)
    elif isinstance(property.type, model.DateType):
        return __getRandomDateValue(property, randomDataTask)
    elif isinstance(property.type, model.TimeType):
        return __getRandomTimeValue(property, randomDataTask)
    elif isinstance(property.type, model.DateTimeType):
        return __getRandomDateTimeValue(property, randomDataTask)
    elif isinstance(property.type, model.ComplexType):
        return __getRandomComplexValue(typeObj, property, randomDataTask, randomDataDict, keyValueDict, currentDepth)
    else:
        return None


    # TODO
    return None