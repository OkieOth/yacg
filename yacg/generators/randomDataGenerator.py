"""A generator that creates from the model types one output file per type"""

from os import path
from pathlib import Path

import yacg.generators.helper.generatorHelperFuncs as generatorHelper
from yacg.generators.multiFileGenerator import getOutputFileName


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
        dataList = []
        setCount = __getSetCountForType(typeObj.name, randomDataTask)
        randomDataDict[typeObj.name] = dataList
    return randomDataDict


def __getSetCountForType(typeName, randomDataTask):
    """returns the number of set that should be created for that type
    """

    # TODO
    pass


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


