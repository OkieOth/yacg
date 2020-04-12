"""A generator that creates from the model types and the given template
one single output file"""

from mako.template import Template


def renderSingleFileTemplate(modelTypes, templateFile, output, args):
    template = Template(filename=templateFile)
    renderResult = template.render(modelTypes=modelTypes)
    if (output == 'stdout'):
        print(renderResult)
    else:
        outputFile = output
        f = open(outputFile, "w+")
        f.write(renderResult)
        f.close()

    # TODO
