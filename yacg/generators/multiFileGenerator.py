"""A generator that creates from the model types one output file per type"""
import yacg.generators.helper.generatorHelperFuncs as generatorHelper

from os import path
from mako.template import Template

from pathlib import Path
from yacg.model.config import MultiFileTaskFileFilterTypeEnum
from yacg.generators.helper.filter.swaggerPathFilter import swaggerFilterByOperationId
from yacg.util.stringUtils import toUpperCamelCase


def renderMultiFileTemplate(
        modelTypes,
        blackList,
        whiteList,
        multiFileTask):
    """render a template that produce one output file. This file contains content based
    on every type of the model.
    A possible example is the creation of a plantUml diagram from a model

    Keyword arguments:
    modelTypes -- list of types that build the model, list of yacg.model.model.Type instances (mostly Enum- and ComplexTypes)
    blackList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be excluded
    whiteList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be included
    multiFileTask -- container object with the parameters
    """

    template = Template(filename=multiFileTask.template)
    modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, whiteList)
    templateParameterDict = {}
    for templateParam in multiFileTask.templateParams:
        templateParameterDict[templateParam.name] = templateParam.value

    if multiFileTask.destDir is None:
        multiFileTask.destDir = '.'
    if multiFileTask.destFilePrefix is None:
        multiFileTask.destFilePrefix = ''
    if multiFileTask.destFilePostfix is None:
        multiFileTask.destFilePostfix = ''
    if multiFileTask.destFileExt is None:
        multiFileTask.destFileExt = 'txt'

    Path(multiFileTask.destDir).mkdir(parents=True, exist_ok=True)

    if multiFileTask.fileFilterType == MultiFileTaskFileFilterTypeEnum.OPENAPIOPERATIONID:
        __renderOneFilePerOpenApiOperationId(
            modelTypesToUse, modelTypes, templateParameterDict,
            template, multiFileTask)
    else:
        __renderOneFilePerType(
            modelTypesToUse, modelTypes, templateParameterDict,
            template, multiFileTask)


def renderRandomDataTemplate(
        modelTypes,
        blackList,
        whiteList,
        multiFileTask):
    """render a template that produce one output file. This file contains content based
    on every type of the model.
    A possible example is the creation of a plantUml diagram from a model

    Keyword arguments:
    modelTypes -- list of types that build the model, list of yacg.model.model.Type instances (mostly Enum- and ComplexTypes)
    blackList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be excluded
    whiteList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be included
    multiFileTask -- container object with the parameters
    """

    template = Template(filename=multiFileTask.template)
    modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, whiteList)
    templateParameterDict = {}
    for templateParam in multiFileTask.templateParams:
        templateParameterDict[templateParam.name] = templateParam.value

    if multiFileTask.destDir is None:
        multiFileTask.destDir = '.'
    if multiFileTask.destFilePrefix is None:
        multiFileTask.destFilePrefix = ''
    if multiFileTask.destFilePostfix is None:
        multiFileTask.destFilePostfix = ''
    if multiFileTask.destFileExt is None:
        multiFileTask.destFileExt = 'txt'

    Path(multiFileTask.destDir).mkdir(parents=True, exist_ok=True)

    if multiFileTask.fileFilterType == MultiFileTaskFileFilterTypeEnum.OPENAPIOPERATIONID:
        __renderOneFilePerOpenApiOperationId(
            modelTypesToUse, modelTypes, templateParameterDict,
            template, multiFileTask)
    else:
        __renderOneFilePerType(
            modelTypesToUse, modelTypes, templateParameterDict,
            template, multiFileTask)


def __renderOneFilePerOpenApiOperationId(
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

    operationIdEntries = swaggerFilterByOperationId(modelTypesToUse)
    for key in operationIdEntries:
        typeObj = operationIdEntries.get(key)
        templateParameterDict['currentOperationId'] = key
        renderResult = template.render(
            currentType=typeObj,
            modelTypes=modelTypesToUse,
            availableTypes=modelTypes,
            templateParameters=templateParameterDict)
        outputFile = __getOutputFileName(destDir, destFilePrefix, destFilePostfix, destFileExt, key, upperCaseFileNames)
        __writeRenderResult(outputFile, multiFileTask, renderResult)


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
        outputFile = __getOutputFileName(destDir, destFilePrefix, destFilePostfix, destFileExt, typeObj, upperCaseFileNames)
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


def __getOutputFileName(destDir, destFilePrefix, destFilePostfix, destFileExt, typeObj, upperCaseFileNames):
    fileNameBase = typeObj.name if hasattr(typeObj, 'name') and (typeObj.name is not None) else str(type(type))
    if isinstance(typeObj, str):
        fileNameBase = typeObj
    if upperCaseFileNames is True:
        fileNameBase = toUpperCamelCase(fileNameBase)
    fileNameBase = ''.join([i if (ord(i) < 123) and (ord(i) > 47) else '_' for i in fileNameBase])
    return '{}/{}{}{}.{}'.format(destDir, destFilePrefix, fileNameBase, destFilePostfix, destFileExt)
