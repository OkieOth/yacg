from mako.template import Template

def renderTemplate():
    template = Template(filename='/home/eiko/prog/github/yacg/yacg/generators/templates/test.mako')
    print(template.render())
