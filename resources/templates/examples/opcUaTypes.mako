<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.dateUtils as dateUtils

    templateFile = 'opcUaTypes.mako'
    templateVersion = '1.0.0'

    usedIds = {}
    lastUsedId = [0]

    modelVersion = templateParameters.get('modelVersion', 'null')
    descriptionLocale = templateParameters.get('locale','null')

    def printId(typeName):
        existingId = usedIds.get(typeName, None)
        if existingId is not None:
            return existingId
        else:
            lastUsedId[0] = lastUsedId[0] + 1
            usedIds[typeName] = lastUsedId[0]
            return lastUsedId[0]

    def getDataTypeFromProperty(property):
        dataType = modelFuncs.getProperty('__dataType', property)
        if dataType is None:
            return None
        else:
            return dataType.type.name
    
    def getTypeFromMethodArgs(method):
        arguments = modelFuncs.getProperty('__arguments', method)
        if arguments is None:
            return None
        else:
            return arguments.type.name

%>
<UANodeSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd" xmlns:uax="http://opcfoundation.org/UA/2008/02/Types.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:s1="http://swarco.com/Types/Base/${modelVersion}">
    <NamespaceUris>
        <Uri>http://swarco.com/Types/Base/${modelVersion}</Uri>
    </NamespaceUris>

    <Models>
        <Model ModelUri="http://swarco.com/Types/Base/${modelVersion}" Version="${modelVersion}" PublicationDate="${dateUtils.getCurrentIsoDateTime()}">
            <RequiredModel ModelUri="http://opcfoundation.org/UA/" Version="1.04.7"></RequiredModel>
        </Model>
    </Models>

    <Aliases>
        <Alias Alias="Enumeration">i=29</Alias>
        <Alias Alias="HasTypeDefinition">i=40</Alias>
        <Alias Alias="HasSubtype">i=45</Alias>
        <Alias Alias="HasProperty">i=46</Alias>
        <Alias Alias="HasComponent">i=47</Alias>
        <Alias Alias="PropertyType">i=68</Alias>
        <Alias Alias="Argument">i=296</Alias>
        <Alias Alias="EnumValueType">i=7594</Alias>
% for type in modelTypes:
    % if not (modelFuncs.hasProperty('__isDataProperty', type) or modelFuncs.hasProperty('__isMethod', type)):
        <Alias Alias="${type.name}">ns=1;i=${printId(type.name)}</Alias>
    % endif
% endfor
    </Aliases>

% for type in modelTypes:
    % if modelFuncs.hasProperty('__isObjectType', type):
    <UAObjectType NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}">
        % if type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
        % endif
        <DisplayName>${type.name}</DisplayName>
        <References>
            % for prop in type.properties:
                % if not prop.name.startswith('__'):
            <Reference ReferenceType="HasComponent">ns=1;i=${printId(prop.type.name)}</Reference>
                % endif
            % endfor
        </References>
    </UAObjectType>

        % for prop in type.properties:

            % if not prop.name.startswith('__'):

                % if modelFuncs.hasProperty('__isDataProperty', prop.type):
    <UAVariable NodeId="ns=1;i=${printId(prop.type.name)}" BrowseName="1:${prop.name}" ParentNodeId="ns=1;i=${printId(type.name)}" DataType="${getDataTypeFromProperty(prop.type)}" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
                    % if prop.type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
                    % endif
        <DisplayName>${prop.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">ns=1;i=${printId(type.name)}</Reference>
        </References>
    </UAVariable>

                % elif modelFuncs.hasProperty('__isMethod', prop.type):
    <UAMethod NodeId="ns=1;i=${printId(prop.type.name)}" BrowseName="1:${prop.name}" ParentNodeId="ns=1;i=${printId(type.name)}">
        <DisplayName>${prop.name}</DisplayName>
        <References>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">ns=1;i=${printId(type.name)}</Reference>
            <Reference ReferenceType="HasProperty">ns=1;i=${printId(prop.type.name + 'InputArguments')}</Reference>
        </References>
    </UAMethod>
    <UAVariable NodeId="ns=1;i=${printId(prop.type.name + 'InputArguments')}" BrowseName="1:InputArguments" DataType="Argument" ValueRank="1" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>InputArguments</DisplayName>
        <References>
            <Reference ReferenceType="HasTypeDefinition">i=68</Reference>
            <Reference ReferenceType="HasProperty" IsForward="false">ns=1;i=${printId(prop.type.name)}</Reference>
        </References>
        <Value>
            <uax:ListOfExtensionObject>
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=296</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:Argument>
                            <uax:Name>${prop.name}</uax:Name>
                            <uax:DataType>
                                <uax:Identifier>ns=1;i=${printId(getTypeFromMethodArgs(prop.type))}</uax:Identifier>
                            </uax:DataType>
                            <uax:ValueRank>-1</uax:ValueRank>
                            <uax:ArrayDimensions></uax:ArrayDimensions>
                            <uax:Description></uax:Description>
                        </uax:Argument>
                    </uax:Body>
                </uax:ExtensionObject>
            </uax:ListOfExtensionObject>
        </Value>
    </UAVariable>
                % endif

            % endif

        % endfor

    % elif modelFuncs.hasProperty('__isDataType', type):
    <UADataType NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}" IsAbstract="false">
        <DisplayName>${type.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty">ns=1;${printId(type.name + 'EnumStrings')}</Reference>
            <Reference ReferenceType="HasSubtype" IsForward="false">i=29</Reference>
        </References>
    </UADataType>
    <UAVariable NodeId="ns=1;i=${printId(type.name + 'EnumStrings')}" BrowseName="1:EnumStrings" DataType="EnumValueType" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>EnumStrings</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty" IsForward="false">ns=1;i=${printId(type.name)}</Reference>
            <Reference ReferenceType="HasTypeDefinition">i=68</Reference>
        </References>
        <Value>
            <uax:ListOfExtensionObject>
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=7594</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:EnumValueType>
                            <uax:Value>0</uax:Value>
                            <uax:DisplayName>
                                <uax:Locale></uax:Locale>
                                <uax:Text>Inaktiv</uax:Text>
                            </uax:DisplayName>
                        </uax:EnumValueType>
                    </uax:Body>
                </uax:ExtensionObject>
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=7594</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:EnumValueType>
                            <uax:Value>1</uax:Value>
                            <uax:DisplayName>
                                <uax:Locale></uax:Locale>
                                <uax:Text>Aktiv</uax:Text>
                            </uax:DisplayName>
                        </uax:EnumValueType>
                    </uax:Body>
                </uax:ExtensionObject>
            </uax:ListOfExtensionObject>
        </Value>
    </UAVariable>

    % endif
% endfor
</UANodeSet>