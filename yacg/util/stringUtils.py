
def toUpperCamelCase(text):
    """converts a given Text to a upper camel case text
    this is a example -> ThisIsAExample"""

    splittedText = text.split()
    upperCamelCase = ''
    for t in splittedText:
        upperCamelCase += t[0:1].capitalize()
        upperCamelCase += t[1:]
    return upperCamelCase


def toUpperCaseName(text):
    """converts all characters of a given text to upper cases and relplaces
    non-ascii characters with '-'
    """

    capText = text.upper()
    return ''.join([i if (ord(i) < 123) and (ord(i) > 47) else '_' for i in capText])
