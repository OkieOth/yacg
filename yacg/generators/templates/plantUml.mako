## Template to create PlantUml class diagrams from the model types
<%
    import yacg.model.modelFuncs as modelFuncs
    import yacg.model.model as model
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

    def printArrayDimensions(prop):
        if not prop.isArray:
            return ''
        return '[]' * prop.arrayDimensions

    def printTypeTags(type):
        ret = ''
        tagCount = 0
        for tag in type.tags:
            if tagCount == 4:
                ret = ret + '\n'
                tagCount = 0
            tmp = '**#{}**'.format(tag.name)
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

    def printTypeName(type):
        if modelFuncs.isDictionaryType(type):
            if type.topLevelType:
                return modelFuncs.getTypeName(type)
            else:
                return "Map<{}>".format(printTypeName(type.valueType))
        elif isinstance(type, model.ArrayType):
            if type.topLevelType:
                modelFuncs.getTypeName(type)
            else:
                return "{}[]".format(printTypeName(type.itemsType))
        else:
            return modelFuncs.getTypeName(type)

    def printPropType(prop):
        return printTypeName(prop.type)

    def printBeautifiedTypeName(type):
        if hasattr(type, "topLevelType") and type.topLevelType:
            return '"**{}**"'.format(modelFuncs.getTypeName(type))
        else:
            return '"{}"'.format(modelFuncs.getTypeName(type))

    def checkIfPrintPropTypeReference(propType, alreadyLinkedTypes):
        if modelFuncs.isBaseType(propType):
            return False
        if hasattr(propType, "topLevelType") and propType.topLevelType:
            return True
        if isinstance(propType, model.ComplexType):
            if propType.name in alreadyLinkedTypes:
                return False
            else:
                return True
        elif isinstance(propType, model.ArrayType):
            if modelFuncs.isBaseType(propType.itemsType):
                return False
            if propType.itemsType.name in alreadyLinkedTypes:
                return False
            if hasattr(propType.itemsType, "topLevelType") and propType.itemsType.topLevelType:
                return True
            else:
                return checkIfPrintPropTypeReference(propType.itemsType, alreadyLinkedTypes)
        elif isinstance(propType, model.DictionaryType):
            if modelFuncs.isBaseType(propType.valueType):
                return False
            if propType.valueType.name in alreadyLinkedTypes:
                return False
            if hasattr(propType.valueType, "topLevelType") and propType.valueType.topLevelType:
                return True
            else:
                return checkIfPrintPropTypeReference(propType.valueType, alreadyLinkedTypes)
        else:
            return False


    def getPropTypeReferenceToPrint(propType, alreadyLinkedTypes):
        if modelFuncs.isBaseType(propType):
            return "???"
        if hasattr(propType, "topLevelType") and propType.topLevelType:
            ret = propType.name
            alreadyLinkedTypes.append(ret)
            return ret
        if isinstance(propType, model.ComplexType):
            if propType.name in alreadyLinkedTypes:
                return "???"
            else:
                ret = propType.name
                alreadyLinkedTypes.append(ret)
                return ret
        elif isinstance(propType, model.ArrayType):
            if modelFuncs.isBaseType(propType.itemsType):
                return "???"
            if propType.itemsType.name in alreadyLinkedTypes:
                return "???"
            if hasattr(propType.itemsType, "topLevelType") and propType.itemsType.topLevelType:
                ret = propType.itemsType.name
                alreadyLinkedTypes.append(ret)
                return ret
            else:
                return getPropTypeReferenceToPrint(propType.itemsType, alreadyLinkedTypes)
        elif isinstance(propType, model.DictionaryType):
            if modelFuncs.isBaseType(propType.valueType):
                return "???"
            if propType.valueType.name in alreadyLinkedTypes:
                return "???"
            if hasattr(propType.valueType, "topLevelType") and propType.valueType.topLevelType:
                ret = propType.valueType.name
                alreadyLinkedTypes.append(ret)
                return ret
            else:
                return getPropTypeReferenceToPrint(propType.valueType, alreadyLinkedTypes)
        else:
            return "???"

    shouldTypeTagsBePrinted = templateParameters.get('printTypeTags',False)
    shouldPropertyTagsBePrinted = templateParameters.get('printPropertyTags',False)

%>
@startuml
hide empty methods
hide empty fields


% for type in modelTypes:
    % if modelFuncs.isEnumType(type):
enum ${printBeautifiedTypeName(type)} as ${modelFuncs.getTypeName(type)} {
        % for value in type.values:
    ${stringUtils.toUpperCaseName(value)}
        % endfor
}
    % elif modelFuncs.isComplexType(type):
class ${printBeautifiedTypeName(type)} as ${modelFuncs.getTypeName(type)} {
        % if hasattr(type,'properties'):
            % for prop in type.properties:
        ${printPropType(prop)}${printArrayDimensions(prop)} ${prop.name}${printForeignKeyComment(prop)}
            % endfor
        % endif
        % if shouldTypeTagsBePrinted and (len(type.tags) > 0):

        == // Type-Tags // ==
        ${printTypeTags(type)}
        % endif
        % if shouldPropertyTagsBePrinted:
        <% propertyTags = modelFuncs.getPropertyTagNamesForType(type) %>
        % for tag in propertyTags:
            % if tag == propertyTags[0]:
        --- // Property-Tags // ---
            % else:
        --
            % endif
        ${printPropertyTag(type, tag)}
            % endfor
        % endif
}
        % if hasattr(type,'description') and (type.description != None):
note top: ${addLineBreakToDescription(type.description)}
        % endif

        % if hasattr(type,'extendsType') and (type.extendsType != None):
${modelFuncs.getTypeName(type)} --|> ${modelFuncs.getTypeName(type.extendsType)}
        % endif
 
    % elif isinstance(type, model.DictionaryType) and type.topLevelType:
class ${printBeautifiedTypeName(type)} as ${modelFuncs.getTypeName(type)} <Map<${printTypeName(type.valueType)}>> {
}
    % elif isinstance(type, model.ArrayType) and type.topLevelType:
class ${printBeautifiedTypeName(type)} as ${modelFuncs.getTypeName(type)} extends List {
}
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
            % if checkIfPrintPropTypeReference(prop.type, alreadyLinkedTypes) :
${modelFuncs.getTypeName(type)} ${ '"0"' if prop.isArray else '' } *-- ${'"n"' if prop.isArray else ''} ${getPropTypeReferenceToPrint(prop.type, alreadyLinkedTypes)}
            % endif

            % if (prop.foreignKey is not None) and (prop.foreignKey.type.name not in alreadyLinkedTypes2):
${modelFuncs.getTypeName(type)} .. ${modelFuncs.getTypeName(prop.foreignKey.type)}
            <%
                ## add the current type name to the already linked types
                alreadyLinkedTypes2.append(prop.foreignKey.type.name)
            %>
            % endif
        % endfor
    % elif isinstance(type, model.DictionaryType) and type.topLevelType and (not modelFuncs.isBaseType(type.valueType)) and (type.valueType.topLevelType or isinstance(type.valueType, model.ComplexType)):
${modelFuncs.getTypeName(type)} -- ${type.valueType.name}
    % elif isinstance(prop.type, model.ArrayType) and type.topLevelType and (not modelFuncs.isBaseType(type.itemsType)) and (type.itemsType.topLevelType or isinstance(type.itemsType, model.ComplexType)):
        % if prop.type.itemsType.name not in alreadyLinkedTypes:
${modelFuncs.getTypeName(type)} -- ${type.itemsType.name}
        % endif
    % endif
% endfor

footer \ngenerated with yacg (https://github.com/OkieOth/yacg),\n(template: ${templateFile} v${templateVersion})\npowered by plantuml (https://plantuml.com/)
@enduml