"""A generator that creates from the model types and the given template
one single output file"""

import yacg.generators.helper.generatorHelperFuncs as generatorHelper

from mako.template import Template


def renderSingleFileTemplate(modelTypes, blackList, whiteList, singleFileTask):
    """render a template that produce one output file. This file contains content based
    on every type of the model.
    A possible example is the creation of a plantUml diagram from a model

    Keyword arguments:
    modelTypes -- list of types that build the model, list of yacg.model.model.Type instances (mostly Enum- and ComplexTypes)
    templateFile -- template file to use
    blackList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be excluded
    whiteList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be included
    singleFileTask - configuration for the single file task
    """

    template = Template(filename=singleFileTask.template)
    modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, whiteList)
    templateParameterDict = {}
    for templateParam in singleFileTask.templateParams:
        templateParameterDict[templateParam.name] = templateParam.value
    renderResult = template.render(
        modelTypes=modelTypesToUse,
        availableTypes=modelTypes,
        templateParameters=templateParameterDict)
    if (singleFileTask.destFile == 'stdout'):
        print(renderResult)
    else:
        outputFile = singleFileTask.destFile
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()
