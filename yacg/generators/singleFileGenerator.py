"""A generator that creates from the model types and the given template
one single output file"""

import yacg.generators.helper.generatorHelperFuncs as generatorHelper

from mako.template import Template


def renderSingleFileTemplate(modelTypes, templateFile, output, templateParameterList, blackList, whiteList):
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

    # TODO
