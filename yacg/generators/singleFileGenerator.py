"""A generator that creates from the model types and the given template
one single output file"""

import yacg.generators.helper.generatorHelperFuncs as generatorHelper

from mako.template import Template


def renderSingleFileTemplate(modelTypes, templateFile, output, templateParameterList, blackList, whiteList):
    """render a template that produce one output file. This file contains content based
    on every type of the model.
    A possible example is the creation of a plantUml diagram from a model

    Keyword arguments:
    modelTypes -- list of types that build the model, list of yacg.model.model.Type instances (mostly Enum- and ComplexTypes)
    templateFile -- template file to use
    output -- output file to create
    templateParameterList -- list of yacg.model.config.TemplateParam instances, these parameters are passed to the template
    blackList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be excluded
    whiteList -- list of yacg.model.config.BlackWhiteListEntry instances to describe types that should be included
    """

    template = Template(filename=templateFile)
    modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, whiteList)
    templateParameterDict = {}
    for templateParam in templateParameterList:
        templateParameterDict[templateParam.name] = templateParam.value
    renderResult = template.render(
        modelTypes=modelTypesToUse,
        templateParameters=templateParameterDict)
    if (output == 'stdout'):
        print(renderResult)
    else:
        outputFile = output
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()
