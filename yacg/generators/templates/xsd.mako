## Template to create PlantUml class diagrams from the model types
<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model

    templateFile = 'xsd.mako'
    templateVersion = '1.0.0'

    def addLineBreakToDescription(textLine):
        breakedText = ''
        splittedLine = textLine.split()
        i = 0
        for t in splittedLine:
            if i==5:
                breakedText = breakedText + '\\n'
                i=0
            if i>0:
                breakedText = breakedText + ' '
            breakedText = breakedText + t
            i = i + 1
        return breakedText

    def printXsdType(prop):
        type = prop.type
        if type is None:
            return '???'
        elif isinstance(type, model.IntegerType):
            return 'xsd:integer'
        elif isinstance(type, model.NumberType):
            return 'xsd:decimal'
        elif isinstance(type, model.BooleanType):
            return 'xsd:boolean'
        elif isinstance(type, model.StringType):
            return 'xsd:string'
        elif isinstance(type, model.UuidType):
            return 'tns:Guid'
        elif isinstance(type, model.EnumType):
            return "tns:{}".format(type.name)
        elif isinstance(type, model.DateType):
            return 'xsd:date'
        elif isinstance(type, model.TimeType):
            return 'xsd:time'
        elif isinstance(type, model.DateTimeType):
            return 'xsd:dateTime'
        elif isinstance(type, model.ComplexType):
            return "tns:{}".format(type.name)
        else:
            return '???'

    def printOccurs(prop):
        if prop.isArray:
            return ' minOccurs="0" maxOccurs="unbounded"'
        else:
            return ''

    modelName = templateParameters.get('modelName','<<PLEASE SET modelName TEMPLATE PARAM>>')
    version = templateParameters.get('version','<<PLEASE SET version TEMPLATE PARAM>>')

%>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    targetNamespace="http://swarco.com/core/service/${modelName}/${version}"
    xmlns:tns="http://swarco.com/core/service/${modelName}/${version}"
    elementFormDefault="qualified" xml:lang="en">
    <!--
        generated with yacg (https://github.com/OkieOth/yacg),
        (template: ${templateFile} v${templateVersion})
    -->
    <xsd:simpleType name="Guid">
         <xsd:restriction base="xsd:string">
             <xsd:pattern value="[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}" />
         </xsd:restriction>
    </xsd:simpleType>

## Handle enums - start
% for type in modelTypes:
    % if isinstance(type, model.EnumType):
    <xsd:simpleType name="${modelFuncs.getTypeName(type)}">
        % if hasattr(type,'description') and (type.description != None):
        <xsd:annotation>
            <xsd:documentation>
                ${addLineBreakToDescription(type.description)}
            </xsd:documentation>
        </xsd:annotation>
        % endif
        <xsd:restriction base="xsd:NCName">
        % for value in type.values:
            <xsd:enumeration value="${value}"/>
        % endfor
        </xsd:restriction>
    </xsd:simpleType>
    % endif
% endfor
## Handle enums - end

## Handle complex types - start
% for type in modelTypes:
    % if not isinstance(type, model.EnumType):
    <xsd:element name="${modelFuncs.getTypeName(type)}" type="tns:${modelFuncs.getTypeName(type)}"/>
    <xsd:complexType name="${modelFuncs.getTypeName(type)}">
        % if hasattr(type,'description') and (type.description != None):
        <xsd:annotation>
            <xsd:documentation>
                ${addLineBreakToDescription(type.description)}
            </xsd:documentation>
        </xsd:annotation>
        % endif
        <xsd:sequence>
            % for prop in type.properties:
            <xsd:element name="${prop.name}" type="${ printXsdType(prop) }"${printOccurs(prop)}>
                % if hasattr(prop,'description') and (prop.description != None):
                <xsd:annotation>
                    <xsd:documentation>
                        ${addLineBreakToDescription(prop.description)}
                    </xsd:documentation>
                </xsd:annotation>
                % endif
            </xsd:element>
            % endfor
        </xsd:sequence>
    </xsd:complexType>
    % endif
% endfor
</xsd:schema>