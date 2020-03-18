
def toUpperCamelCase(text):
    """converts a given Text to a upper camel case text
    this is a example -> ThisIsAExample"""
    
    splittedText = text.split()
    upperCamelCase = ''
    for t in splittedText:
        upperCamelCase += t.capitalize()
    return upperCamelCase