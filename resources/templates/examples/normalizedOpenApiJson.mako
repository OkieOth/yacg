## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.model.openapi as openapi
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

    tags = modelFuncs.getOpenApiTags(modelTypes)
    (pathTypes, nonEnumTypes, enumTypes) = modelFuncs.separateOpenApiPathTypes(modelTypes)
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
        % for tag in tags:
        {
            "name": "${tag}"
        }${',' if tag != tags[-1] else ''}
        % endfor
    ],
    "paths": {
        % for pathType in pathTypes:
        "${pathType.pathPattern}": {
            % for command in pathType.commands:
            "${command.command.value.lower()}": {
                "operationId": "${command.operationId}",
                % if command.summary is not None:
                "summary": "${command.summary}",
                % endif
                % if command.description is not None:
                "description": "${command.description}",
                % endif
                "tags": [
                    % for tag in command.tags:
                    "${tag}"${',' if tag != command.tags[-1] else ''}
                    % endfor
                ],
                % if len(command.parameters) > 0:
                "parameters": [
                    % for param in command.parameters:
                    {
                        % if param.description is not None:
                        "description": "${param.description}",
                        % endif
                        "required": ${'true' if param.required is True else 'false'},
                        "in": "${param.inType.value}",
                        "name": "${param.name}",
                        "schema": {
                            
                        }
                    }${',' if param != command.parameters[-1] else ''}
                    % endfor
                ],
                % endif
                % if command.requestBody is not None:
                "requestBody": {
                    % if command.requestBody.description is not None:
                    "description": "${command.requestBody.description}",
                    % endif
                    "required": ${'true' if command.requestBody.required is True else 'false'},
                    "content": {
                    % for content in command.requestBody.content:
                        "${content.mimeType}": {
                            "schema": {
                        % if content.isArray:
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/${content.type.name}"
                                }
                        % else:
                                "$ref": "#/components/schemas/${content.type.name}"
                        % endif 
                            }
                        }${',' if content != command.requestBody.content[-1] else ''}
                    % endfor
                    }
                },
                % endif
                "responses": {
                % for response in command.responses:
                    "${response.returnCode}": {
                    % if response.description is not None:
                        "description": "${response.description}",
                    % endif
                        "content": {
                        % for content in response.content:
                            "${content.mimeType}": {
                                "schema": {
                            % if content.isArray:
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/${content.type.name}"
                                    }
                            % else:
                                    "$ref": "#/components/schemas/${content.type.name}"
                            % endif 
                                }
                            }${',' if content != response.content[-1] else ''}
                        % endfor
                        }
                    }${',' if response != command.responses[-1] else ''}
                % endfor
                }
            }${',' if command != pathType.commands[-1] else ''}
            % endfor
        }${',' if pathType != pathTypes[-1] else ''}
        % endfor
    },
    "components": {
        "schemas": {
        % for type in nonEnumTypes:
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
            }${',' if type != nonEnumTypes[-1] else ''}
        % endfor
        }
    }
}
