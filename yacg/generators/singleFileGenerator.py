"""A generator that creates from the model types and the given template
one single output file"""

from mako.template import Template

def renderSingleFileTemplate(modelTypes,templateFile,args):
    template = Template(filename=templateFile)
    renderResult = template.render(modelTypes = modelTypes)
    print (renderResult) # TODO
