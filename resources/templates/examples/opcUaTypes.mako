<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.dateUtils as dateUtils

    templateFile = 'opcUaTypes.mako'
    templateVersion = '1.0.0'

    usedIds = {}
    lastUsedId = [0]
    usedModelTypes = {}
    aliasBlacklist = {}
    opcUaPrimitives = {
        'Boolean': 1,
        'Int32': 6,
        'Int64': 8,
        'Float': 10,
        'Double': 11,
        'String': 12
    }

    modelVersion = templateParameters.get('modelVersion', 'null')
    descriptionLocale = templateParameters.get('locale','null')
    nsIndex = templateParameters.get('nsIndex', '1')

    for type in modelTypes:
        if isinstance(type, model.ComplexType):
            for prop in type.properties:
                if isinstance(prop.type, model.ComplexType):
                    aliasBlacklist[prop.type.name] = True

    def printId(typeName):
        existingId = usedIds.get(typeName, None)
        if existingId is not None:
            return existingId
        else:
            lastUsedId[0] = lastUsedId[0] + 1
            usedIds[typeName] = lastUsedId[0]
            return lastUsedId[0]

    def getValueDataTypeNameFromType(type):
        value = modelFuncs.getProperty('value', type)
        if value is None:
            return None
        else:
            return value.type.name
    
    def getComplexTypeNameFromMethodArgs(method):
        arguments = modelFuncs.getProperty('__arguments', method)
        if arguments is None:
            return None
        else:
            return arguments.type.name

    def getArgsFromType(type):
        return modelFuncs.getProperty('__arguments', type)

    def isTypePropertyTrue(type, propertyName):
        return modelFuncs.hasProperty(propertyName, type) and modelFuncs.getProperty(propertyName, type).type.default

    def getOpcUaPrimitive(type):
        opcUaPrimitiveType = 'InvalidTypeName'

        if isinstance(type, model.IntegerType):
            if type.format == model.IntegerTypeFormatEnum.INT32:
                opcUaPrimitiveType = 'Int32'
            else:
                opcUaPrimitiveType = 'Int64'
        elif isinstance(type, model.NumberType):
            if type.format == model.NumberTypeFormatEnum.FLOAT:
                opcUaPrimitiveType = 'Float'
            else:
                opcUaPrimitiveType = 'Double'
        elif isinstance(type, model.BooleanType):
            opcUaPrimitiveType = 'Boolean'
        elif isinstance(type, model.StringType):
            opcUaPrimitiveType = 'String'

        return opcUaPrimitiveType

%>
<UANodeSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd" xmlns:uax="http://opcfoundation.org/UA/2008/02/Types.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:s${nsIndex}="http://swarco.com/Types/${modelVersion}">
    <NamespaceUris>
        <Uri>http://swarco.com/Types/${modelVersion}</Uri>
    </NamespaceUris>

    <Models>
        <Model ModelUri="http://swarco.com/Types/${modelVersion}" Version="${modelVersion}" PublicationDate="${dateUtils.getCurrentIsoDateTime()}">
            <RequiredModel ModelUri="http://opcfoundation.org/UA/" Version="1.04.7"></RequiredModel>
        </Model>
    </Models>

    <Aliases>
% for primitive in opcUaPrimitives:
        <Alias Alias="${primitive}">i=${opcUaPrimitives[primitive]}</Alias>
% endfor
        <Alias Alias="Enumeration">i=29</Alias>
        <Alias Alias="HasTypeDefinition">i=40</Alias>
        <Alias Alias="HasSubtype">i=45</Alias>
        <Alias Alias="HasProperty">i=46</Alias>
        <Alias Alias="HasComponent">i=47</Alias>
        <Alias Alias="PropertyType">i=68</Alias>
        <Alias Alias="Argument">i=296</Alias>
        <Alias Alias="EnumValueType">i=7594</Alias>
% for type in modelTypes:
    % if aliasBlacklist.get(type.name) is None:
        <Alias Alias="${type.name}">ns=${nsIndex};i=${printId(type.name)}</Alias>
    % endif
% endfor
    </Aliases>

% for type in modelTypes:
    % if usedModelTypes.get(type.name) is None:
        % if isinstance(type, model.ComplexType):
    <UAObjectType NodeId="ns=${nsIndex};i=${printId(type.name)}" BrowseName="${nsIndex}:${type.name}">
            % if type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
            % endif
        <DisplayName>${type.name}</DisplayName>
        <References>
                % for prop in type.properties:
            <Reference ReferenceType="HasComponent">ns=${nsIndex};i=${printId(prop.type.name)}</Reference>
                % endfor
        </References>
    </UAObjectType>

            % for prop in type.properties:

                % if isTypePropertyTrue(prop.type, '__isMethod'):
    <UAMethod NodeId="ns=${nsIndex};i=${printId(prop.type.name)}" BrowseName="${nsIndex}:${prop.name}" ParentNodeId="ns=${nsIndex};i=${printId(type.name)}">
        <DisplayName>${prop.name}</DisplayName>
        <References>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">ns=${nsIndex};i=${printId(type.name)}</Reference>
            <Reference ReferenceType="HasProperty">ns=${nsIndex};i=${printId(prop.type.name + 'InputArguments')}</Reference>
                    % for innerProp in prop.type.properties:
                         % if not innerProp.name.startswith('__'):
            <Reference ReferenceType="HasProperty">ns=${nsIndex};i=${printId(prop.type.name + innerProp.name)}</Reference>
                        % endif
                    % endfor
        </References>
    </UAMethod>
    <UAVariable NodeId="ns=${nsIndex};i=${printId(prop.type.name + 'InputArguments')}" BrowseName="${nsIndex}:InputArguments" DataType="Argument" ValueRank="1" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>InputArguments</DisplayName>
        <References>
            <Reference ReferenceType="HasTypeDefinition">i=68</Reference>
            <Reference ReferenceType="HasProperty" IsForward="false">ns=${nsIndex};i=${printId(prop.type.name)}</Reference>
        </References>
        <Value>
            <uax:ListOfExtensionObject>
                    % if getArgsFromType(prop.type).isArray and isinstance(getArgsFromType(prop.type).arrayMinItems, int) and getArgsFromType(prop.type).arrayMinItems > 1:
                        % for i in range(getArgsFromType(prop.type).arrayMinItems):
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=296</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:Argument>
                            <uax:Name>${prop.name}${i}</uax:Name>
                            <uax:DataType>
                            % if getOpcUaPrimitive(getArgsFromType(prop.type).type).lower().startswith('invalid'):
                                <uax:Identifier>ns=${nsIndex};i=${printId(getComplexTypeNameFromMethodArgs(prop.type))}</uax:Identifier>
                            % else:
                                <uax:Identifier>i=${opcUaPrimitives.get(getOpcUaPrimitive(getArgsFromType(prop.type).type))}</uax:Identifier>
                            % endif
                            </uax:DataType>
                            <uax:ValueRank>-1</uax:ValueRank>
                            <uax:ArrayDimensions></uax:ArrayDimensions>
                            <uax:Description></uax:Description>
                        </uax:Argument>
                    </uax:Body>
                </uax:ExtensionObject>
                        % endfor
                    % else:
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=296</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:Argument>
                            <uax:Name>${prop.name}</uax:Name>
                            <uax:DataType>
                            % if getOpcUaPrimitive(getArgsFromType(prop.type).type).lower().startswith('invalid'):
                                <uax:Identifier>ns=${nsIndex};i=${printId(getComplexTypeNameFromMethodArgs(prop.type))}</uax:Identifier>
                            % else:
                                <uax:Identifier>i=${opcUaPrimitives.get(getOpcUaPrimitive(getArgsFromType(prop.type).type))}</uax:Identifier>
                            % endif
                            </uax:DataType>
                            <uax:ValueRank>-1</uax:ValueRank>
                            <uax:ArrayDimensions></uax:ArrayDimensions>
                            <uax:Description></uax:Description>
                        </uax:Argument>
                    </uax:Body>
                </uax:ExtensionObject>
                    % endif
            </uax:ListOfExtensionObject>
        </Value>
    </UAVariable>
                % else:
    <UAVariable NodeId="ns=${nsIndex};i=${printId(prop.type.name)}" BrowseName="${nsIndex}:${prop.name}" ParentNodeId="ns=${nsIndex};i=${printId(type.name)}" DataType="${getValueDataTypeNameFromType(prop.type)}" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
                    % if prop.type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
                    % endif
        <DisplayName>${prop.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">ns=${nsIndex};i=${printId(type.name)}</Reference>
                % for innerProp in prop.type.properties:
                    % if innerProp.name != 'value':
            <Reference ReferenceType="HasProperty">ns=${nsIndex};i=${printId(prop.type.name + innerProp.name)}</Reference>
                    % endif
                % endfor
        </References>
    </UAVariable>
                % endif

                % for innerProp in prop.type.properties:
                    % if not innerProp.name.startswith('__') and innerProp.name != 'value':
    <UAVariable NodeId="ns=${nsIndex};i=${printId(prop.type.name + innerProp.name)}" BrowseName="${nsIndex}:${innerProp.name}" DataType="${getOpcUaPrimitive(innerProp.type)}" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>${innerProp.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty" IsForward="false">ns=${nsIndex};i=${printId(prop.type.name)}</Reference>
        </References>
                        % if innerProp.type.default is not None:
        <Value>
            ${innerProp.type.default}
        </Value>
                        % endif
    </UAVariable>
                    % endif
                % endfor

                <% usedModelTypes[prop.type.name] = True %>
                    
            % endfor

        % else:
    <UADataType NodeId="ns=${nsIndex};i=${printId(type.name)}" BrowseName="${nsIndex}:${type.name}" IsAbstract="false">
        <DisplayName>${type.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty">ns=${nsIndex};${printId(type.name + 'EnumStrings')}</Reference>
            <Reference ReferenceType="HasSubtype" IsForward="false">i=29</Reference>
        </References>
    </UADataType>
    <UAVariable NodeId="ns=${nsIndex};i=${printId(type.name + 'EnumStrings')}" BrowseName="${nsIndex}:EnumStrings" DataType="EnumValueType" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>EnumStrings</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty" IsForward="false">ns=${nsIndex};i=${printId(type.name)}</Reference>
            <Reference ReferenceType="HasTypeDefinition">i=68</Reference>
        </References>
        <Value>
            <uax:ListOfExtensionObject>
                % for enumValue in type.values:
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=7594</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:EnumValueType>
                            <uax:Value>${loop.index}</uax:Value>
                            <uax:DisplayName>
                                <uax:Locale></uax:Locale>
                                <uax:Text>${enumValue}</uax:Text>
                            </uax:DisplayName>
                        </uax:EnumValueType>
                    </uax:Body>
                </uax:ExtensionObject>
                % endfor 
            </uax:ListOfExtensionObject>
        </Value>
    </UAVariable>
        % endif

    % endif
% endfor
</UANodeSet>