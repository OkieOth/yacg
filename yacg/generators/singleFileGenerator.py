"""A generator that creates from the model types and the given template
one single output file"""

from mako.template import Template


def renderSingleFileTemplate(modelTypes, templateFile, output, templateParameterList):
    template = Template(filename=templateFile)
    templateParameterDict = {}
    for templateParam in templateParameterList:
        templateParameterDict[templateParam.name] = templateParam.value
    renderResult = template.render(
        modelTypes=modelTypes,
        templateParameters=templateParameterDict)
    if (output == 'stdout'):
        print(renderResult)
    else:
        outputFile = output
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()

    # TODO
