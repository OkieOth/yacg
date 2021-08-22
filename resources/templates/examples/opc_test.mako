## Template to create PlantUml class diagrams from the model types
<%!
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model

    templateFile = 'opc_test.mako'
    templateVersion = '1.0.0'

    ordinalsDict = {}
    lastOrdinal = [0]

    def printOrdinal(typeName):
        currentOrdinal = ordinalsDict.get(typeName, None)
        if currentOrdinal is None:
            ordinalsDict[typeName] = lastOrdinal[0]
            t = lastOrdinal[0] + 1
            lastOrdinal[0] = t
            return t
        else:
            return currentOrdinal

%>
<UANodeSet 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd"
    xmlns:uax="http://opcfoundation.org/UA/2008/02/Types.xsd"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
    xmlns:s1="http://astra.admin.ch/Types/Base/0.26">
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
        <Alias Alias="${type.name}">ns=1;i=${printOrdinal(type.name)}</Alias>
% endfoFr
    </Aliases>
% for type in modelTypes:
    <UAObjectType NodeId="ns=1;i=5721" BrowseName="1:WSType0v26" IsAbstract="false">
        <DisplayName>WSType0v26</DisplayName>
        <Description Locale="de">Wechselsignal (WSType0v26)</Description>
        <References>
            <Reference ReferenceType="HasSubtype" IsForward="false">ns=1;i=5000</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8720</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8721</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8722</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8723</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8724</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8725</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8726</Reference>
            <Reference ReferenceType="HasComponent">ns=1;i=8727</Reference>
        </References>
    </UAObjectType>

% endfor

</UANodeSet>

