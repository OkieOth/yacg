## Template to create a Python file with type beans of the model types
<%
    import yacg.model.model as model
    import yacg.templateHelper as templateHelper
    import yacg.model.modelFuncs as modelFuncs
    import yacg.util.stringUtils as stringUtils
    import yacg.generators.helper.pythonFuncs as pythonFuncs

    templateFile = 'javaBeans.mako'
    templateVersion = '1.0.0'

    packageName = templateParameters.get('modelPackage','<<PLEASE SET modelPackage TEMPLATE PARAM>>')

%># Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: ${templateFile} v${templateVersion})

package ${packageName};

% if isinstance(currentType, model.EnumType):    
// I am a Enum type
% else:
// I am a normal Java bean 
% endif
