<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.dateUtils as dateUtils

    templateFile = 'opcUaTypes.mako'
    templateVersion = '1.0.0'

    usedIds = {}
    lastUsedId = [0]
    usedModelTypes = {}

    modelVersion = templateParameters.get('modelVersion', 'null')
    descriptionLocale = templateParameters.get('locale','null')
    nsIndex = templateParameters.get('nsIndex', '1')

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

    def getArgsFromType(type):
        return modelFuncs.getProperty('__arguments', prop.type)

    def isTypePropertyTrue(type, propertyName):
        return modelFuncs.hasProperty(propertyName, type) and modelFuncs.getProperty(propertyName, type).type.default

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
        <Alias Alias="Boolean">i=1</Alias>
        <Alias Alias="SByte">i=2</Alias>
        <Alias Alias="Byte">i=3</Alias>
        <Alias Alias="Int16">i=4</Alias>
        <Alias Alias="UInt16">i=5</Alias>
        <Alias Alias="Int32">i=6</Alias>
        <Alias Alias="UInt32">i=7</Alias>
        <Alias Alias="Int64">i=8</Alias>
        <Alias Alias="UInt64">i=9</Alias>
        <Alias Alias="Float">i=10</Alias>
        <Alias Alias="Double">i=11</Alias>
        <Alias Alias="DateTime">i=13</Alias>
        <Alias Alias="String">i=12</Alias>
        <Alias Alias="ByteString">i=15</Alias>
        <Alias Alias="Guid">i=14</Alias>
        <Alias Alias="XmlElement">i=16</Alias>
        <Alias Alias="NodeId">i=17</Alias>
        <Alias Alias="ExpandedNodeId">i=18</Alias>
        <Alias Alias="QualifiedName">i=20</Alias>
        <Alias Alias="LocalizedText">i=21</Alias>
        <Alias Alias="StatusCode">i=19</Alias>
        <Alias Alias="Structure">i=22</Alias>
        <Alias Alias="Number">i=26</Alias>
        <Alias Alias="Integer">i=27</Alias>
        <Alias Alias="UInteger">i=28</Alias>
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
        <Alias Alias="${type.name}">ns=${nsIndex};i=${printId(type.name)}</Alias>
    % endif
% endfor
    </Aliases>

% for type in modelTypes:
    % if usedModelTypes.get(type.name, None) is None:
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

                % if isTypePropertyTrue(prop.type, '__isDataProperty'):
    <UAVariable NodeId="ns=${nsIndex};i=${printId(prop.type.name)}" BrowseName="${nsIndex}:${prop.name}" ParentNodeId="ns=${nsIndex};i=${printId(type.name)}" DataType="${getDataTypeFromProperty(prop.type)}" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
                    % if prop.type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
                    % endif
        <DisplayName>${prop.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">ns=${nsIndex};i=${printId(type.name)}</Reference>
                % for innerProp in prop.type.properties:
                    % if not innerProp.name.startswith('__'):
            <Reference ReferenceType="HasProperty">ns=${nsIndex};i=${printId(prop.type.name + innerProp.name)}</Reference>
                    % endif
                % endfor
        </References>
    </UAVariable>

                % elif isTypePropertyTrue(prop.type, '__isMethod'):
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
                                <uax:Identifier>ns=${nsIndex};i=${printId(getTypeFromMethodArgs(prop.type))}</uax:Identifier>
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
                                <uax:Identifier>ns=${nsIndex};i=${printId(getTypeFromMethodArgs(prop.type))}</uax:Identifier>
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
                % endif

                 % for innerProp in prop.type.properties:
                    % if not innerProp.name.startswith('__'):
    <UAVariable NodeId="ns=${nsIndex};i=${printId(prop.type.name + innerProp.name)}" BrowseName="${nsIndex}:${innerProp.name}" DataType="???" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>${innerProp.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty" IsForward="false">ns=${nsIndex};i=${printId(prop.type.name)}</Reference>
        </References>
        <Value>
            ${innerProp.type.default}
        </Value>
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