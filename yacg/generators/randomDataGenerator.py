"""A generator that creates from the model types one output file per type"""

import json
import random
import string
import uuid
import datetime
from pathlib import Path
from uuid import UUID

import yacg.generators.helper.generatorHelperFuncs as generatorHelper
import yacg.model.model as model
import yacg.model.config as config


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def renderRandomData(
        modelTypes,
        blackList,
        whiteList,
        randomDataTask):
    """render a template that produce one output file. This file contains content based
    on every type of the model.
    A possible example is the creation of a plantUml diagram from a model

    Keyword arguments:
    modelTypes -- list of types that build the model, list of yacg.model.model.Type instances (mostly Enum- and ComplexTypes)
    blackList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be excluded
    whiteList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be included
    randomDataTask -- container object with the parameters
    """

    modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, whiteList)

    Path(randomDataTask.destDir).mkdir(parents=True, exist_ok=True)

    # TODO create dict with random data
    randomDataDict, keyValueDict = __prepareTypeObjects(modelTypesToUse, randomDataTask)
    __fillRandomValues(modelTypesToUse, randomDataTask, randomDataDict, keyValueDict)
    __writeRandomValues(randomDataTask, randomDataDict)
    return randomDataDict


def __prepareTypeObjects(modelTypesToUse, randomDataTask):
    """Simply create empty dictionaries for every type and fill it with unique key values
    it return a dict with type name as key and the array of the test data value
    """

    randomDataDict = {}
    keyValueDict = {}
    for typeObj in modelTypesToUse:
        if not isinstance(typeObj, model.ComplexType):
            continue
        dataList = []
        setCount = __getSetCountForType(typeObj.name, randomDataTask)
        keyValueList = []
        for i in range(setCount):
            typeDict = {}
            __initKeyAttribInTypeDict(typeDict, typeObj, randomDataTask, keyValueList)
            dataList.append(typeDict)
        randomDataDict[typeObj.name] = dataList
        keyValueDict[typeObj.name] = keyValueList
    return (randomDataDict, keyValueDict)


def __initKeyAttribInTypeDict(typeDict, typeObj, randomDataTask, keyValueList):
    if __initKeyAttribInTypeDictFromKeyField(typeDict, typeObj, randomDataTask, keyValueList):
        return
    if __initKeyAttribInTypeDictFromSpecialKeyField(typeDict, typeObj, randomDataTask, keyValueList):
        return
    __initKeyAttribInTypeDictFromDefaultKeyNames(typeDict, typeObj, randomDataTask, keyValueList)


def __getRandomKeyValue(property, randomDataTask, keyValueList):
    if property.type is None:
        return None
    elif isinstance(property.type, model.IntegerType):
        lastKey = keyValueList[-1] if len(keyValueList) > 0 else 0
        newKey = lastKey + 1
        keyValueList.append(newKey)
        return newKey
    elif isinstance(property.type, model.UuidType):
        uuidValue = uuid.uuid4()
        keyValueList.append(uuidValue)
        return uuidValue
    else:
        return None


def __getRandomIntValue(property, randomDataTask):
    newInt = random.randint(-10000, 10000)
    return newInt


def __getRandomNumberValue(property, randomDataTask):
    newInt = random.randint(-10000, 10000)
    return random.random() + newInt


def __getRandomBooleanValue(property, randomDataTask):
    return bool(random.getrandbits(1))


def __getRandomStringValue(property, randomDataTask):
    strLen = random.randint(0, 20)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(strLen))


def __getRandomEnumValue(property, randomDataTask):
    return random.choice(property.type.values)


def __getRandomDateValue(property, randomDataTask):
    # seems to be a better approach: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    # startdate=datetime.date(YYYY,MM,DD)
    # date=startdate+datetime.timedelta(randint(1,365))
    minYear = 2005
    maxYear = 2025
    return datetime.date(random.randint(minYear, maxYear), random.randint(1, 12), random.randint(1, 28))


def __getRandomDateTimeValue(property, randomDataTask):
    minYear = 2005
    maxYear = 2025
    return datetime.datetime(
        random.randint(minYear, maxYear),
        random.randint(1, 12),
        random.randint(1, 28),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59))


def __getRandomComplexValue(typeObj, property, randomDataTask, randomDataDict, keyValueDict, currentDepth):
    # create a new dict for the type
    # initialize the keys
    # init the addtional properties
    # put it to randomDataDict

    # TODO
    maxDepth = randomDataTask.defaultMaxDepth
    propertyName = '{typeName}.{propName}'.format(typeName=typeObj.name, propName=property.name)
    for md in randomDataTask.specialMaxDepths:
        if md.propertyName == propertyName:
            maxDepth = md.maxDepth if md.maxDepth is not None else maxDepth
            break
    if currentDepth > maxDepth:
        return None

    keyValueList = keyValueDict.get(property.type.name, [])

    typeDict = {}
    __initKeyAttribInTypeDict(typeDict, property.type, randomDataTask, keyValueList)
    __fillRandomValuesForType(property.type, typeDict, randomDataTask, randomDataDict, keyValueDict, currentDepth)
    return typeDict


def __getRandomValue(typeObj, property, randomDataTask, randomDataDict, keyValueDict, currentDepth):
    """get random value for a specific type property

    Keyword arguments
    typeObj -- current type
    property -- item of yacg.model.ComplexType.properties
    randomDataTask -- configuration how to generate random data
    randomDataDict -- dictionary that takes per type a list with generated random data
    keyValueDict -- dictionary that takes per type a list with already used keys
    """

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
    elif isinstance(property.type, model.DateTimeType):
        return __getRandomDateTimeValue(property, randomDataTask)
    elif isinstance(property.type, model.ComplexType):
        return __getRandomComplexValue(typeObj, property, randomDataTask, randomDataDict, keyValueDict, currentDepth)
    else:
        return None


def __initKeyAttribInTypeDictFromKeyField(typeDict, typeObj, randomDataTask, keyValueList):
    # has they type a taged key field ('x-key')?
    for property in typeObj.properties:
        if property.isKey:
            randomValue = __getRandomKeyValue(property, randomDataTask, keyValueList)
            if randomValue is None:
                return True
            typeDict[property.name] = randomValue
            return True
    return False


def __initKeyAttribInTypeDictFromDefaultKeyNames(typeDict, typeObj, randomDataTask, keyValueList):
    # if the property name in the default keyNames
    for property in typeObj.properties:
        if property.name in randomDataTask.defaultKeyPropNames:
            randomValue = __getRandomKeyValue(property, randomDataTask, keyValueList)
            if randomValue is None:
                return True
            typeDict[property.name] = randomValue
            return


def __initKeyAttribInTypeDictFromSpecialKeyField(typeDict, typeObj, randomDataTask, keyValueList):
    # is for that type a specific field given as key?
    keyPropName = None
    if randomDataTask.specialKeyPropNames is not None:
        for keyPropNameEntry in randomDataTask.specialKeyPropNames:
            if typeObj.name == keyPropNameEntry.typeName:
                keyPropName = keyPropNameEntry.keyPropName
                break

    if keyPropName is None:
        return False

    # if the property equals the special config or is in the default keyNames
    for property in typeObj.properties:
        if property.name == keyPropName:
            randomValue = __getRandomKeyValue(property, randomDataTask, keyValueList)
            if randomValue is None:
                return True
            typeDict[property.name] = randomValue
            return True
    return False


def __getSetCountForType(typeName, randomDataTask):
    """returns the number of set that should be created for that type
    """

    minElemCount = randomDataTask.defaultMinElemCount
    maxElemCount = randomDataTask.defaultMaxElemCount
    if len(randomDataTask.specialElemCounts) > 0:
        for elemCount in randomDataTask.specialElemCounts:
            if typeName == elemCount.typeName:
                minElemCount = elemCount.minElemCount
                maxElemCount = elemCount.maxElemCount
                break
    if minElemCount == maxElemCount:
        return minElemCount
    else:
        return random.randint(minElemCount, maxElemCount)


def __getArraySize(typeOb, property, randomDataTask):
    # TODO
    return random.randint(1, 10)


def __fillRandomValues(modelTypesToUse, randomDataTask, randomDataDict, keyValueDict):
    """fills the type dictionaries with random values

    Keyword arguments
    modelTypesToUse -- list of model types
    randomDataTask -- configuration how to generate random data
    randomDataDict -- dictionary that takes per type a list with generated random data
    keyValueDict -- dictionary that takes per type a list with already used keys
    """

    for typeObj in modelTypesToUse:
        if not isinstance(typeObj, model.ComplexType):
            continue
        dataList = randomDataDict.get(typeObj.name, [])
        for dataListEntryDict in dataList:
            __fillRandomValuesForType(typeObj, dataListEntryDict, randomDataTask, randomDataDict, keyValueDict, 1)


def __fillRandomValuesForType(typeObj, typeDict, randomDataTask, randomDataDict, keyValueDict, currentDepth):
    currentDepth = currentDepth + 1
    for property in typeObj.properties:
        if typeDict.get(property.name, None) is not None:
            continue
        if property.isArray:
            arraySize = __getArraySize(typeObj, property, randomDataTask)
            randomValue = []
            for i in range(arraySize):
                tmpRandomValue = __getRandomValue(typeObj, property, randomDataTask, randomDataDict, keyValueDict, currentDepth)
                if tmpRandomValue is None:
                    continue
                randomValue.append(tmpRandomValue)
        else:
            randomValue = __getRandomValue(typeObj, property, randomDataTask, randomDataDict, keyValueDict, currentDepth)
        if randomValue is None:
            continue
        typeDict[property.name] = randomValue


def __writeRandomValues(randomDataTask, randomDataDict):
    """writes the random data dictionary in one file per type
    """

    destDir = randomDataTask.destDir
    isCsv = randomDataTask.outputType is config.RandomDataTaskOutputTypeEnum.CSV
    for typeName in randomDataDict.keys():
        fileExt = 'csv' if isCsv else 'json'
        fileNameBase = ''.join([i if (ord(i) < 123) and (ord(i) > 47) else '_' for i in typeName])
        fileName = '{}/{}.{}'.format(destDir, fileNameBase, fileExt)
        randomData = randomDataDict[typeName]
        with open(fileName, 'w') as outfile:
            if isCsv:
                # implementation for object trees really sucks
                pass
            else:
                json.dump(randomData, outfile, cls=JsonEncoder, indent=4)
