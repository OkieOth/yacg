## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.pythonFuncs as pythonFuncs

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
    ${stringUtils.toUpperCaseName(value)} = '${value}'
        % endfor

    % else:
class ${type.name}${ ' ({})'.format(type.extendsType.name) if type.extendsType is not None else ''}:
        % if type.description != None:
    """${templateHelper.addLineBreakToDescription(type.description,4)}
    """

        % endif
    def __init__(self):
        % if len(type.properties) == 0:
        pass
        % else:
            % for property in type.properties:

                % if type.description != None:
        #: ${type.description}
                % endif
        self.${property.name} = ${pythonFuncs.getDefaultPythonValue(property)}
            % endfor
        % endif

    @classmethod
    def dictToObject(cls, dict):
        obj = ${type.name}()
        obj.name = dict.get('name', None)
        % for property in type.properties:
            % if modelFuncs.isBaseType(type) and (not (property)):
        #: ${type.description}
            % endif

        obj.${property.name} = dict.get('${property.name}', None)
        % endfor
        return obj
    % endif


% endfor