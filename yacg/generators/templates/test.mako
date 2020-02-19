<%!
def calcOutput(text):
    text=text+" "
    return 3 * text

def calcOutput2(text):
    text=text+" "
    return 2 * text
%>

This is my first template
output 1:
${calcOutput("a string")}
output 2:
${calcOutput2("another string")}
