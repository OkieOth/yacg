<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils

    templateFile = 'golang.mako'
    templateVersion = '1.0.0'

    packageName = templateParameters.get('modelPackage','<<PLEASE SET modelPackage TEMPLATE PARAM>>')


    def printGolangType(typeObj, isArray, isRequired):
        ret = ''
        if typeObj is None:
            return '???'
        elif isinstance(typeObj, model.IntegerType):
            if typeObj.format is None or typeObj.format == model.IntegerTypeFormatEnum.INT32:
                ret = 'int32'
            else:
                ret = 'int'
        elif isinstance(typeObj, model.ObjectType):
            ret = 'interface{}'
        elif isinstance(typeObj, model.NumberType):
            if typeObj.format is None or typeObj.format == model.NumberTypeFormatEnum.DOUBLE:
                ret = 'float64'
            else:
                ret = 'float32'
        elif isinstance(typeObj, model.BooleanType):
            ret = 'bool'
        elif isinstance(typeObj, model.StringType):
            ret = 'string'
        elif isinstance(typeObj, model.BytesType):
            ret = 'byte'
        elif isinstance(typeObj, model.UuidType):
            ret = 'uuid.UUID'
        elif isinstance(typeObj, model.EnumType):
            ret = typeObj.name
        elif isinstance(typeObj, model.DateType):
            ret = 'time.Date'
        elif isinstance(typeObj, model.TimeType):
            ret = 'time.Time'
        elif isinstance(typeObj, model.DateTimeType):
            ret = 'time.Date'
        elif isinstance(typeObj, model.DictionaryType):
            ret = 'map[string]{}'.format(printGolangType(typeObj.valueType, False, True))
        elif isinstance(typeObj, model.ComplexType):
            ret = typeObj.name
        else:
            ret = '???'
        if not isRequired:
            ret = "*" + ret
        if isArray:
            return "[]" + ret
        else:
            return ret

    def getEnumDefaultValue(type):
        if type.default is not None:
            return type.default
        else:
            return type.values[0]

    def isEnumDefaultValue(value, type):
        return True if (type.default is not None) and (value == type.default) else False

%>// Attention, this file is generated. Manual changes get lost with the next
// run of the code generation.
// created by yacg (template: ${templateFile} v${templateVersion})
package ${packageName}

% if modelFuncs.isUuidContained(modelTypes):
import (
    // go get github.com/google/uuid
    // https://pkg.go.dev/github.com/google/uuid#section-readme
	uuid "github.com/google/uuid"
)
% endif

% for type in modelTypes:
    % if modelFuncs.isEnumType(type):
        % if type.description != None:
/* ${templateHelper.addLineBreakToDescription(type.description,4)}
*/
        % endif
const {
    ${getEnumDefaultValue(type)} ${type.name} = ioat
    % for value in type.values:
        % if not isEnumDefaultValue(value, type):
        ${value}
        % endif
    % endfor
}

func (s ${type.name}) String() string {
	switch s {
    % for value in type.values:
	case ${value}:
		return "${value}"
    % endfor
	}
	return "???"
}

    % endif
% endfor

% for type in modelTypes:
    % if (not modelFuncs.isEnumType(type)) and (not modelFuncs.isDictionaryType(type)):
        % if type.description != None:
/* ${templateHelper.addLineBreakToDescription(type.description,4)}
*/
        % endif
type ${type.name} struct {
        % for property in type.properties:

            % if property.description != None:
    // ${property.description}
            % endif
    ${stringUtils.toUpperCamelCase(property.name)} ${printGolangType(property.type, property.isArray, property.required)}
        % endfor
}

    % endif
% endfor