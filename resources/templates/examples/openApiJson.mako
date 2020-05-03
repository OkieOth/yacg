## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.pythonFuncs as pythonFuncs

    templateFile = 'openApiJson.mako'
    templateVersion = '1.0.0'

    def printJsonType(type):
        if type is None:
            return '???'
        elif isinstance(type, model.IntegerType):
            return '"type": "integer"'
        elif isinstance(type, model.NumberType):
            return '"type": "number"'
        elif isinstance(type, model.BooleanType):
            return '"type": "boolean"'
        elif isinstance(type, model.StringType):
            return '"type": "string"'
        elif isinstance(type, model.UuidType):
            return '"type": "string"'
        elif isinstance(type, model.EnumType):
            return '"type": "string"'
        elif isinstance(type, model.DateType):
            return '"type": "string"'
        elif isinstance(type, model.DateTimeType):
            return '"type": "string"'
        elif isinstance(type, model.ComplexType):
            return '"$ref": "#/components/schemas/{}"'.format(type.name)
        else:
            return '"type": "???"'

    def isFormatRequired(type):
        if type is None:
            return False
        elif isinstance(type, model.IntegerType) and (type.format is not None):
            return True
        elif isinstance(type, model.NumberType) and (type.format is not None):
            return True
        elif isinstance(type, model.UuidType):
            return True
        elif isinstance(type, model.DateType):
            return True
        elif isinstance(type, model.DateTimeType):
            return True
        else:
            return False

    def printFormat(type):
        if type is None:
            return ''
        elif isinstance(type, model.IntegerType) and (type.format is not None):
            return ',"format": "{}"'.format(type.format)
        elif isinstance(type, model.NumberType) and (type.format is not None):
            return ',"format": "{}"'.format(type.format)
        elif isinstance(type, model.UuidType):
            return ',"format": "uuid"'
        elif isinstance(type, model.DateType):
            return ',"format": "date"'
        elif isinstance(type, model.DateTimeType):
            return ',"format": "date-time"'
        else:
            return ''

    def isMinRequired(type):
        if type is None:
            return False
        elif isinstance(type, model.IntegerType) and (type.format is not None):
            return True
        elif isinstance(type, model.NumberType) and (type.format is not None):
            return True
        elif isinstance(type, model.DateType):
            return True
        elif isinstance(type, model.DateTimeType):
            return True
        else:
            return False

    title = templateParameters.get('title',"If you set a template param called 'title', then this text appears here")
    description = templateParameters.get('description','This is a simple template that create an OpenApi file')
    description = description + "(created by yacg, template: {} v{})".format(templateFile,templateVersion)
    version = templateParameters.get('version','1.0.0')
    restTypeParam = templateParameters.get('restTypes','')
    restTypeNames = restTypeParam.split(',')
    restTypes = modelFuncs.getTypesWithName(modelTypes,restTypeNames)
    nonEnumModelTypes = modelFuncs.getNonEnumModelType(modelTypes)
%>{
    "openapi": "3.0.1",
    "info": {
        "title": "${title}",
        "description": "${description}",
        "license": {
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "version": "${version}"
    },
    "tags": [
        % for type in restTypes:
        {
            "name": "${type.name}",
            % if type.description != None:
            "description": "${type.description}"
            % endif
        }${',' if type != modelTypes[-1] else ''}
        % endfor
    ],
    "paths": {
        % for type in restTypes:
        % endfor
    },
    "components": {
        "schemas": {
        % for type in nonEnumModelTypes:
            "${type.name}": {
            % if type.description is not None:
                "description": "${type.description}",
            % endif
                "type": "object"
            % if type.extendsType is not None:
                ,"allOf": [{
                        "$ref": "#/components/schemas/${type.extendsType.name}}"
                    }
                % if len(type.properties) > 0:
                    ,{
                        "properties": {
                    % for property in type.properties:
                            "${property.name}": {
                        % if property.description is not None:
                                "description": "${property.description}",
                        % endif
                        % if property.isArray:
                                "type": "array",
                                "items": {
                                    ${printJsonType(property.type)}
                            % if isFormatRequired(property.type):
                                    ${printFormat(property.type)}
                            % endif    
                                }
                        % else:
                                ${printJsonType(property.type)}
                            % if isFormatRequired(property.type):
                                ${printFormat(property.type)}
                            % endif    
                        % endif    
                            }${',' if property != type.properties[-1] else ''}
                    % endfor
                        }
                % endif
                    }
                ]
            % else:
                % if len(type.properties) > 0:
                ,"properties": {
                    % for property in type.properties:
                    "${property.name}": {
                        % if property.description is not None:
                        "description": "${property.description}",
                        % endif
                        % if property.isArray:
                        "type": "array",
                        "items": {
                            ${printJsonType(property.type)}
                            % if isFormatRequired(property.type):
                            ${printFormat(property.type)}
                            % endif    
                        }
                        % else:
                        ${printJsonType(property.type)}
                            % if isFormatRequired(property.type):
                        ${printFormat(property.type)}
                            % endif    
                        % endif    
                    }${',' if property != type.properties[-1] else ''}
                    % endfor
                }
                % endif
            % endif
            }${',' if type != modelTypes[-1] else ''}
        % endfor
        }
    }
}
