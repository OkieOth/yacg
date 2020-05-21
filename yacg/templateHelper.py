"""functions passed to the templates, that cam be used there
"""


def addLineBreakToDescription(textLine, indent):
    indentStr = ' ' * indent if indent > 0 else ''
    breakedText = ''
    currentLen = 0
    splittedLine = textLine.split()
    for t in splittedLine:
        if currentLen > 60:
            currentLen = 0
            breakedText = breakedText + '\n' + indentStr
        else:
            currentLen = currentLen + len(t)
            breakedText = breakedText + ' '
        breakedText = breakedText + t
    return breakedText

