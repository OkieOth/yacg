## Template to create a proto buffer file with type definitions of the model types
<%
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.model.model as model

    templateFile = 'protobuf.mako'
    templateVersion = '1.0.0'

    baseModelDomain = templateParameters.get('baseModelDomain',None)
    domainList = modelFuncs.getDomainsAsList(modelTypes)

    def printArray(property):
        return 'repeated ' if property.isArray else ''

    def getType(property):
        type = property.type
        if type is None:
            return '???'
        elif isinstance(type, model.IntegerType):
            if type.format is None:
                return 'int32'
            elif type.format is model.IntegerTypeFormatEnum.INT32:
                return 'int32'
            elif type.format is model.IntegerTypeFormatEnum.INT64:
                return 'int64'
            else:
                return 'int32'
        elif isinstance(type, model.NumberType):
            return 'double'
        elif isinstance(type, model.BooleanType):
            return 'bool'
        elif isinstance(type, model.StringType):
            return 'string'
        elif isinstance(type, model.UuidType):
            return 'string'
        elif isinstance(type, model.EnumType):
            return type.name
        elif isinstance(type, model.DateType):
            return 'google.protobuf.Date'
        elif isinstance(type, model.DateTimeType):
            return 'google.protobuf.Timestamp'
        elif isinstance(type, model.ComplexType):
            return type.name
        else:
            return '???'


%>/* Attention, this file is generated. Manual changes get lost with the next
* run of the code generation.
* created by yacg (template: ${templateFile} v${templateVersion}) */

syntax = "proto3";

import "google/protobuf/timestamp.proto";
import "google/protobuf/date.proto";

% for type in modelTypes:
    % if modelFuncs.isEnumType(type):    
enum ${type.name} {
        % for i in range(len(type.values)) :
    ${stringUtils.toUpperCaseName(type.values[i])} = ${i};
        % endfor
}


    % else:
        % if type.description != None:
/*${templateHelper.addLineBreakToDescription(type.description,4)}
*/
        % endif
message ${type.name} {
    <% flattenProperties = modelFuncs.getFlattenProperties(type) %>
        % for i in range(len(flattenProperties)):
                % if type.description != None:
        // ${type.description}
                % endif
        ${printArray(flattenProperties[i])}${getType(flattenProperties[i])} ${flattenProperties[i].name} = ${i+1};

        % endfor
}


    % endif
% endfor