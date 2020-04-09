## Template to create a Python file with type beans of the model types
<%
    templateFile = 'pythonBeans.mako'
    templateVersion = '1.0.0'

    def addLineBreakToDescription(textLine, indent):
        indentStr = ' ' * indent if indent > 0 else ''
        breakedText = ''
        currentLen = 0
        splittedLine = textLine.split()
        i = 0
        for t in splittedLine:
            if currentLen > 60:
                currentLen = 0
                breakedText = breakedText + '\n' + indentStr
            else:
                currentLen = currentLen + len(t)
                breakedText = breakedText + ' '
            breakedText = breakedText + t
        return breakedText
%>

# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation. 
# created by yacg (template: ${templateFile} v${templateVersion})

% for type in modelTypes:
class ${type.name}${ ' ({})'.format(type.extendsType.name) if type.extendsType is not None else ''}:
    % if type.description != None:
    """${addLineBreakToDescription(type.description,4)}        
    """

    % endif
    
    def __init__(self):
        pass


% endfor
