## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.javaFuncs as javaFuncs

    templateFile = 'javaBeans.mako'
    templateVersion = '1.0.0'

    packageName = templateParameters.get('modelPackage','<<PLEASE SET modelPackage TEMPLATE PARAM>>')

%>// Attention, this file is generated. Manual changes get lost with the next
// run of the code generation.
// created by yacg (template: ${templateFile} v${templateVersion})

package ${packageName};

% if isinstance(currentType, model.EnumType):
    % if currentType.description != None:
/**
${templateHelper.addLineBreakToDescription(currentType.description,4)}
*/
    % endif
public static enum ${currentType.name} {
    % for value in currentType.values:
    ${stringUtils.toUpperCaseName(value)}("${value}")${',' if value != currentType.values[-1] else ';'}
    % endfor

    private String value;

    private ${currentType.name}(String value) {
        this.value = value;
    }
}
% else:
    % if currentType.description != None:
/**
${templateHelper.addLineBreakToDescription(currentType.description,4)}
*/
    % endif
class ${currentType.name} ${javaFuncs.printExtendsType(currentType)}{
    % if modelFuncs.hasTypeProperties(currentType):
        % for property in currentType.properties:
            % if property.description != None:
    /**
    ${templateHelper.addLineBreakToDescription(property.description,4)}
    */
            % endif
    private ${javaFuncs.getJavaType(property.type, property.isArray)} ${property.name};

        % endfor
    % endif

    public ${currentType.name}() {
        super();
    }

    % if modelFuncs.hasTypeProperties(currentType):
        % for property in currentType.properties:
    public ${javaFuncs.getJavaType(property.type, property.isArray)} get${stringUtils.toUpperCamelCase(property.name)}() {
        return this.${property.name};
    };

    public void set${stringUtils.toUpperCamelCase(property.name)}(${javaFuncs.getJavaType(property.type, property.isArray)} value) {
        this.${property.name} = value;
    };

        % endfor
    % endif
    @Override
    public boolean equals(Object obj) {
        if (obj==null) return false;
        if ( ! (obj instanceof ${currentType.name})) return false;

        ${currentType.name} _typeInst = (${currentType.name}) obj;

    % if modelFuncs.hasTypeProperties(currentType):
        % for property in currentType.properties:
        ${javaFuncs.getJavaType(property.type, property.isArray)} _${property.name} = _typeInst.getget${stringUtils.toUpperCamelCase(property.name)}();
        if (this.${property.name} == null && _${property.name} != null) return false;
        if (this.${property.name} != null) {
            if (!this.${property.name}.equals(_${property.name})) return false;
        }

        % endfor
    % endif
    % if modelFuncs.hasTypeExtendsType(currentType):
        return super.equals(obj);
    % else:
        return true;
    % endif
    }
}
% endif
