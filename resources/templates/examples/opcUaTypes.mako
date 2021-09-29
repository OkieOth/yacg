<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
    import yacg.util.dateUtils as dateUtils

    templateFile = 'template.mako'
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
    ## % if not 'opcUaTag' in getattr(type, 'x-tags'):
        <Alias Alias="${type.name}">ns=1;i=${printId(type.name)}</Alias>
    ## % endif
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