import re


def toLowerCamelCase(text):
    """converts a given Text to a lower camel case text
    this is an example -> thisIsAnExample"""

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


def toUpperCamelCase(text, separator=None):
    """converts a given Text to a upper camel case text
    this is an example -> ThisIsAnExample"""

    splittedText = text.split() if separator is None else text.split(separator)
    upperCamelCase = ''
    for t in splittedText:
        upperCamelCase += t[0:1].capitalize()
        upperCamelCase += t[1:]
    return upperCamelCase


def toUpperCaseName(text):
    """converts all characters of a given text to upper cases and replaces
    non-ascii characters with '-'
    """

    capText = text.upper()
    return toName(capText)


def toSnakeCase(text):
    """converts camel case to snake case
    ThisIsAnExample -> this_is_an_example"""

    return ''.join(['_' + c.lower() if c.isupper() else c for c in text]).lstrip('_')


def toName(text):
    """converts a text that it is suitable as name
    """

    ret = "x"
    lastRet = ""
    while ret != lastRet:
        lastRet = ret
        ret = re.sub("[^0-9a-zA-Z_]+", "_", text)
    pattern = re.compile("^[0-9]")
    return '_' + ret if pattern.match(ret) else ret


def snakeToUpperCamelCase(text):
    """converts a given snake case text to upper camel case text
    this_is_a_snake_case -> ThisIsASnakeCase"""
    if text is None:
        return None
    tokens = text.split('_')
    upperCamelCase = ''
    for t in tokens:
        upperCamelCase += t[0:1].capitalize()
        upperCamelCase += t[1:]
    return upperCamelCase


def snakeToLowerCamelCase(text):
    """converts a given snake case text to lower camel case text
    this_is_a_snake_case -> thisIsASnakeCase"""
    if text is None:
        return None
    tokens = text.split('_')
    lowerCamelCase = None
    for t in tokens:
        if lowerCamelCase is None:
            lowerCamelCase = t[0:1].lower()
            lowerCamelCase += t[1:]
            print('lower first: t={} lcc={}'.format(t, lowerCamelCase))
        else:
            lowerCamelCase += t[0:1].capitalize()
            lowerCamelCase += t[1:]
            print('lower subsequent: t={} lcc={}'.format(t, lowerCamelCase))
    return lowerCamelCase


def toLowerCase(text):
    """ ensures that the first letter of the text is lower case
    AbCdE -> abCdE"""
    if text is None:
        return None
    lowerCase = text[0:1].lower()
    lowerCase += text[1:]
    return lowerCase


def toUpperCase(text):
    """ ensures that the first letter of the text is upper case
    aBcDe -> ABcDe"""
    if text is None:
        return None
    upperCase = text[0:1].upper()
    upperCase += text[1:]
    return upperCase
