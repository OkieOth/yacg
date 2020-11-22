"""A generator that creates from the model types one output file per type"""

import random
import uuid
from os import path
from pathlib import Path

import yacg.generators.helper.generatorHelperFuncs as generatorHelper
from yacg.generators.multiFileGenerator import getOutputFileName
import yacg.model.model as model


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
    randomDataDict = __prepareTypeObjects(modelTypesToUse, randomDataTask)
    __fillRandomValues(modelTypesToUse, randomDataTask, randomDataDict)
    __fillRandomValues(randomDataTask, randomDataDict)


def __prepareTypeObjects(modelTypesToUse, randomDataTask):
    """Simply create empty dictionaries for every type and fill it with unique key values
    it return a dict with type name as key and the array of the test data value
    """

    randomDataDict = {}
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
    return randomDataDict


def __initKeyAttribInTypeDict(typeDict, typeObj, randomDataTask, keyValueList):
    if __initKeyAttribInTypeDictFromKeyField(typeDict, typeObj, randomDataTask, keyValueList):
        return
    if __initKeyAttribInTypeDictFromSpecialKeyField(typeDict, typeObj, randomDataTask, keyValueList):
        return
    __initKeyAttribInTypeDictFromDefaultKeyNames(typeDict, typeObj, randomDataTask, keyValueList)


def __getRandomKeyValue(property, randomDataTask, keyValueList):
    if property.type is None:
        return None
    elif isinstance(type, model.IntegerType):
        lastKey = keyValueList[-1] if len(keyValueList)>0 else 0
        newKey = lastKey + 1
        keyValueList.append(newKey)
        return newKey
    elif isinstance(type, model.UuidType):
        uuidValue = uuid.uuid4()
        keyValueList.append(uuidValue)
        return uuid
    else:
        return None


def __initKeyAttribInTypeDictFromKeyField(typeDict, typeObj, randomDataTask, keyValueList):
    # has they type a taged key field ('__key')?
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
    if randomDataTask.specialElemCounts is not None:
        for elemCount in randomDataTask.specialElemCounts:
            if typeName == elemCount.typeName:
                minElemCount = elemCount.minElemCount
                maxElemCount = elemCount.maxElemCount
                break
    if minElemCount == maxElemCount:
        return minElemCount
    else:
        return random.randint(minElemCount, maxElemCount)


def __fillRandomValues(modelTypesToUse, randomDataTask, randomDataDict):
    """fills the type dictionaries with random values
    """

    # TODO
    pass


def __writeRandomValues(randomDataTask, randomDataDict):
    """writes the random data dictionary in one file per type
    """

    # TODO
    pass


def __renderOneFilePerType(
        modelTypesToUse,
        modelTypes,
        templateParameterDict,
        template,
        multiFileTask):

    destDir = multiFileTask.destDir
    destFilePrefix = multiFileTask.destFilePrefix
    destFilePostfix = multiFileTask.destFilePostfix
    destFileExt = multiFileTask.destFileExt
    upperCaseFileNames = multiFileTask.upperCaseStartedDestFileName

    for typeObj in modelTypesToUse:
        renderResult = template.render(
            currentType=typeObj,
            modelTypes=modelTypesToUse,
            availableTypes=modelTypes,
            templateParameters=templateParameterDict)
        outputFile = getOutputFileName(destDir, destFilePrefix, destFilePostfix, destFileExt, typeObj, upperCaseFileNames)
        __writeRenderResult(outputFile, multiFileTask, renderResult)


def __writeRenderResult(outputFile, multiFileTask, renderResult):
    if path.exists(outputFile) and multiFileTask.createOnlyIfNotExist:
        if multiFileTask.createTmpFileIfAlreadyExist:
            outputFile = outputFile + ".tmp"
            f = open(outputFile, "w+")
            f.write(renderResult)
            f.close()
    else:
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()


