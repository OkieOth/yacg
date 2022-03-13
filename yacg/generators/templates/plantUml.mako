## Template to create PlantUml class diagrams from the model types
<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils

    templateFile = 'plantUml.mako'
    templateVersion = '1.1.0'

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

    def printForeignKeyComment(prop):
        ret = ''
        if (prop.foreignKey is not None) and (prop.foreignKey.type is not None):
            propTxt = '.' + prop.foreignKey.property.name if prop.foreignKey.property is not None else ''
            ret = '<color:grey>"" // -> {}{}""</color>'.format(prop.foreignKey.type.name, propTxt)
        return ret
    
    def printTypeTags(type):
        ret = ''
        tagCount = 0
        for tag in type.tags:
            if tagCount == 4:
                ret = ret + '\n'
                tagCount = 0
            tmp = '**#{}**'.format(ret, tag)
            ret = '{}, {}'.format(ret, tmp) if len(ret)>0 else '{}'.format(tmp)
            tagCount = tagCount + 1
        return ret

    def printPropertyTag(typeObj, tag):
        propsWithTag = modelFuncs.getPropertiesThatHasTag(tag, typeObj)
        if len(propsWithTag) == 0:
            return ''
        ret = '**#{}**: '.format(tag)
        tagCount = 0
        firstTag = True
        for prop in propsWithTag:
            tmp = ''
            if firstTag:
                firstTag = False
            else:
                ret = '{}, '.format(ret)
            if tagCount == 4:
                ret = ret + '\n'
                tagCount = 0
            ret = '{}{}'.format(ret, prop.name)
            tagCount = tagCount + 1
        return ret

    shouldTypeTagsBePrinted = templateParameters.get('printTypeTags',False)
    shouldPropertyTagsBePrinted = templateParameters.get('printPropertyTags',False)

%>
@startuml
hide empty methods

% for type in modelTypes:
    % if modelFuncs.isEnumType(type):
enum ${modelFuncs.getTypeName(type)} {
        % for value in type.values:
    ${stringUtils.toUpperCaseName(value)}
        % endfor
}
    % else:
class ${modelFuncs.getTypeName(type)} {
        % if hasattr(type,'properties'):
            % for prop in type.properties:
        ${modelFuncs.getTypeName(prop.type)}${'[]' if prop.isArray else ''} ${prop.name}${printForeignKeyComment(prop)}
            % endfor
        % endif
        % if shouldTypeTagsBePrinted and (len(type.tags) > 0):
        ==
        ${printTypeTags(type)}
        ==
        % endif
        % if shouldPropertyTagsBePrinted:
        <%
            propertyTags = modelFuncs.getPropertyTagsForType(type)
        %>
            % for tag in propertyTags:
        ${printPropertyTag(type, tag)}
        --
            % endfor
        % endif
}
    % endif

    % if hasattr(type,'description') and (type.description != None):
note top: ${addLineBreakToDescription(type.description)}
    % endif

    % if hasattr(type,'extendsType') and (type.extendsType != None):
${modelFuncs.getTypeName(type)} --|> ${modelFuncs.getTypeName(type.extendsType)}
    % endif
% endfor

% for type in modelTypes:
    <%
        ## array to store already printed links between the objects
        alreadyLinkedTypes=[]
        alreadyLinkedTypes2=[]
    %>
    % if hasattr(type,'properties'):
        % for prop in type.properties:
            % if (not modelFuncs.isBaseType(prop.type)):
                % if prop.type.name not in alreadyLinkedTypes:
${modelFuncs.getTypeName(type)} ${ '"0"' if prop.isArray else '' } *-- ${'"n"' if prop.isArray else ''} ${modelFuncs.getTypeName(prop.type)}
            <%
                ## add the current type name to the already linked types
                alreadyLinkedTypes.append(modelFuncs.getTypeName(prop.type))
            %>
                % endif
            % endif

            % if (prop.foreignKey is not None) and (prop.foreignKey.type.name not in alreadyLinkedTypes2):
${modelFuncs.getTypeName(type)} .. ${modelFuncs.getTypeName(prop.foreignKey.type)}
            <%
                ## add the current type name to the already linked types
                alreadyLinkedTypes2.append(prop.foreignKey.type.name)
            %>
            % endif
        % endfor
    % endif
% endfor

footer \ngenerated with yacg (https://github.com/OkieOth/yacg),\n(template: ${templateFile} v${templateVersion})\npowered by plantuml (https://plantuml.com/)
@enduml