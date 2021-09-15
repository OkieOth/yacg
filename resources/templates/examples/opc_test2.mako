<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model

    templateFile = 'template.mako'
    templateVersion = '1.0.0'

    usedIds = {}
    lastUsedId = [0]

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
<UANodeSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd" xmlns:uax="http://opcfoundation.org/UA/2008/02/Types.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:s1="http://astra.admin.ch/Types/Base/0.26">
    <NamespaceUris>
        <Uri>http://astra.admin.ch/Types/Base/0.26</Uri>
    </NamespaceUris>
    <Models>
        <Model ModelUri="http://astra.admin.ch/Types/Base/0.26" Version="0.26" PublicationDate="2021-08-10T08:46:39.397Z">
            <RequiredModel ModelUri="http://opcfoundation.org/UA/" Version="1.04.7"></RequiredModel>
        </Model>
    </Models>
    <Aliases>
% for type in modelTypes:
        <Alias Alias="${type.name}">i=${printId(type.name)}</Alias>
% endfor
    </Aliases>
% for type in modelTypes:
    <UAObjectType NodeId="ns=1;i=${printId(type.name)}" BrowseName="1:${type.name}">
    % if type.description is not None:
        <Description Locale="${descriptionLocale}">${type.description}</Description>
    % endif
        <DisplayName>${type.name}</DisplayName>
        <References>
        </References>
    </UAObjectType>
% endfor
</UANodeSet>