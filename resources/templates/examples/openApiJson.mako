## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.jsonFuncs as jsonFuncs

    templateFile = 'openApiJson.mako'
    templateVersion = '1.0.0'

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
        "/${stringUtils.toLowerCamelCase(type.name)}": {
            "get": {
                "tags": [
                    "${type.name}"
                ],
                "description": "Returns a list of ${type.name} entries",
                "operationId": "get${type.name}",
                "responses": {
                    "200": {
                        "description": "successful operation",
                        "content": {
                        "application/xml": {
                            "schema": {
                            "$ref": "#/components/schemas/${type.name}"
                            }
                        },
                        "application/json": {
                            "schema": {
                            "$ref": "#/components/schemas/${type.name}"
                            }
                        }
                        }
                    },
                    "500": {
                        "description": "in case of errors",
                        "content": {}
                    }
                },
            }
        }${',' if type != restTypes[-1] else ''}
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
                        "$ref": "#/components/schemas/${type.extendsType.name}"
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
                                    ${jsonFuncs.printOpenApiJsonTypeEntry(property.type)}
                            % if jsonFuncs.isEnumRequired(property.type):
                                    ,${jsonFuncs.printOpenApiJsonEnumEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isFormatRequired(property.type):
                                    ${jsonFuncs.printOpenApiJsonFormatEntry(property.type)}
                            % endif
                            % if jsonFuncs.isMinRequired(property.type):
                                    ,"minimum": "${property.type.minimum}"
                            % endif
                            % if jsonFuncs.isExclusiveMinRequired(property.type):
                                    ,"exclusiveMinimum": "${property.type.exclusiveMinimum}"
                            % endif
                            % if jsonFuncs.isMaxRequired(property.type):
                                    ,"maximum": "${property.type.maximum}"
                            % endif
                            % if jsonFuncs.isExclusiveMaxRequired(property.type):
                                    ,"exclusiveMaximum": "${property.type.exclusiveMaximum}"
                            % endif
                            % if jsonFuncs.isDefaultRequired(property.type):
                                    ,"default": "${property.type.default}"
                            % endif
                                }
                        % else:
                                ${jsonFuncs.printOpenApiJsonTypeEntry(property.type)}
                            % if jsonFuncs.isEnumRequired(property.type):
                                ,${jsonFuncs.printOpenApiJsonEnumEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isFormatRequired(property.type):
                                ${jsonFuncs.printOpenApiJsonFormatEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isMinRequired(property.type):
                                ,"minimum": "${property.type.minimum}"
                            % endif
                            % if jsonFuncs.isExclusiveMinRequired(property.type):
                                ,"exclusiveMinimum": "${property.type.exclusiveMinimum}"
                            % endif
                            % if jsonFuncs.isMaxRequired(property.type):
                                ,"maximum": "${property.type.maximum}"
                            % endif
                            % if jsonFuncs.isExclusiveMaxRequired(property.type):
                                ,"exclusiveMaximum": "${property.type.exclusiveMaximum}"
                            % endif
                            % if jsonFuncs.isDefaultRequired(property.type):
                                ,"default": "${property.type.default}"
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
                            ${jsonFuncs.printOpenApiJsonTypeEntry(property.type)}
                            % if jsonFuncs.isEnumRequired(property.type):
                            ,${jsonFuncs.printOpenApiJsonEnumEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isFormatRequired(property.type):
                            ${jsonFuncs.printOpenApiJsonFormatEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isMinRequired(property.type):
                            ,"minimum": "${property.type.minimum}"
                            % endif
                            % if jsonFuncs.isExclusiveMinRequired(property.type):
                            ,"exclusiveMinimum": "${property.type.exclusiveMinimum}"
                            % endif
                            % if jsonFuncs.isMaxRequired(property.type):
                            ,"maximum": "${property.type.maximum}"
                            % endif
                            % if jsonFuncs.isExclusiveMaxRequired(property.type):
                            ,"exclusiveMaximum": "${property.type.exclusiveMaximum}"
                            % endif
                            % if jsonFuncs.isDefaultRequired(property.type):
                            ,"default": "${property.type.default}"
                            % endif
                        }
                        % else:
                        ${jsonFuncs.printOpenApiJsonTypeEntry(property.type)}
                            % if jsonFuncs.isEnumRequired(property.type):
                        ,${jsonFuncs.printOpenApiJsonEnumEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isFormatRequired(property.type):
                        ${jsonFuncs.printOpenApiJsonFormatEntry(property.type)}
                            % endif    
                            % if jsonFuncs.isMinRequired(property.type):
                        ,"minimum": "${property.type.minimum}"
                            % endif
                            % if jsonFuncs.isExclusiveMinRequired(property.type):
                        ,"exclusiveMinimum": "${property.type.exclusiveMinimum}"
                            % endif
                            % if jsonFuncs.isMaxRequired(property.type):
                        ,"maximum": "${property.type.maximum}"
                            % endif
                            % if jsonFuncs.isExclusiveMaxRequired(property.type):
                        ,"exclusiveMaximum": "${property.type.exclusiveMaximum}"
                            % endif
                            % if jsonFuncs.isDefaultRequired(property.type):
                        ,"default": "${property.type.default}"
                            % endif
                        % endif    
                    }${',' if property != type.properties[-1] else ''}
                    % endfor
                }
                % endif
            % endif
            }${',' if type != nonEnumModelTypes[-1] else ''}
        % endfor
        }
    }
}
