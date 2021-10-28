## Template to create a Python file with type beans of the model types
<%
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.pythonFuncs as pythonFuncs

    templateFile = 'pythonBeans.mako'
    templateVersion = '1.0.0'

    baseModelDomain = templateParameters.get('baseModelDomain',None)
    domainList = modelFuncs.getDomainsAsList(modelTypes)

%># Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: ${templateFile} v${templateVersion})

% if modelFuncs.hasEnumTypes(modelTypes):
from enum import Enum
% endif
% for domain in domainList:
    % if baseModelDomain != domain:
import ${domain}
    % endif
% endfor


% for type in modelTypes:
    % if modelFuncs.isEnumType(type):
class ${type.name}(Enum):
        % for value in type.values:
    ${stringUtils.toUpperCaseName(value)} = '${value}'
        % endfor

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        % for value in type.values:
        elif lowerStringValue == '${value.lower()}':
            return ${type.name}.${stringUtils.toUpperCaseName(value)}
        % endfor
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        % for value in type.values:
        elif enumValue == ${type.name}.${stringUtils.toUpperCaseName(value)}:
            return '${value}'
        % endfor
        else:
            return ''


    % else:
class ${type.name}${ ' ({})'.format(pythonFuncs.getExtendsType(type, modelTypes, baseModelDomain)) if type.extendsType is not None else ''}:
        % if type.description != None:
    """${templateHelper.addLineBreakToDescription(type.description,4)}
    """

        % endif
    def __init__(self, config):
        if config is None:
            return None
        % if type.extendsType is not None:
        super(${pythonFuncs.getExtendsType(type, modelTypes, baseModelDomain)}, self).__init__()
        % endif
        % if len(type.properties) == 0:
        pass
        % else:
            % for property in type.properties:

                % if type.description != None:
        #: ${type.description}
                % endif
            % if modelFuncs.isBaseType(property.type):
                % if not property.isArray:
        self.${property.name} = config.get('${property.name}', ${property.type.default if hasattr(property.type,'default') else ${pythonFuncs.getDefaultPythonValue(property)}})
                % else:
        self.${property.name} = config.get('${property.name}', [])
                % endif
            % elif modelFuncs.isEnumType(property.type):
                % if not property.isArray:

        self.${property.name} = ${property.type.name}.valueForString(config.get('${property.name}', None))
                % else:

        self.${property.name} = [
            ${property.type.name}.valueForString(item)
            for item in config.get('${property.name}', [])
        ]
                % endif
            % else:
                % if not property.isArray:

        self.${property.name} = ${pythonFuncs.getTypeWithPackage(property.type, modelTypes, baseModelDomain)}(config.get('${property.name}', ${property.type.default if hasattr(property.type,'default') else None}))
                % else:

        self.${property.name} = [
            ${pythonFuncs.getTypeWithPackage(property.type, modelTypes, baseModelDomain)}(item)
            for item in config.get('${property.name}', [])
        ]
                % endif
            % endif
            % endfor
        % endif

    % endif

% endfor
