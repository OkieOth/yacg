## Template to create a Python file with type beans of the model types
<%
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.pythonFuncs as pythonFuncs

    templateFile = 'pythonBeans.mako'
    templateVersion = '1.1.0'

    baseModelDomain = templateParameters.get('baseModelDomain',None)
    domainList = modelFuncs.getDomainsAsList(modelTypes)
    includeFlatInit = templateParameters.get('includeFlatInit', False)

    def printDefaultValue(property):
        if hasattr(property.type,'default'):
            ret = property.type.default
            if ret is None:
                return None
            elif isinstance(property.type, model.StringType):
                return '"{}"'.format(ret)
            elif isinstance(property.type, model.UuidType):
                return '"{}"'.format(ret)
            else:
                return ret
        else:
            return 'None'

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
class ${type.name}${ ' ({})'.format(pythonFuncs.getExtendsType(type, modelTypes, baseModelDomain)) if modelFuncs.hasTypeExtendsType(type) else ''}:
        % if type.description != None:
    """${templateHelper.addLineBreakToDescription(type.description,4)}
    """

        % endif
    def __init__(self, dictObj=None):
        % if modelFuncs.hasTypeExtendsType(type):
        ${pythonFuncs.getExtendsType(type, modelTypes, baseModelDomain)}.__init__(self)
        % endif
        % if not modelFuncs.hasTypeProperties(type):
        pass
        % else:
            % for property in type.properties:
                % if property.description != None:

        #: ${property.description}
                % endif
        self.${property.name} = ${pythonFuncs.getDefaultPythonValue(property)}
            % endfor
        % endif

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        % if hasattr(type, "properties"):
            % for property in type.properties:
                % if (property.isArray) or (isinstance(property.type, model.DictionaryType)) or (isinstance(property.type, model.ArrayType)):
        if (self.${property.name} is not None) and (len(self.${property.name}) > 0):
                    % if modelFuncs.isBaseType(property.type):
            ret["${property.name}"] = self.${property.name}
                    % elif isinstance(property.type, model.EnumType):
            ret["${property.name}"] = ${property.type.name}.valueAsString(self.${property.name})
                    % else:
            ret["${property.name}"] = self.${property.name}.toDict()
                    % endif
                % else:
        if self.${property.name} is not None:
                    % if modelFuncs.isBaseType(property.type):
            ret["${property.name}"] = self.${property.name}
                    % elif isinstance(property.type, model.EnumType):
            ret["${property.name}"] = ${property.type.name}.valueAsString(self.${property.name})
                    % else:
            ret["${property.name}"] = self.${property.name}.toDict()
                    % endif
                % endif
            % endfor
        % endif
        return ret

        % if includeFlatInit and hasattr(type, "properties") and len(type.properties) > 0:
    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj=None):
        ret = initObj
            % for property in type.properties:
                % if modelFuncs.isBaseType(property.type):
        if attribName == "${property.name}":
            if ret is None:
                ret = ${type.name}()
            ret.${property.name} = value
                % elif isinstance(property.type, model.EnumType):
        if attribName == "${property.name}":
            if ret is None:
                ret = ${type.name}()
            ret.${property.name} = ${property.type.name}.valueForString(value)
                % elif isinstance(property.type, model.ComplexType):
        initObj = ret.${property.name} if ret is not None else None
        ${property.name}Tmp = ${property.type.name}.initWithFlatValue(attribName, value, initObj)
        if ${property.name}Tmp is not None:
            if ret is None:
                ret = ${type.name}()
            ret.${property.name} = ${property.name}Tmp
                % endif
            % endfor
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            % for property in type.properties:
                % if modelFuncs.isBaseType(property.type):
            if key == "${property.name}":
                if ret is None:
                    ret = ${type.name}()
                ret.${property.name} = value
                % elif isinstance(property.type, model.EnumType):
            if key == "${property.name}":
                if ret is None:
                    ret = ${type.name}()
                ret.${property.name} = ${property.type.name}.valueForString(value)
                % elif isinstance(property.type, model.ComplexType):
            initObj = ret.${property.name} if ret is not None else None
            ${property.name}Tmp = ${property.type.name}.initWithFlatValue(key, value, initObj)
            if ${property.name}Tmp is not None:
                if ret is None:
                    ret = ${type.name}()
                ret.${property.name} = ${property.name}Tmp
                % endif
            % endfor
        return ret
        % endif

    def initFromDict(self, dictObj):
        if dictObj is None:
            return
        % if modelFuncs.hasTypeProperties(type):
            % for property in type.properties:
                % if modelFuncs.isBaseOrDictionaryType(property.type):
                    % if not property.isArray:

        self.${property.name} = dictObj.get('${property.name}', ${printDefaultValue(property)})
                    % else:

        array${stringUtils.toUpperCamelCase(property.name)} = dictObj.get('${property.name}', [])
        for elem${stringUtils.toUpperCamelCase(property.name)} in array${stringUtils.toUpperCamelCase(property.name)}:
            self.${property.name}.append(elem${stringUtils.toUpperCamelCase(property.name)})
                    % endif
                % elif modelFuncs.isEnumType(property.type):
                    % if not property.isArray:

        self.${property.name} = ${property.type.name}.valueForString(dictObj.get('${property.name}', None))
                    % else:

        array${stringUtils.toUpperCamelCase(property.name)} = dictObj.get('${property.name}', [])
        for elem${stringUtils.toUpperCamelCase(property.name)} in array${stringUtils.toUpperCamelCase(property.name)}:
            self.${property.name}.append(
                ${property.type.name}.valueForString(elem${stringUtils.toUpperCamelCase(property.name)}))
                    % endif
                % else:
                    % if not property.isArray:

        subDictObj = dictObj.get('${property.name}', ${printDefaultValue(property)})
        if subDictObj is not None:
            self.${property.name} = ${pythonFuncs.getTypeWithPackage(property.type, modelTypes, baseModelDomain)}(subDictObj)
                    % else:

        array${stringUtils.toUpperCamelCase(property.name)} = dictObj.get('${property.name}', [])
        for elem${stringUtils.toUpperCamelCase(property.name)} in array${stringUtils.toUpperCamelCase(property.name)}:
            self.${property.name}.append(
                ${pythonFuncs.getTypeWithPackage(property.type, modelTypes, baseModelDomain)}(elem${stringUtils.toUpperCamelCase(property.name)}))
                    % endif
                % endif
            % endfor
        % endif

    % endif

% endfor
