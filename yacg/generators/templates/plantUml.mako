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

%>
@startuml

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
        ${modelFuncs.getTypeName(prop.type)}${'[]' if prop.isArray else ''} ${prop.name} 
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
    %>
    % if hasattr(type,'properties'):
        % for prop in type.properties:
            % if (not modelFuncs.isBaseType(prop.type)) and (not (prop.type.name in alreadyLinkedTypes)):
${modelFuncs.getTypeName(type)} ${ '"0"' if prop.isArray else '' } *-- ${'"n"' if prop.isArray else ''} ${modelFuncs.getTypeName(prop.type)}        
            <%
                ## add the current type name to the already linked types
                alreadyLinkedTypes.append(modelFuncs.getTypeName(prop.type))
            %>
            % endif 
        % endfor
    % endif 
% endfor

footer \ngenerated with yacg (https://github.com/OkieOth/yacg),\n(template: ${templateFile} v${templateVersion})\npowered by plantuml (https://plantuml.com/)
@enduml