## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs

    templateFile = 'pythonBeans.mako'
    templateVersion = '1.0.0'

    def hasEnumTypes(modelTypes):
        for type in modelTypes:
            if isinstance(type,model.EnumType):
                return True
        return False

%># Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: ${templateFile} v${templateVersion})

% if hasEnumTypes(modelTypes):
from enum import Enum

% endif

% for type in modelTypes:
    % if isinstance(type, model.EnumType):    
class ${type.name}(Enum):
        % for value in type.values:
    ${value.upper()} = '${value}'
        % endfor

    % else:
class ${type.name}${ ' ({})'.format(type.extendsType.name) if type.extendsType is not None else ''}:
        % if type.description != None:
    """${templateHelper.addLineBreakToDescription(type.description,4)}
    """

        % endif
    def __init__(self):
        % if type.description != None:
        super.__init__()
        % endif
        pass

    % endif

% endfor