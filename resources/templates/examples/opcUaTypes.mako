<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.dateUtils as dateUtils

    templateFile = 'opcUaTypes.mako'
    templateVersion = '1.0.0'

    usedIds = {}
    lastUsedId = [0]

    modelVersion = templateParameters.get('modelVersion', '???')
    descriptionLocale = templateParameters.get('locale','???')

    def printId(typeName):
        existingId = usedIds.get(typeName, None)
        if existingId is not None:
            return existingId
        else:
            lastUsedId[0] = lastUsedId[0] + 1
            usedIds[typeName] = lastUsedId[0]
            return lastUsedId[0]

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
% for type in modelTypes:
    % if not modelFuncs.hasTag('opcUaTag', type):
        <Alias Alias="${type.name}">ns=1;i=${printId(type.name)}</Alias>
    % endif
% endfor
    </Aliases>

% for type in modelTypes:
    % if not modelFuncs.hasTag('opcUaTag', type):
    % if type.extendsType.name == 'UAObjectType':
    <UAObjectType NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}">
        % if type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
        % endif
        <DisplayName>${type.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasComponent">???</Reference>
            <Reference ReferenceType="HasComponent">???</Reference>
        </References>
    </UAObjectType>

    % elif type.extendsType.name == 'UAVariable':
    <UAVariable NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}" ParentNodeId="" DataType="" ValueRank="1" ArrayDimensions="0" AccessLevel="1" UserAccessLevel="1">
        % if type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
        % endif
        <DisplayName>${type.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">???</Reference>
        </References>
    </UAVariable>

    % elif type.extendsType.name == 'UAMethod':
    <UAMethod NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}" ParentNodeId="???">
        <DisplayName>${type.name}</DisplayName>
        <References>
        <References>
            <Reference ReferenceType="HasComponent" IsForward="false">???</Reference>
            <Reference ReferenceType="HasProperty">???</Reference>
        </References>
    </UAMethod>
    <UAVariable NodeId="???" BrowseName="1:InputArguments" DataType="Argument" ValueRank="1" AccessLevel="1" UserAccessLevel="1">
        <DisplayName>InputArguments</DisplayName>
        <References>
            <Reference ReferenceType="HasTypeDefinition">i=68</Reference>
            <Reference ReferenceType="HasProperty" IsForward="false">???</Reference>
        </References>
        <Value>
            <uax:ListOfExtensionObject>
                <uax:ExtensionObject>
                    <uax:TypeId>
                        <uax:Identifier>i=296</uax:Identifier>
                    </uax:TypeId>
                    <uax:Body>
                        <uax:Argument>
                            <uax:Name>${type.name}</uax:Name>
                            <uax:DataType>
                                <uax:Identifier>???</uax:Identifier>
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

    % elif type.extendsType.name == 'UADataType':
    <UADataType NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}" IsAbstract="false">
        <DisplayName>${type.name}</DisplayName>
        <References>
            <Reference ReferenceType="HasProperty">???</Reference>
            <Reference ReferenceType="HasSubtype" IsForward="false">???</Reference>
        </References>
    </UADataType>

    % endif
    % endif
% endfor
</UANodeSet>