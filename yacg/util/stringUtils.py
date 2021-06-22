import re


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
    return toName(capText)


def toSnakeCase(text):
    """converts camel case to snake case
    """

    return ''.join(['_' + c.lower() if c.isupper() else c for c in text]).lstrip('_')


def toName(text):
    """converts a text that it is suitable as name
    """

    ret = re.sub("[^0-9a-zA-Z_]+", "_", text)
    pattern = re.compile("^[0-9]")
    return '_' + ret if pattern.match(ret) else ret
