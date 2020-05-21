def toLowerCamelCase(text):
    """converts a given Text to a lower camel case text
    this is a example -> thisIsAExample"""

    splittedText = text.split()
    lowerCamelCase = None
    for t in splittedText:
        if lowerCamelCase is None:
            lowerCamelCase = t[0:1].lower()
            lowerCamelCase += t[1:]
        else:
            lowerCamelCase += t[0:1].capitalize()
            lowerCamelCase += t[1:]
    return lowerCamelCase


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
