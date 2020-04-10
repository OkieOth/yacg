## Template to create a Python file with type beans of the model types
<%
    import yacg.templateHelper as templateHelper

    templateFile = 'pythonBeans.mako'
    templateVersion = '1.0.0'
%>

# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation. 
# created by yacg (template: ${templateFile} v${templateVersion})

% for type in modelTypes:
class ${type.name}${ ' ({})'.format(type.extendsType.name) if type.extendsType is not None else ''}:
    % if type.description != None:
    """${templateHelper.addLineBreakToDescription(type.description,4)}        
    """

    % endif
    
    def __init__(self):
        pass


% endfor
