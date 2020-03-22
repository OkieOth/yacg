@startuml

% for type in modelTypes:
class ${type.name} {
    % for prop in type.properties:
    ${prop.type.name}${'[]' if prop.isArray else ''} ${prop.name} 
    % endfor
}

% endfor

% for type in modelTypes:
    <%
        ## array to store already printed links between the objects
        alreadyLinkedTypes=[]
    %>
    % for prop in type.properties:
        % if not prop.type.isBaseType and (not (prop.type.name in alreadyLinkedTypes)):
${type.name} ${ '"0"' if prop.isArray else '' } *-- ${'"n"' if prop.isArray else ''} ${prop.type.name}        
            <%
                ## add the current type name to the already linked types
                alreadyLinkedTypes.append(prop.type.name)
            %>
        % endif 
    % endfor
% endfor

footer \ngenerated with yacg (https://github.com/OkieOth/yacg),\npowered by plantuml (https://plantuml.com/)
@enduml