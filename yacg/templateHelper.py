"""functions passed to the templates, that cam be used there
"""


# def addLineBreakToDescription(textLine, indent=0):
#     indentStr = ' ' * indent if indent > 0 else ''
#     breakedText = ''
#     currentLen = 0
#     splittedLine = textLine.split()
#     for t in splittedLine:
#         if currentLen > 60:
#             currentLen = 0
#             breakedText = breakedText + '\n' + indentStr
#         else:
#             currentLen = currentLen + len(t)
#             breakedText = breakedText + ' '
#         breakedText = breakedText + t
#     return breakedText

def addLineBreakToDescription(textLine, indent=0, prefix=''):
    indentStr = (' ' * indent if indent > 0 else '') + prefix
    breakedText = prefix
    currentLen = 0
    splittedLine = textLine.split()
    for t in splittedLine:
        # print('currentLen=' + str(currentLen))
        if currentLen > 60:
            currentLen = 0
            breakedText = breakedText + '\n' + indentStr
        elif currentLen > 0:
            # add space in-between the previous and the current token
            breakedText = breakedText + ' '
        currentLen = currentLen + len(t)
        breakedText = breakedText + t
    return breakedText
