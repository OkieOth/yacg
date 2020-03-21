@startuml
% for type in modelTypes:
class ${type.name} {
    % for prop in type.properties:
    ${prop.type.name} ${prop.name} 
    % endfor
}

% endfor

% for type in modelTypes:
    % for prop in type.properties:
        % if not prop.type.isBaseType:
${type.name} *-- ${prop.type.name}        
        % endif 
    % endfor

% endfor

@enduml