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

    def printExtendsType(type):
        if baseModelDomain is None:
            return type.extendsType.name            
        elif type.extendsType.domain != baseModelDomain: 
            return type.extendsType.name
        else:
            ret = baseModelPackageShort + '.' + type.extendsType.name
            return '{}.{}'.format(baseModelPackageShort, type.extendsType.name)

    baseModelDomain = templateParameters.get('baseModelDomain',None)
    baseModelPackage = templateParameters.get('baseModelPackage',None)
    baseModelPackageShort = templateParameters.get('baseModelPackageShort','<<"baseModelPackageShort" template param is missing>>')


%># Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: ${templateFile} v${templateVersion})

% if hasEnumTypes(modelTypes):
from enum import Enum

% endif
% if baseModelPackage is not None:
import ${baseModelPackage} as ${baseModelPackageShort}

% endif

% for type in modelTypes:
    % if isinstance(type, model.EnumType):    
class ${type.name}(Enum):
        % for value in type.values:
    ${stringUtils.toUpperCaseName(value)} = '${value}'
        % endfor

    @classmethod
    def valueForString(cls, stringValue):
        if stringValue is None:
            return None
        % for value in type.values:
        elif stringValue == '${value}':
            return ${type.name}.${stringUtils.toUpperCaseName(value)}
        % endfor
        else:
            return None

    % else:
class ${type.name}${ ' ({})'.format(printExtendsType(type)) if type.extendsType is not None else ''}:
        % if type.description != None:
    """${templateHelper.addLineBreakToDescription(type.description,4)}
    """

        % endif
    def __init__(self):
        % if type.extendsType is not None:
        super(${type.extendsType.name}, self).__init__()
        % endif
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
        if dict is None:
            return None
        obj = ${type.name}()
        % for property in type.properties:
            % if modelFuncs.isBaseType(property.type):
                % if not property.isArray:

        obj.${property.name} = dict.get('${property.name}', None)
                % else:

        array${stringUtils.toUpperCamelCase(property.name)} = dict.get('${property.name}', [])
        for elem${stringUtils.toUpperCamelCase(property.name)} in array${stringUtils.toUpperCamelCase(property.name)}:
            obj.${property.name}.append(elem${stringUtils.toUpperCamelCase(property.name)})
                % endif
            % elif modelFuncs.isEnumType(property.type):
                % if not property.isArray:

        obj.${property.name} = ${property.type.name}.valueForString(dict.get('${property.name}', None))
                % else:

        array${stringUtils.toUpperCamelCase(property.name)} = dict.get('${property.name}', [])
        for elem${stringUtils.toUpperCamelCase(property.name)} in array${stringUtils.toUpperCamelCase(property.name)}:
            obj.${property.name}.append(
                ${property.type.name}.valueForString(elem${stringUtils.toUpperCamelCase(property.name)}))
                % endif
            % else:
                % if not property.isArray:

        obj.${property.name} = ${property.type.name}.dictToObject(dict.get('${property.name}', None))
                % else:

        array${stringUtils.toUpperCamelCase(property.name)} = dict.get('${property.name}', [])
        for elem${stringUtils.toUpperCamelCase(property.name)} in array${stringUtils.toUpperCamelCase(property.name)}:
            obj.${property.name}.append(
                ${property.type.name}.dictToObject(elem${stringUtils.toUpperCamelCase(property.name)}))
                % endif
            % endif
        % endfor
        return obj

    % endif

% endfor