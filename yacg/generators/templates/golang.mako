<%
    import re
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils

    templateFile = 'golang_types.mako'
    templateVersion = '1.1.0'

    packageName = templateParameters.get('modelPackage','<<PLEASE SET modelPackage TEMPLATE PARAM>>')
    jsonTypesPackage = templateParameters.get('jsonTypesPackage','<<PLEASE SET jsonTypesPackage TEMPLATE PARAM>>')
    jsonSerialization = templateParameters.get('jsonSerialization',False)

    def printStarForJson(isJson):
        return "*" if isJson else ""

    def printGolangType(typeObj, isArray, isRequired, arrayDimensions, forJson):
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
            if jsonSerialization:
                ret = printStarForJson(forJson and (not isRequired)) + 'bool'
            else:
                ret = 'bool'
        elif isinstance(typeObj, model.StringType):
            ret = 'string'
        elif isinstance(typeObj, model.BytesType):
            ret = 'byte'
        elif isinstance(typeObj, model.UuidType):
            ret = printStarForJson(forJson and (not isRequired)) + 'uuid.UUID'
        elif isinstance(typeObj, model.EnumType):
            ret = typeObj.name
        elif isinstance(typeObj, model.DateType):
            if jsonSerialization:
                ret = printStarForJson(forJson and (not isRequired)) + 'json_types.JsonDate'
            else:
                ret = 'time.Time'
        elif isinstance(typeObj, model.TimeType):
            if jsonSerialization:
                ret = printStarForJson(forJson and (not isRequired)) + 'json_types.JsonTime'
            else:
                ret = 'time.Time'
        elif isinstance(typeObj, model.DateTimeType):
            if jsonSerialization:
                ret = printStarForJson(forJson and (not isRequired)) + 'json_types.JsonTimestamp'
            else:
                ret = 'time.Time'
        elif isinstance(typeObj, model.DictionaryType):
            ret = '{}map[string]{}'.format(printStarForJson(forJson),printGolangType(typeObj.valueType, False, True, 0, False))
        elif isinstance(typeObj, model.ComplexType):
            if (not isArray) and (not isRequired):
                ret = printStarForJson(forJson) + typeObj.name
            else:
                ret = typeObj.name
        else:
            ret = '???'

        if (not isRequired) and (not isArray) and (not isinstance(typeObj, model.DictionaryType)):
            if isinstance(typeObj, model.EnumType) or hasattr(typeObj, "properties"):
                ret = "*{}".format(ret)
            else:
                ret = "*{}".format(ret)
        if isArray:
            ret = printStarForJson(forJson) + ("[]" * arrayDimensions) + ret

        return ret

    def printOmitemptyIfNeeded(property):
        if not property.required or property.isArray or isinstance(property.type, model.DictionaryType):
            return ",omitempty"
        else:
            return ""

    def getEnumDefaultValue(type):
        if type.default is not None:
            return secureEnumValues(type.default, type.name)
        else:
            return secureEnumValues(type.values[0], type.name)

    def secureEnumValues(value, typeName):
        valueName = stringUtils.toName(value)
        typeName = stringUtils.toName(typeName)
        return typeName + "_" + valueName
        #pattern = re.compile("^[0-9]")
        #return '_' + value if pattern.match(value) else value

    def isEnumDefaultValue(value, type):
        return getEnumDefaultValue(type) == secureEnumValues(value, type.name)

    def sanitizePropertyName(property):
        name = property.name
        if name == "type":
            return "type_"
        return name


%>// Attention, this file is generated. Manual changes get lost with the next
// run of the code generation.
// created by yacg (template: ${templateFile} v${templateVersion})
package ${packageName}


import (
% if modelFuncs.isUuidContained(modelTypes):
    uuid "github.com/google/uuid"
% endif
% if modelFuncs.isAtLeastOneDateRelatedTypeContained(modelTypes):
    "time"
% endif
    "encoding/json"
    "errors"
    "fmt"
)

% for type in modelTypes:
    % if modelFuncs.isEnumType(type):
        % if type.description != None:
/* ${templateHelper.addLineBreakToDescription(type.description,4)}
*/
        % endif
type ${type.name} int64

const (
    ${getEnumDefaultValue(type)} ${type.name} = iota
        % for value in type.values:
            % if not isEnumDefaultValue(value, type):
        ${secureEnumValues(value, type.name)}
            % endif
        % endfor
)

func (s ${type.name}) String() string {
	switch s {
        % for value in type.values:
	case ${secureEnumValues(value, type.name)}:
		return "${value}"
        % endfor
	}
	return "???"
}

func (s ${type.name}) MarshalJSON() ([]byte, error) {
    return json.Marshal(s.String())
}

func (s *${type.name}) UnmarshalJSON(data []byte) error {
    var value string
    if err := json.Unmarshal(data, &value); err != nil {
        return err
    }

    switch value {
        % for value in type.values:
    case "${value}":
        *s = ${secureEnumValues(value, type.name)} 
        % endfor
    default:
		msg := fmt.Sprintf("invalid value for DDDDomainType: %s", value)
		return errors.New(msg)
    }
    return nil
}

    % endif

    % if hasattr(type, "properties"):
        % if type.description != None:
/* ${templateHelper.addLineBreakToDescription(type.description,4)}
*/
        % endif
type ${type.name} struct {
        % for property in type.properties:

            % if property.description != None:
    // ${property.description}
            % endif
    ${stringUtils.toUpperCamelCase(property.name)} ${printGolangType(property.type, property.isArray, property.required, property.arrayDimensions, False)}  `json:"${property.name}${printOmitemptyIfNeeded(property)}"`
        % endfor
} 


func Make${type.name}Builder() *${type.name}Builder {
	var b ${type.name}Builder
    b.Init()
	return &b
}

type ${type.name}Builder struct {
        % for property in type.properties:
    ${sanitizePropertyName(property)} ${printGolangType(property.type, property.isArray, property.required, property.arrayDimensions, False)}
        % endfor
}

func (b *${type.name}Builder) Init() {
        % for property in type.properties:
            % if property.isArray:
    b.${sanitizePropertyName(property)} = make(${"[]" * property.arrayDimensions}${printGolangType(property.type, True, True, 0, False)}, 0)
            % endif
            % if isinstance(property.type, model.DictionaryType):
    b.${sanitizePropertyName(property)} = make(${printGolangType(property.type, False, True, 0, False)})
            % endif
        % endfor
}



        % for property in type.properties:
            % if property.required or property.isArray or isinstance(property.type, model.DictionaryType):
func (b *${type.name}Builder) ${stringUtils.toUpperCamelCase(property.name)}(v ${printGolangType(property.type, property.isArray, True, property.arrayDimensions, False)}) *${type.name}Builder {
	b.${sanitizePropertyName(property)} = v
	return b
}
            % else:
func (b *${type.name}Builder) ${stringUtils.toUpperCamelCase(property.name)}(v ${printGolangType(property.type, False, False, property.arrayDimensions, False)}) *${type.name}Builder {
	b.${sanitizePropertyName(property)} = v
	return b
}
            % endif
        % endfor
func (b *${type.name}Builder) Build() ${type.name} {
	var r ${type.name}
        % for property in type.properties:
    r.${stringUtils.toUpperCamelCase(property.name)} = b.${sanitizePropertyName(property)}
        % endfor
	return r
}



    % endif


% endfor
