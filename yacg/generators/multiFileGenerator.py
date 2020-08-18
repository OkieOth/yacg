"""A generator that creates from the model types one output file per type"""

import yacg.generators.helper.generatorHelperFuncs as generatorHelper

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
    multiFileTask -- container object with the parameters
    templateFile -- template file to use
    destDir -- output directory for the file to create
    destFilePrefix -- possible prefix to the type name based dest file name
    destFilePostfix -- possible postfix to the type name based dest file name
    destFileExt -- file extension
    templateParameterList -- list of yacg.model.config.TemplateParam instances, these parameters are passed to the template
    blackList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be excluded
    whiteList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be included
    fileFilter -- how the model should be filtered to create the files, default per model type
    """

    templateFile = multiFileTask.template
    destDir = multiFileTask.destDir
    destFilePrefix = multiFileTask.destFilePrefix
    destFilePostfix = multiFileTask.destFilePostfix
    destFileExt = multiFileTask.destFileExt
    templateParameterList = multiFileTask.templateParams
    fileFilter = multiFileTask.fileFilterType
    upperCaseFileNames = multiFileTask.upperCaseStartedDestFileName

    Path(destDir).mkdir(parents=True, exist_ok=True)
    if destDir is None:
        destDir = '.'
    if destFilePrefix is None:
        destFilePrefix = ''
    if destFilePostfix is None:
        destFilePostfix = ''
    if destFileExt is None:
        destFileExt = 'txt'

    template = Template(filename=templateFile)
    modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, whiteList)
    templateParameterDict = {}
    for templateParam in templateParameterList:
        templateParameterDict[templateParam.name] = templateParam.value
    if fileFilter == MultiFileTaskFileFilterTypeEnum.OPENAPIOPERATIONID:
        __renderOneFilePerOpenApiOperationId(
            modelTypesToUse, modelTypes, templateParameterDict,
            template, destDir, destFilePrefix, destFilePostfix, destFileExt, upperCaseFileNames)
    else:
        __renderOneFilePerType(
            modelTypesToUse, modelTypes, templateParameterDict,
            template, destDir, destFilePrefix, destFilePostfix, destFileExt, upperCaseFileNames)


def __renderOneFilePerOpenApiOperationId(
        modelTypesToUse,
        modelTypes,
        templateParameterDict,
        template,
        destDir,
        destFilePrefix,
        destFilePostfix,
        destFileExt,
        upperCaseFileNames):

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
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()


def __renderOneFilePerType(
        modelTypesToUse,
        modelTypes,
        templateParameterDict,
        template,
        destDir,
        destFilePrefix,
        destFilePostfix,
        destFileExt,
        upperCaseFileNames):
    for typeObj in modelTypesToUse:
        renderResult = template.render(
            currentType=typeObj,
            modelTypes=modelTypesToUse,
            availableTypes=modelTypes,
            templateParameters=templateParameterDict)
        outputFile = __getOutputFileName(destDir, destFilePrefix, destFilePostfix, destFileExt, typeObj, upperCaseFileNames)
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()


def __getOutputFileName(destDir, destFilePrefix, destFilePostfix, destFileExt, typeObj, upperCaseFileNames):
    fileNameBase = typeObj.name if hasattr(typeObj, 'name') and (typeObj.name is not None) else str(type(type))
    if isinstance(typeObj, str):
        fileNameBase = typeObj
    if upperCaseFileNames is True:
        fileNameBase = toUpperCamelCase(fileNameBase)
    return '{}/{}{}{}.{}'.format(destDir, destFilePrefix, fileNameBase, destFilePostfix, destFileExt)
